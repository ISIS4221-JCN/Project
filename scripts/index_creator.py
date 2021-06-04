import concurrent.futures
import numpy as np
import os, json, nltk, random, time, string, argparse
from tqdm import tqdm

class IndexCreator:

    def __init__(self, args):
        self.BERT_embeddings_news = os.listdir(os.path.join(args.path, 'embeddings_BERT', 'news', args.lang))
        self.BERT_embeddings_reddit = os.listdir(os.path.join(args.path, 'embeddings_BERT', 'reddit', args.lang))
        self.BERT_embeddings_tweets = os.listdir(os.path.join(args.path, 'embeddings_BERT', 'tweets', args.lang))
        self.D2V_embeddings = os.listdir(os.path.join(args.path, 'embeddings_D2V', args.lang))

    def main(self, args):
        sources = ['tweets', 'reddit', 'news']
        emb_files_dict = {}
        file_names = []
        for source in sources:
            file_names += os.listdir(os.path.join(args.path, source, args.lang))[:30]
        for file in tqdm(file_names):
            bert_path = self.find_bert_embedding(file, args)
            d2v_path = self.find_d2v_embedding(file, args)
            emb_files_dict[file] = {'bert': bert_path, 'd2v': d2v_path}
        with open(os.join.path(args.path, 'emb_index' + str(args.lang) + '.json')) as index_file:
            json.dump(emb_files_dict, index_file)

    def find_bert_embedding(self, file, args):
        source = file[:2]

        sources_dict = {'TW': self.BERT_embeddings_tweets, 'RE': self.BERT_embeddings_reddit,
                        'tw': self.BERT_embeddings_tweets, 'GO': self.BERT_embeddings_news}

        path_dict = {'TW': os.path.join(args.path, 'embeddings_BERT', 'tweets', args.lang),
                    'RE': os.path.join(args.path, 'embeddings_BERT', 'reddit', args.lang),
                    'tw': os.path.join(args.path, 'embeddings_BERT', 'tweets', args.lang),
                    'GO': os.path.join(args.path, 'embeddings_BERT', 'news', args.lang)}

        for emb_file in sources_dict[source]:
            with open(os.path.join(path_dict[source], emb_file)) as emb_file_txt:
                emb_dict = json.load(emb_file_txt)
                if file in emb_dict:
                    emb_file_name = os.path.join('embeddings_BERT', 'tweets', args.lang, emb_file)
                    break
        return emb_file_name

    def find_d2v_embedding(self, file, args):
        for emb_file in self.D2V_embeddings:
            with open(os.path.join(args.path, 'embeddings_D2V', args.lang, emb_file)) as emb_file_txt:
                emb_dict = json.load(emb_file_txt)
                if file in emb_dict:
                    emb_file_name = os.path.join('embeddings_D2V', args.lang, emb_file)
                    break
        return emb_file_name

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='/media/juan/Juan/NLP/')
    parser.add_argument('--lang', type=str, default='es')
    args = parser.parse_args()
    index_creator_object = IndexCreator(args)
    index_creator_object.main(args)
