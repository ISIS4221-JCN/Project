from tqdm import tqdm
import os, json, argparse

def main(path):
    docs = os.listdir(path)
    purged_docs = []
    for doc in docs:
        if doc.split('_')[0] == 'TUMBLR':
            continue
        else:
            purged_docs.append(doc)

    for doc in tqdm(purged_docs):
        with open(path + '/' + doc, 'r') as file:
            tweet = json.load(file)
            tweet['id'] = tweet['url'].split('/')[-1]
        with open(path + '/' + doc, 'w') as file:
            json.dump(tweet, file, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='/media/juan/Juan/NLP/')
    parser.add_argument('--lang', type=str, default='en')
    args = parser.parse_args()
    args.path = args.path + args.lang
    main(args.path)
