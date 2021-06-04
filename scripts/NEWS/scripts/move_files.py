import os
import shutil
from tqdm import tqdm

SRC_FOLDER = "/media/nicolas-rocha/FOTOS/NLP/anciano/news_anciano/files/"
DST_FOLDER = "/media/nicolas-rocha/FOTOS/NLP/files/"

LANG = ["fr", "en", "es"]


for lang in LANG:

  src = SRC_FOLDER + lang + '/'
  dst = DST_FOLDER + lang + '/'

  files = os.listdir(src)

  for file in tqdm(files):

    shutil.move(os.path.join(src, file), dst)

