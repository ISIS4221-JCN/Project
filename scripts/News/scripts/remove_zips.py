path_to_files = "/media/nicolas-rocha/FOTOS/NLP/files/fr/"

import os

from tqdm import tqdm

files = os.listdir(path_to_files)

for file in tqdm(files):

  if file.endswith(".zip"):

    os.remove(path_to_files + file)