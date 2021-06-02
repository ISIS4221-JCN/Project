# This script will check that there are no duplicates in a specific folder
PATH_TO_FILES = "/media/nicolas-rocha/FOTOS/NLP/files/es/"

# Imports the OS package
import os

# Imports the GLOB package
import glob

# Imports the execution environment
import concurrent.futures

from tqdm import tqdm

# Imports itertools
import itertools

# Imports the Document class
from document import Document

# 
files = os.listdir(PATH_TO_FILES)

doc_list = []

for file in tqdm(files):

  doc = Document()
  doc.load_from_json(PATH_TO_FILES + file)

  if doc not in doc_list:
    doc_list.append(doc)
  else:
    print("Jummmmmm")
