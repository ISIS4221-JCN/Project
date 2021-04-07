import requests
import os
import json
import time

from progress.bar import ChargingBar, Bar

def remove_duplicates(dir='/NLP/en', by='id'):
    # Retrieve docs from directory
    docs = os.listdir(dir)

    # Look for duplicated docs
    print('Looking for duplicated docs...')
    duplicated_docs = []

    # Bar to visualize progress
    progress_bar = Bar('Progreso: ', max=len(docs))

    # Extract key for doc to compare
    for i, doc in enumerate(docs):
        key = None
        with open(dir+'/'+doc) as json_file:
            data = json.load(json_file)
            key = data[by]

        # Extract key from following docs to compare
        for j, next_doc in enumerate(docs[i+1:-1]):
            next_key = None
            with open(dir+'/'+next_doc) as json_file:
                data = json.load(json_file)
                next_key = data[by]

            # If keys are the same, save the duplicated doc
            if key == next_key:
                duplicated_docs.append(next_doc)
                break
        # Next step
        progress_bar.next()

    # Print number of duplicated docs
    progress_bar.finish()
    print('Found {} duplicated docs!'.format(len(duplicated_docs)))

    # Remove duplicated duplicated docs
    print('Removing duplicated docs...')

    for doc in duplicated_docs:
        print(doc)
        #os.remove(dir+'/'+doc)

def main():
    # Remove duplicates from EN folder
    remove_duplicates(dir='./reddit/es')
    # Remove duplicates from ES folder
    #remove_duplicates(dir='/NLP/es')
    # Remove duplicates from FR folder
    #remove_duplicates(dir='/NLP/fr')

if __name__ == "__main__":
    main()
