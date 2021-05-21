import numpy as np
import os, json, nltk, random, time
from gensim.parsing.porter import PorterStemmer
from tqdm import tqdm
import string
import concurrent.futures
from nltk.tokenize.casual import TweetTokenizer


class Utils:
    def __init__(self, path_prefix, num_workers = 15):
        self.path_prefix = path_prefix
        self.num_workers = num_workers
        self.tweet_tokenizer = TweetTokenizer(preserve_case=False, reduce_len=True, strip_handles=True)

    def data_loader(self, lang, source, total_data=None):
        """ Function to retrieve tweet data in specified language

        Args:
            lang (str): Language to load tweets in [en, es, fr]

        Returns:
            list: tweets list
        """
        start = time.time()
        def chunk_loader(path, files_list):
            data = []
            for file in files_list:
                with open(os.path.join(path, file), 'r+') as file_str:
                    data_dict = json.load(file_str)
                    data.append(data_dict['text'])
            return data

        path = os.path.join(self.path_prefix, source, lang)
        files_list = os.listdir(path)
        if total_data != None:
            files_list = random.sample(files_list, total_data)
        else:
            total_data = len(files_list)
        lists = np.array_split(files_list, self.num_workers)

        data = []
        print("Starting threads to load {} documents from {} in {}".format(total_data, source, lang))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for files_list in lists:
                futures.append(executor.submit(chunk_loader, path, files_list))
            for future in concurrent.futures.as_completed(futures):
                data = data + future.result()
        elapsed_time = time.time() - start

        print("Loaded {} files in {} seconds.".format(len(data), elapsed_time))
        return data

    def preprocessing(self, text,
                        stop_words = None,
                        stemmer = None,
                        tokenizer = None,
                        lemmatizer = None):
        """ Function to apply preprocessing steps to text

        Args:
            text (str): String to preprocess
            stop_words (list): stopwords to remove
            stemmer (nltk.stem): stemmer to be used
            tokenizer (nltk.tokenize): tokenizer to be used


        Returns:
            str: Preprocessed string
        """
        # Stems text
        if stemmer:
            text = stemmer.stem(text)

        # # Converts to lowercase
        text = "".join([char.lower() for char in text if char not in string.punctuation])

        # Removes stopwords
        if tokenizer:
            text = tokenizer.tokenize(text)


        # Lemmatizes text
        relevant_words=[]
        for word in text:
            if word not in stop_words:
                relevant_words.append(word)

        text = relevant_words
        # Returns preprocessed text
        return text
