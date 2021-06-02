
# Imports the operating system library
import os

# Imports the datetime
from datetime import datetime

# Imports the JSON library
import json
from json.decoder import JSONDecodeError

# Imports the time library
import time

# Imports the Google News API
from pygooglenews import GoogleNews

# Imports the document class
from document import Document

# Imports the URL library
import urllib


def fetch(filepath):

  # Sets the start time
  start_time = time.time()

  # Prints information
  print("INFO: Starting thread for file {}".format(filepath))

  # STAGE 1: Tries to open the parameters file
  try:
    param_file = open(filepath, "r")
  except OSError:
    print("ERROR: Could not open context file!")
    return False

  # STAGE 2: Tries to load the parameters file as JSON
  try:
    search_params = json.load(param_file)
  except Exception:
    print("ERROR: Could not decode JSON file!")
    param_file.close()
    return False

  # STAGE 3: Closes the parameters file
  param_file.close()

  # STAGE 4: Stores the parametes into variables
  lang = search_params["lang"]
  country = search_params["country"]
  start_date = search_params["start_date"]
  stop_date = search_params["stop_date"]
  keyword = search_params["keyword"]

  # STAGE 5: Clears the search parameters
  del search_params

  # STAGE 6: Creates the Google API
  try:
    google_api = GoogleNews(
      lang=lang,
      country=country
    )
  except Exception:
    print("ERROR: Failed to create Google API")
    return False

  # STAGE 7: Calls the Google API
  try:
    response = google_api.search(
      keyword,
      from_=start_date,
      to_=stop_date
    )
  except Exception:
    print("ERROR: Failed to call Google API")
    return False

  # STAGE 7: Retrieves the HTML source and creates the documents
  documents_list = []
  for entry in response["entries"]:

    # Data dictionary to create document object
    document_data = {
      "source": "Google News",
      "lang": lang,
      "date": start_date,
      "author": entry["source"]["title"],
      "url": entry["link"],
      "id": entry["id"],
      "title": entry["title"],
      "keyword": keyword
    }

    # Tries to retrieve the HTML source code
    try:
      html_source = urllib.request.urlopen(document_data["url"], timeout=5).read()
    except Exception as e:
      continue

    # Tries to decode the HTML source code
    try:
      html_source = html_source.decode("utf-8")
    except UnicodeDecodeError:
      html_source = html_source.decode("latin-1")

    # Replaces the quotes with escape characters
    html_source = html_source.replace('"', '\"')

    # Stores the HTML text
    document_data["text"] = html_source

    # Creates the document instance
    document = Document()

    # Loads the document with data
    document.load_from_dict(document_data)

    # Appends to document list
    documents_list.append(document)

  # STAGE 8: Stores the documents
  document_path_prefix = "/media/nicolas-rocha/FOTOS/NLP/files/" + lang + "/"
  for document in documents_list:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%s%f")
    doc_path = document_path_prefix + "GOOGLE_" + timestamp
    document.dump_to_json(doc_path)

  # Correct return for function includes deleting the parent file
  os.remove(filepath)

  # Prints output information
  print("Finished quering file: {}".format(filepath), end=" ")
  print("Took {} seconds for {} documents".format(
    time.time() - start_time,
    len(documents_list)  
  ))

  # Returns True to indicate a correct return
  return True

