import requests
import os
import json
import time
import argparse
import numpy as np

from progress.bar import ChargingBar, Bar

def remove_duplicates(args, by='text'):

    # Setting paths
    path_to_remove = '../resources/repeated_files'+args.lang+'.npy'
    dir = args.path

    # Retrieve docs from directory
    docs = sorted(os.listdir(dir))
    duplicated_docs = []

    # Set variables with warm start
    if args.warm_start:
        duplicated_docs = np.load(path_to_remove).tolist()
        last = duplicated_docs[-1]
        docs = docs[docs.index(last):]

    # Look for duplicated docs
    print('Looking for duplicated docs...')

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
                np.save(path_to_remove, np.array(duplicated_docs))
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
        # os.remove(dir+'/'+doc)

def main(args):
    # Remove duplicates from EN folder
    remove_duplicates(args)
    # Remove duplicates from ES folder
    #remove_duplicates(dir='/NLP/es')
    # Remove duplicates from FR folder
    #remove_duplicates(dir='/NLP/fr')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='/media/juan/Juan/NLP/')
    parser.add_argument('--lang', type=str, default='es1')
    parser.add_argument('--warm_start', type=bool, default=False)
    args = parser.parse_args()
    args.path = args.path + args.lang
    main(args)
