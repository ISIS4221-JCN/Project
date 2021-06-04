# Sets the path to file
path_to_files = "/media/nicolas-rocha/FOTOS/NLP/files/en/"

# Imports OS to generate an iterator
import os 

from tqdm import tqdm

# Imports document
from document import Document

# Imports the processing function
from extract_html_data import extract_html_data

# Imports ThreadPoolExecutor
import concurrent.futures

# Gets the glob iterator
files = os.listdir(path_to_files)

# Iterates over files
for file in tqdm(files):

  if file.endswith(".json"):
    continue

  # Creates a document instance
  doc = Document()

  # Loads file from ZIP
  doc.load_from_json(path_to_files + file)

  # Processes data
  extract_html_data(path_to_files + file, doc)
