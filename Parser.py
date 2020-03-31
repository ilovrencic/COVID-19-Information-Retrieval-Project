from enum import Enum
import json
import os


BASE_URL = "./dataset/"
#enum type of a dataset we will parsing
class Dataset(Enum):
	BIORXIV = BASE_URL + "biorxiv_medrxiv100/"
	COMMON = BASE_URL + "comm_use100/"
	NONCOMMON = BASE_URL + "noncomm_use100/"

#Custom exception if the dataset isn't provided
class NoDatasetDefinedException(Exception):
	pass

#Paper class that contains textual elements of a paper
class Paper:
	def __init__(self, title = "", abstract = "", body = ""):
		self.title = title
		self.abstract = abstract
		self.body = body

	def __str__(self):
		paper = ""
		paper += '\033[1m'+"Title"+'\033[0m'+"\n" if self.title is not "" else ""
		paper += self.title 
		paper += "\n"+"\n" if self.title is not "" else ""
		paper += '\033[1m'+"Abstract"+'\033[0m'+"\n" if self.abstract is not "" else ""
		paper += self.abstract
		paper += "\n"+"\n" if self.abstract is not "" else ""
		paper += '\033[1m'+"Body"+'\033[0m'+"\n" if self.body is not "" else ""
		paper += self.body
		paper += "\n"+"\n" if self.body is not "" else ""
		return paper

#Parser class
#It's used to parse dataset to manageable data
class Parser:
	def __init__(self, datasets = list()):
		self.datasets = datasets # paths of datasets we want to parse
		self.data_dicts = {} # data will be in dictonary combined into a text
		self.json_dicts = {} # data will be in dictonary based on parts of paper (e.g. introduction,..)

	#returns a tuple with title, abstract, body and whole text
	# (title, abstract, body , whole text)
	def transformJsonToString(self,paper_dict):
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

		return Paper(title,abstract_text,body_text)

	#Main function 
	#param parseByParts determins whether will paper be parsed by parts
	#or will it be put together
	#param indexByFile tells whether will dict be index by paper name or
	#just number index
	def parse(self, parseByParts = False, indexByFile = False):
		if len(self.datasets) == 0:
			raise NoDatasetDefinedException

		for dataset in self.datasets:
			data_dict = {}
			json_dict = {}
			try:
				files = [file for file in os.listdir(dataset.value) if file.endswith(".json")]
			except Exception as e:
				raise e

			paper_index = 0
			for file in files:
				with open(dataset.value+file,"r") as paper:
					paper_dict = json.load(paper)

					if(indexByFile):
						json_dict[file[:-5]] = paper_dict
						data_dict[file[:-5]] = self.transformJsonToString(paper_dict)
					else:
						json_dict[paper_index] = paper_dict
						data_dict[paper_index] = self.transformJsonToString(paper_dict)
				paper_index += 1

			self.data_dicts[dataset] = data_dict
			self.json_dicts[dataset] = json_dict

	#returns a dictonary of titles
	def titles(self):
		dataset_dict = {}
		for key in self.data_dicts.keys():
			titles_dict = {}
			papers = self.data_dicts[key]
			for id in papers.keys():
				titles_dict[id] = Paper(title = papers[id].title)

			dataset_dict[key] = titles_dict
		return dataset_dict

	#returns a dictonary of abstracts
	def abstracts(self):
		dataset_dict = {}
		for key in self.data_dicts.keys():
			abstracts_dict = {}
			papers = self.data_dicts[key]
			for id in papers.keys():
				abstracts_dict[id] = Paper(abstract = papers[id].abstract)

			dataset_dict[key] = abstracts_dict
		return dataset_dict

	#returns a dictonary of bodies
	def bodies(self):
		dataset_dict = {}
		for key in self.data_dicts.keys():
			bodies_dict = {}
			papers = self.data_dicts[key]
			for id in papers.keys():
				bodies_dict[id] = Paper(body = papers[id].body)

			dataset_dict[key] = bodies_dict
		return dataset_dict


#example of usage
def main():

	#Example of parsing the Common dataset and BIORIXIV dataset
	p = Parser([Dataset.COMMON,Dataset.BIORXIV])
	p.parse()

	#Print of one paper based on index (change the indexByFile parametar to 
	#find papers by their id)
	print(p.data_dicts[Dataset.COMMON][10])


	#Example of printing all the abstracts inside of parsed dataset
	abstracts = p.abstracts()
	for abstracts in abstracts[Dataset.BIORXIV].values():
		print(abstracts)

#Uncomment this to try it in terminal
#main()
