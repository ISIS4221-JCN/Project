
# Sets the path to file
path_to_files = "/media/nicolas-rocha/FOTOS/NLP/files/fr/"

import os

from tqdm import tqdm

import json

from zipfile import ZipFile


files = os.listdir(path_to_files)

for file in tqdm(files):

  if file.endswith(".zip"):

    # Opens zip file
    zip_file = ZipFile(path_to_files + file, "r")

    # Gets full path inside file
    fname = zip_file.namelist()[0]

    # Gets data from file
    data = zip_file.read(fname)

    # Defines json file
    data = json.loads(data)

    # Replaces .zip to .json
    file = file.replace(".zip", ".json")

    # Creates the full JSON path
    json_path = path_to_files + file

    # Dumps to file
    with open(json_path, "w") as fp:
      json.dump(data, fp, indent=4)
