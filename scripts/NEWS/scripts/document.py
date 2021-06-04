
# Imports JSON library
import json

# Imports ZIP library
from zipfile import ZipFile

# Imports the remove function
from os import remove

class Document(object):

	def __init__(self):
		
		# Flag to state whether data is loaded or not
		self.is_loaded = False

		# Initializes the source attribute
		self.source = None

		# Initializes the url attribute
		self.url = None

		# Initializes the language attribute
		self.lang = None

		# Initializes the date attribute
		self.date = None

		# Initializes the author attribute
		self.author = None

		# Initializes the keyword attribute
		self.keyword = None

		# Initializes the title attribute
		self.title = None

		# Initializes the text attribute
		self.text = None

		# Initializes the ID attribute
		self.id = None


	def load_from_json(self, path):
		""" Initializes attributes from JSON file.

		Args:
			path (str): path to JSON file with document information.

		Raises:
			IOError: if the file does not exists or can not be opened.
			JSONDecodeError: if the file is not a valid JSON file.

		"""

		# Checks if file is zipped or not
		if path.endswith(".zip"):
			
			# Opens the ZIP file
			archive = ZipFile(path, "r")

			# Gets the filename from file
			filename = archive.infolist()[0].filename

			# Reads the file
			archive = archive.read(filename)

			# Loads the archive as JSON
			input_data = json.loads(archive)

		elif path.endswith(".json"):

			# Opens the file in read mode
			input_file = open(path, "r")

			# Reads the file as JSON format
			input_data = json.load(input_file)

		# Sets the source attribute
		self.source = input_data["source"]

		# Sets URL attribute
		self.url = input_data["url"]

		# Sets the language attribute
		self.lang = input_data["lang"]

		# Sets the date attribute
		self.date = input_data["date"]

		# Sets the author attribute
		self.author = input_data["author"]

		# Sets the keyword attribute
		self.keyword = input_data["keyword"]

		# Sets the title attribute
		self.title = input_data["title"]

		# Sets the text attribute
		self.text = input_data["text"]

		# Sets the ID attribute
		self.id = input_data["id"]

		# Sets loaded flag on True
		self.is_loaded = True


	def load_from_dict(self, parameters):
		""" Initializes attributes from dictionary.

		"""

		# Sets the set attribute
		self.source = parameters["source"]

		# Sets the URL attribute
		self.url = parameters["url"]

		# Sets the language attribute
		self.lang = parameters["lang"]

		# Sets the date attribute
		self.date = parameters["date"]

		# Sets the author attribtue
		self.author = parameters["author"]

		# Sets the keyword attribtue
		self.keyword = parameters["keyword"]

		# Sets the title attribute
		self.title = parameters["title"]

		# Sets the text attribute
		self.text = parameters["text"]

		# Sets the ID attribute
		self.id = parameters["id"]



	def dump_to_json(self, path):
		""" Saves the object attributes into a JSON file.

		Args:
			path (str): path for the new JSON file. If the file exists it will be
				replaced with a new file.

		"""

		# Creates the attributes dictionary
		attributes_dict = {
			"source": self.source,
			"url": self.url,
			"lang": self.lang,
			"date": self.date,
			"author": self.author,
			"keyword": self.keyword,
			"title": self.title,
			"text": self.text,
			"id": self.id
		}

		# Defines the JSON path
		json_path = path + ".json"

		# Defines the ZIP file
		zip_path = path + ".zip"

		# Opens the output file
		with open(json_path, "w") as output_file:

			# Dumps attribute dictionary into a JSON file
			json_string = json.dump(attributes_dict, output_file, indent=4)

		# Zips the output file
		ZipFile(zip_path, mode="w").write(json_path)

		# Removes the original file
		remove(json_path)


	def __eq__(self, other):
		""" Checks if another object is equal to current.

		Performs the comparison between two objects that might be from the
		same class and equal. The comparison starts by checking that both
		objects are form the Document class. Then it checks that  the 'id'
		attribute is equal between both objects.		

		Args:
			other (Document): object that will be compared to current instance
				of Document class.

		Returns:
			bool: True if both objects are equal. False otherwise.

		Raises:
			Exception: if the other object is not an instance of the Document
				class.
			Exception: if either the current or the other instance data was not 
				loaded before performing the comparison.
		
		"""

		# Checks if other is instance of Document class
		if not isinstance(other, Document):
			raise Exception("Other object is not instance of Document class.")

		# Checks if instace was loaded
		if not self.is_loaded:
			raise Exception("Current instance data was not loaded.")

		# Checks if other object data is loaded
		if not other.is_loaded:
			raise Exception("Other instance data was not loaded.")

		# Checks if ID is equal between objects
		elif self.id == other.id:
			# Returns true if both IDs are equal
			return True
		else:
			# Returns false if IDs are different
			return False


	def __str__(self):
		""" Prints string representation of Document object. """
		return self.id
