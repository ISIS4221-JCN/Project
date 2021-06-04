
PATH_TO_FILES = "/media/nicolas-rocha/FOTOS/NLP/files/es/"
PATH_TO_CSV = "/media/nicolas-rocha/FOTOS/NLP/dicts/es/"


import os

import csv

csv_files = os.listdir(PATH_TO_CSV)

i = 0
j = 0

id_list = []

for csv_file in csv_files:

  with open(PATH_TO_CSV + csv_file, "r") as fcsv:

    csv_reader = csv.reader(fcsv, delimiter=',')

    for row in csv_reader:
      
      if row[0] not in id_list:
        id_list.append(row[0])
      else:
        try:
          os.remove(PATH_TO_FILES + row[1])
        except FileNotFoundError as e:
          pass
        j+= 1

      i += 1

      print("Found {} documents. Removed {} duplicates".format(i, j), end="\r")
