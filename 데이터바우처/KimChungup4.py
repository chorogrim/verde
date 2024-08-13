from itertools import compress
from urllib3 import PoolManager
from multiprocessing import Pool
from urllib import request, parse
import json
import argparse
import csv
import time
from functools import partial
from os import cpu_count, path
import re

parser = argparse.ArgumentParser()
parser.add_argument('--site_openapi', type=str, default="http://aiopen.etri.re.kr:8000/WiseNLU_spoken", help='<변수에 대한 설명을 넣어주세요>')
parser.add_argument('--site_papago', type=str, default="https://openapi.naver.com/v1/papago/n2mt", help='<변수에 대한 설명을 넣어주세요>')
parser.add_argument('--code', type=str, default="ner", help='<변수에 대한 설명을 넣어주세요>')
parser.add_argument('--encoding_type', type=str, default="cp949", help='<변수에 대한 설명을 넣어주세요>')

parser.add_argument('--src_lang', type=str, default="ko", help='<변수에 대한 설명을 넣어주세요>')

parser.add_argument('--tar_langs', type=str, default="en,zh-CN,ja", help='<변수에 대한 설명을 넣어주세요>')

parser.add_argument('--key_file', type=str, default="./api_token.json", help='<변수에 대한 설명을 넣어주세요>')
parser.add_argument('--input_file', type=str, default="./txt.data/data1.txt", help='<변수에 대한 설명을 넣어주세요>')
parser.add_argument('--processed_file', type=str, default="./data/kimchungup!.csv", help='<변수에 대한 설명을 넣어주세요>')
parser.add_argument('--output_file', type=str, default="./results/result.csv", help='<변수에 대한 설명을 넣어주세요>')

parser.add_argument('--do_ner', type=bool, default=True, help='<변수에 대한 설명을 넣어주세요>')
parser.add_argument('--ignore_header', type=bool, default=True, help='<변수에 대한 설명을 넣어주세요>')
parser.add_argument('--num_cores', type=int, default=None, help='<변수에 대한 설명을 넣어주세요>')
parser.add_argument('--max_sen_len', type=int, default=1000, help='<변수에 대한 설명을 넣어주세요>')
parser.add_argument('--ner_types', type=str, default="AF_BUILDING,PS_NAME,OGG_ART", help='<변수에 대한 설명을 넣어주세요>')



def read_json_key(path):
    with open(path, 'r', encoding='utf-8') as r:
        content = json.load(r)
    return content["ACCESS"], content["CLIENT_ID"], content["CLIENT_SECRET"]


def read_words(path, encoding='cp949', ignore_header=True):
    with open(path, 'r', encoding=encoding) as r:
        contents = csv.reader(r)
        contents = [c[1] for c in contents]
    if ignore_header:
        contents = contents[1:]
    return contents


def preprocessing(text):
    text = text.splitlines()
    texts = [[]]
    for t in text:
        if 1000 < len(' '.join(texts[-1])):
            texts.append([texts[-1].pop()])
        texts.append(t)
    texts = [''.join(t) for t in texts if t]
    texts = list(compress(texts, texts))
    return texts


def read_text_by_lines(path):
    with open(path, encoding='utf-8') as f:
        sentences = preprocessing(f.read())
    return sentences


def ner_chk(text, open_api_url, access_key, anly_code, ner_types):
    req_json = {
        "access_key": access_key,
        "argument": {
            "text": text,
            "analysis_code": anly_code
        }
    }

    response = PoolManager().request(
        "POST",
        open_api_url,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(req_json)
    )
    data = json.loads(response.data.decode("utf-8"))['return_object']['sentence'][0]['NE']
    data = [d['text'] for d in data if d['type'] in ner_types and isinstance(d['text'], str)]
    return data if data else []


def translate(word, req, tar_lang='en'):
    data = f"source=ko&target={tar_lang}&text={parse.quote(word)}"
    response = request.urlopen(req, data=data.encode("utf-8"))
    if response.getcode() == 200:
        return json.loads(response.read())['message']['result']['translatedText']
    else:
        print("Error Code:" + response.getcode())


def save_csv(path, dic_words, encoding='utf-8', languages='ko,en,zh-CN,ja', header='NO,명사,Noun,名詞,めいし\n'):
    total = [dic_words[lang] for lang in languages.split(',')]
    with open(path, 'w', encoding=encoding) as w:
        w.write(header)
        for i, words in enumerate(zip(*total)):
            w.write(f'{i+1},{",".join(words)}\n')


def run_imap_multiprocessing(func, argument_list, num_processes):
    pool = Pool(processes=num_processes)
    result_list_tqdm = []
    for result in pool.imap(func=func, iterable=argument_list):
        result_list_tqdm.append(result)
    return result_list_tqdm


if __name__ == '__main__':
    start = time.time()
    args = parser.parse_args()
    ACCESS, ID, SECRET = read_json_key(args.key_file)

    if args.do_ner:
        assert path.isfile(args.input_file), f'There is no file on the path; {args.input_file}'
        src_words = []
        for sw in read_text_by_lines(args.input_file):
            src_words += ner_chk(sw, open_api_url=args.site_openapi, access_key=ACCESS,
                                 anly_code=args.code, ner_types=args.ner_types.split(','))
        src_words = list(set(src_words))
    else:
        assert path.isfile(args.processed_file), f'There is no file on the path; {args.processed_file}'
        src_words = read_words(path=args.processed_file,
                               encoding=args.encoding_type,
                               ignore_header=args.ignore_header)
    req = request.Request(args.site_papago)
    req.add_header("X-Naver-Client-Id", ID)
    req.add_header("X-Naver-Client-Secret", SECRET)

    output = {k: [] for k in args.tar_langs.split(',')}
    num_cores = args.num_cores if args.num_cores else cpu_count()

    for lang in args.tar_langs.split(','):
        func = partial(translate, req=req, tar_lang=lang)
        output[lang] += run_imap_multiprocessing(func, src_words, num_processes=num_cores)

    output[args.src_lang] = src_words
    save_csv(args.output_file, output)
    print(time.time()-start)


