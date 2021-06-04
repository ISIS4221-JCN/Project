# This script will remove the duplicates from a specific folder
PATH_TO_FILES = "/media/nicolas-rocha/FOTOS/NLP/files/fr/"

PATH_TO_DICTS = "/media/nicolas-rocha/FOTOS/NLP/dicts/fr/"

# Maximum size of document list
N = 20000

# Imports the OS package
import os

# Imports the CSV package
import csv

# Imports the GLOB package
import glob

# Imports the execution environment
import concurrent.futures

from tqdm import tqdm

# Imports itertools
import itertools

# Imports the Document class
from document import Document


def save_to_disk(documents, path, index):

  fname = "dict_" + str(index) + ".csv"

  with open(PATH_TO_DICTS + fname, "w") as output_file:

    csv_writer = csv.writer(output_file, delimiter=',')

    for key in documents.keys():

      csv_writer.writerow([key, documents[key]])


# Creates the files list
files = os.listdir(PATH_TO_FILES)

# Prints information on the list
print("There are {} files to be processed".format(len(files)))

# Creates a list definition
document_dict = {}

# Creates an index for the files
i = 0

# Iterates over files
for file in tqdm(files):

  # Tries to load the document
  try:
    
    # Creates the document instance
    doc = Document()

    # Loads the document from file
    doc.load_from_json(PATH_TO_FILES + file)

  except:
    os.remove(PATH_TO_FILES + file)

  # If document is not in list it is appended
  if doc.id not in document_dict.keys():
    document_dict[doc.id] = file

  # If document is in list, it is discarded
  else:
    os.remove(PATH_TO_FILES + file)

  # If document list is equal to max size, it is saved on disk
  if len(document_dict.keys()) == N:
    
    # Saves dictionary in disk
    save_to_disk(document_dict, PATH_TO_DICTS, i)

    # Initializes an empty dictionary
    document_dict = {}

    # Increments the index
    i += 1

# Increments index
i += 1

# Stores remaining values
save_to_disk(document_dict, PATH_TO_DICTS, i)
