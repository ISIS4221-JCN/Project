import requests
import os
import json
import time

def remove_duplicates(dir='/NLP/en', by='id'):
    # Retrieve docs from directory
    docs = os.listdir(dir)

    # Look for duplicated docs
    print('Looking for duplicated docs...')
    duplicated_docs = []

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

    print('Found {} duplicated docs!'.format(len(duplicated_docs)))


def main():
    # Remove duplicates from EN folder
    remove_duplicates(dir='./reddit/fr')
    # Remove duplicates from ES folder
    #remove_duplicates(dir='/NLP/es')
    # Remove duplicates from FR folder
    #remove_duplicates(dir='/NLP/fr')

if __name__ == "__main__":
    main()
