import numpy as np
import os, json, nltk, random, time
from gensim.parsing.porter import PorterStemmer
from tqdm import tqdm
import concurrent.futures


class Utils:
    def __init__(self, path_prefix, num_workers = 15):
        self.path_prefix = path_prefix
        self.num_workers = num_workers

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
            for file in tqdm(files_list):
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
                            remove_contractions = False,
                            remove_stop_words = False,
                            stemming = False,
                            tonekize = False,
                            lemmatize = False,
                            tweet_tokenizer = False):
        """ Function to apply preprocessing steps to text

        Args:
            text (str): String to preprocess
            remove_contractions (bool): True to apply contractions removal
            remove_stop_words (bool): True to remove stop words
            stemming (bool): True to apply stemming
            tokenize (bool): True to tokenize text
            lemmatize (bool): True to lemmatize
            tweet_tokenizer (bool): True to use nltk tweet tokenizer

        Returns:
            str: Preprocessed string
        """

        if tweet_tokenizer:
            tokenizer = TweetTokenizer(preserve_case=False, reduce_len=True, strip_handles=True)
        else:
            tokenizer = nltk.RegexpTokenizer(r'\w+')

        porter_stemmer = PorterStemmer()
        lemmatizer = nltk.stem.WordNetLemmatizer()

        # Converts to lowercase
        text = text.lower()

        # Replace colloquial terms
        if remove_contractions:
            for word in text.split():
                if word in list(contraction_colloq_dict.keys()):
                    text = text.replace(word, contraction_colloq_dict[word])

        # Removes stopwords
        if remove_stop_words:
            text = remove_stopwords(text)

        # Stems text
        if stemming:
            text = porter_stemmer.stem_sentence(text)

        # Tokenizes text and removes punctuation
        if tokenize:
            text = tokenizer.tokenize(text)

        # Lemmatizes text
        if lemmatize:
            text_lm = []
            for word in text:
               text_lm.append(self.lemmatizer.lemmatize(word))
        text = text_lm

        # Returns preprocessed text
        return text
