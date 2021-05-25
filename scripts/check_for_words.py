import os, json, argparse
from tqdm import tqdm
import concurrent.futures
import numpy as np
import os, json, nltk, random, time, string
from tqdm import tqdm

def main(args):
    """ Function to check if words exist in tweets data in specified language

    Args:
        args (dict): dict containing script arguments
    """
    # Dictionaries with words to find in tweets
    words_dict_schools = {'es': ['colegios', 'colegio', 'reapertura', 'educacion', 'profesores', 'estudiantes'],
                          'en': ['school', 'schools', 'reopening', 're-opening', 'teachers', 'teach', 'education'],
                          'fr': ['école', 'écoles', 'réouverture', 'enseignants', 'enseignant', 'apprendre', 'éducation']}

    words_dict_violence = {'es': ['violencia', 'intrafamiliar', 'agresion', 'irrespeto'],
                          'en': ['violence', 'household violence', 'agression', 'disrespect', 'intrafamily'],
                          'fr': ['intrafamiliale', 'violence', 'manque de respect', 'agression']}

    words_dict_vaccine = {'es': ['vacuna', 'vacunacion', 'vacunación', 'pfizer', 'astrazeneca', 'inmunización', 'inmunizacion'],
                          'en': ['vaccine', 'vaccination', 'pfizer', 'astrazeneca', 'inmunization'],
                          'fr': ['vaccin', 'vaccination', 'pfizer', 'astrazeneca', 'inmuinisation']}

    # Cases to choose word_dict
    if args.topic == 'schools':
        words_dict = words_dict_schools
    elif args.topic == 'vaccine':
        words_dict = words_dict_vaccine
    else:
        words_dict = words_dict_violence

    # Function for the threads to exceute
    def chunk_diver(path, files, words):
        matching_files = []
        for file in tqdm(files):
            with open(os.path.join(path, file), 'r+') as file_str:
                data_dict = json.load(file_str)
                text = data_dict['text']
                for word in words:
                    if word in text.lower():
                        matching_files.append(file)
                        break
        return matching_files

    # Divide files in number of threads
    path = os.path.join(args.path, args.source, args.lang)
    files_list = os.listdir(path)
    lists = np.array_split(files_list, 10)

    start = time.time()
    matching_files_all = []
    print("Starting threads to search documents")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        # Deploy threads
        for files_list in lists:
            futures.append(executor.submit(chunk_diver, path, files_list, words_dict[args.lang]))
        for future in concurrent.futures.as_completed(futures):
            matching_files_all = matching_files_all + future.result()
    # Print results
    elapsed_time = time.time() - start
    print('Took {} seconds to exceute script'.format(elapsed_time))
    print('Found {} matching files'.format(len(matching_files_all)))
    return matching_files_all

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='/media/juan/Juan/NLP/')
    parser.add_argument('--source', type=str, default = 'tweets')
    parser.add_argument('--lang', type=str, default='es')
    parser.add_argument('--topic', type=str, default = 'violence')
    args = parser.parse_args()
    main(args)
