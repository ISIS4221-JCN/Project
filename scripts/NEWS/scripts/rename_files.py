
path_to_files = "/media/nicolas-rocha/FOTOS/NLP/files/es/"

import os

from tqdm import tqdm

files = os.listdir(path_to_files)

for file in tqdm(files):

  if file.endswith(".zip"):

    new_file = file.replace(".zip", ".json")

    os.rename(path_to_files + file, path_to_files + new_file)
