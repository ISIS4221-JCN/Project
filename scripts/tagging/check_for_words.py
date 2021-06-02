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

    words_dict_violence = {'es': ['violencia intrafamiliar', 'intrafamiliar'],
                          'en': ['household violence', 'intrafamily', 'domestic violence'],
                          'fr': ['violence intrafamiliale', 'violence domestique']}

    words_dict_vaccine = {'es': ['vacuna', 'vacunacion', 'vacunación', 'pfizer', 'astrazeneca', 'inmunización', 'inmunizacion'],
                          'en': ['vaccine', 'vaccination', 'pfizer', 'astrazeneca', 'inmunization'],
                          'fr': ['vaccin', 'vaccination', 'pfizer', 'astrazeneca', 'inmuinisation']}

    words_dict_mental = {'es': ['suicidio', 'mental', 'esquizofrenia', 'paranoia', 'paranoico', 'deprimido', 'depresión', 'deprimida'],
                         'en': ['suicide', 'mental', 'esquizofrenia', 'paranoia', 'paranoid', 'depressed', 'depression'],
                         'fr': ['suicide', 'mentale', 'schizophrénie', 'paranoïa', 'paranoïaque', 'déprimée', 'déprimé', 'dépression']}

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

def show_some_files(args):
    matching_files = main(args)
    files_list = random.sample(matching_files, args.num_files)
    path = os.path.join(args.path, args.source, args.lang)
    for file in files_list:
            with open(os.path.join(path, file), 'r+') as file_str:
                data_dict = json.load(file_str)
                print(data_dict['text'])
    return matching_files

def tag_data(args):
    matching_files = show_some_files(args)
    codes_dict = {'vaccine': [1,0,0,0,0], 'schools': [0,0,1,0,0], 'violence': [0,0,0,1,0], 'mental': [0,1,0,0,0]}
    pos_dict = {'vaccine': 0, 'schools': 2, 'violence': 3, 'mental': 1}
    tags_dict = {}
    labels = ['vaccine', 'mental-health', 'school-reopneing', 'household-violence', 'none']
    tag_file_name = args.source  + '_' + args.lang + '_words.json'
    exists =os.path.exists(tag_file_name)
    print(exists)
    if not (exists):
        for file in matching_files:
            tags_dict[file] = dict(zip(labels, codes_dict[args.topic]))
        with open(tag_file_name, 'w+') as tag_file:
            json.dump(tags_dict, tag_file)
    else:
        with open(tag_file_name, 'r') as tag_file:
            tags_dict = json.load(tag_file)
        for file in matching_files:
            if file in tags_dict:
                tags_dict[file][labels[pos_dict[args.topic]]] = True
            else:
                tags_dict[file] = dict(zip(labels, codes_dict[args.topic]))
        with open(tag_file_name, 'w') as tag_file:
            json.dump(tags_dict, tag_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='/media/juan/Juan/NLP/')
    parser.add_argument('--source', type=str, default = 'tweets')
    parser.add_argument('--lang', type=str, default='es')
    parser.add_argument('--topic', type=str, default = 'violence')
    parser.add_argument('--num_files', type=int, default = 5)
    args = parser.parse_args()
    tag_data(args)
