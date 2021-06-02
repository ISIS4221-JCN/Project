path_to_files = "/media/nicolas-rocha/FOTOS/NLP/juan/fr/"

import os

from tqdm import tqdm

from document import Document

files = os.listdir(path_to_files)

for file in tqdm(files):

  try:
    doc = Document()
    doc.load_from_json(path_to_files + file)
  except:
    os.remove(path_to_files + file)
