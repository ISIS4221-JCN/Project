
import os

languages = ["fr"]

path_to_files = "/media/nicolas-rocha/FOTOS/NLP/files/"

for lang in languages:
  print("For language {} there are {} files.".format(
    lang,
    len(os.listdir(path_to_files + lang + "/"))
  ))

print("There are {} context files".format(len(os.listdir("./context/"))))