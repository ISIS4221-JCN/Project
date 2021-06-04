


import os

import glob

from bs4 import BeautifulSoup

from document import Document

def process_data(data):

  # Creates the return list
  document_text = []

  # Iterates over elements data
  for element in data:

    # Checks that element is not an empty string
    if element.text != "" or len(element.text.split(" ")) > 1:

      # Appends to text list
      document_text.append(element.text)

  # Returns the text lists
  return document_text


def extract_html_data(filename, document):

  # Extracts HTML
  soup = BeautifulSoup(document.text, 'html5lib')

  # Extracts text from relevant elements
  document_text = process_data(soup.find_all("p"))

  # Checks the amount of text
  if not len(document_text) > 0:

    # Attempts to prcess data from spans
    document_text = process_data(soup.find_all("span"))

  # Checks the amount of text again
  if not len(document_text) > 0:

    # Discards document if still empty
    os.remove(filename)

  # Saves processed document
  else:

    # Creates the text
    text_str = ""

    # Appends text
    text_str = text_str.join(document_text)

    # Stores text
    document.text = text_str

    # Strips .zip from JSON
    filename = filename.replace(".zip", "")

    # Saves file
    document.dump_to_json(filename)

