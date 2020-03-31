from enum import Enum
import json
import os


BASE_URL = "/Users/ilovrencic/Personal/FER/2.semestar/Analiza i pretraživanje teksta/TAR-2020-Project/dataset/"
#enum type of a dataset we will parsing
#since everyones path to them is different, I advise you
#to change this accordingly :)
class Dataset(Enum):
	BIORXIV = BASE_URL + "biorxiv_medrxiv100/"
	COMMON = BASE_URL + "comm_use100/"
	NONCOMMON = BASE_URL + "noncomm_use100/"

#Custom exception if the dataset isn't provided
class NoDatasetDefinedException(Exception):
	pass

#Parser class
#It's used to parse dataset to manageable data 
class Parser:
	def __init__(self, datasets = list()):
		if isinstance(datasets,list):
			self.datasets = datasets # paths of datasets we want to parse
		else:
			self.datasets = list()
		self.data_dicts = {} # data will be in dictonary based on parts of paper (e.g. introduction,..)

	#returns a tuple with title, abstract, body and whole text
	# (title, abstract, body , whole text)
	def transformJsonToString(self,paper_dict):
		paper_text = ""
		title = ""
		abstract_text = ""
		body_text = ""
		
		if "metadata" in paper_dict:
			metadata = paper_dict["metadata"]
			if "title" in metadata:
				title = metadata["title"]
		if "abstract" in paper_dict:
			abstract = paper_dict["abstract"]
			for paragraph in abstract:
				if "text" in paragraph:
					abstract_text += paragraph["text"]
		if "body_text" in paper_dict:
			body = paper_dict["body_text"]
			for paragraph in body:
				if "text" in paragraph:
					body_text += paragraph["text"]

		paper_text = title+abstract_text+body_text
		return (title,abstract_text,body_text,paper_text)

	#Main function 
	#param parseByParts determins whether will paper be parsed by parts
	#or will it be put together
	def parse(self, parseByParts = True):
		if len(self.datasets) == 0:
			raise NoDatasetDefinedException
		
		for dataset in self.datasets:
			data_dict = {}
			try:
				files = [file for file in os.listdir(dataset.value) if file.endswith(".json")]
			except Exception as e:
				raise e

			for file in files:
				with open(dataset.value+file,"r") as paper:
					paper_dict = json.load(paper)
					if(parseByParts):
						data_dict[file] = paper_dict
					else:
						data_dict[file] = self.transformJsonToString(paper_dict)

			self.data_dicts[dataset] = data_dict
				
#example of usage
def main():
	p = Parser([Dataset.COMMON])
	p.parse(parseByParts = True)
	print(p.data_dicts)
main()
