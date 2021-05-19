import os, json, argparse
from tqdm import tqdm

def remove_duplicates(args):
    docs = sorted(os.listdir(args.path + args.lang))
    print('Found {} documents...'.format(len(docs)))

    text = {}
    for doc in tqdm(docs):
        with open(args.path + args.lang + '/' + doc) as file:
            tweet = json.load(file)
        text[doc] = tweet['text']

    print('Loaded {} documents...'.format(len(text)))
    print('Looking for reapeted files...')
    to_remove = []
    for key1 in tqdm(list(text.keys())):
        for key2 in list(text.keys()):
            if not(key1 == key2):
                if text[key1] == text[key2]:
                    to_remove.append(key2)
    to_remove = set(to_remove)
    print('Found {} repeated documents...'.format(len(to_remove)))

    counter = 0
    for doc in to_remove:
        os.remove(args.path + args.lang + '/' + doc)
        counter += 1
    print('Removed {} documents...'.format(counter))

    remaining_docs = len(os.listdir(args.path + args.lang))

    print('{} remaining documents...'.format(remaining_docs))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='/media/juan/Juan/NLP/Tweets/')
    parser.add_argument('--lang', type=str, default='es')
    args = parser.parse_args()
    remove_duplicates(args)
