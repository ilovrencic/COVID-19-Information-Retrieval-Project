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
		self.whole_text = title+abstract+body

	def __str__(self):
		paper = ""

		paper += Paper.addParagraph('Title', self.title)
		paper += Paper.addParagraph('Abstract', self.abstract)
		paper += Paper.addParagraph('Body', self.body)

		return paper

	#stylistic method for adding a paragraph
	@staticmethod
	def addParagraph(header,body):
		if not body:
			return ""

		return Paper.bold(header) + "\n" + body + "\n\n"

	#text bolding for better output
	@staticmethod
	def bold(text):
		return '\033[1m' + text + '\033[0m'

#Parser class
#It's used to parse dataset to manageable data
class Parser:
	def __init__(self, datasets = []):
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

			files = [file for file in os.listdir(dataset.value) if file.endswith(".json")]
			
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

	#method for extracting certain part of papers into a dictonary
	def getDictonary(self,filter):
		dataset_dict = {}
		for key in self.data_dicts:
			texts_dict = {}
			papers = self.data_dicts[key]
			for id in papers:
				if(filter == "title"):
					texts_dict[id] = Paper(title = papers[id].title)
				elif(filter == "abstract"):
					texts_dict[id] = Paper(abstract = papers[id].abstract)
				else:
					texts_dict[id] = Paper(body = papers[id].body)

			dataset_dict[key] = texts_dict
		return dataset_dict

	#returns a dictonary of titles
	def titles(self):
		return self.getDictonary("title")

	#returns a dictonary of abstracts
	def abstracts(self):
		return self.getDictonary("abstract")

	#returns a dictonary of bodies
	def bodies(self):
		return self.getDictonary("body")

#example of usage
def main():

	#Example of parsing the Common dataset and BIORIXIV dataset
	p = Parser([Dataset.COMMON,Dataset.BIORXIV])
	p.parse()

	#Print of one paper based on index (change the indexByFile parametar to 
	#find papers by their id)
	print(p.data_dicts[Dataset.COMMON][10])


	#Example of printing all the abstracts inside of parsed dataset
	abstracts = p.bodies()
	for abstracts in abstracts[Dataset.BIORXIV].values():
		print(abstracts)

#Uncomment this to try it in terminal
#main()
