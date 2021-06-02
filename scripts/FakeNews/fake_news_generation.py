import pandas as pd
import argparse, json, os, random
from tqdm import tqdm
from transformers import pipeline, set_seed
import zipfile
import torch

model_dict = {'en': 'gpt2',
              'es': 'datificate/gpt2-small-spanish',
              'fr': 'dbddv01/gpt2-french-small'}

def main(args):
    device = torch.device("cuda")
    print(device)
    generator = pipeline('text-generation', model=model_dict[args.lang],device=0,framework='pt')
    set_seed(args.seed)
    if not args.backwards:
        counter = len(os.listdir(os.path.join(args.path, 'FakeNews', args.lang)))
        counter = 15377
        real_news_names = sorted(os.listdir(os.path.join(args.path, 'news' , args.lang + '/')))[counter:]
    else:
        counter = len(os.listdir(os.path.join(args.path, 'news', args.lang)))
        real_news_names = sorted(os.listdir(os.path.join(args.path, 'news' , args.lang + '/')))
    for file in tqdm(real_news_names):
        with open(os.path.join(args.path, 'news' , args.lang, file), encoding='utf-8') as opened_file:
            news = json.load(opened_file)
            base_text = ''
            if 'title' in news:
                base_text = base_text + news['title'] + '. '
            base_text = base_text + news['text'].split('. ')[0] + '. '
            base_text = news['title'] + '. '
            genereated = generator(base_text,  max_length=args.max_length + random.randint(0, 50) , num_return_sequences=1, pad_token_id=50256)
            text = genereated[0]['generated_text']

            fake_news_dict = {'source': 'Generated Fake News',
                        'lang': args.lang,
                        'author': model_dict[args.lang],
                        'text': text}

            file = open(os.path.join(args.path, 'FakeNews', args.lang, 'fake_' + str(counter) + '.json'), 'w+', encoding='utf-8')
            json.dump(fake_news_dict, file, indent=4)
            file.close()
            counter += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='/media/juan/Juan/NLP/')
    parser.add_argument('--counter', type=int, default=0)
    parser.add_argument('--lang', type=str, default='es')
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--max_length', type=int, default=300)
    parser.add_argument('--backwards', type=bool, default=False)
    args = parser.parse_args()
    main(args)
