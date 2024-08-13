from itertools import compress
from urllib3 import PoolManager
from multiprocessing import Pool
from urllib import request, parse
import json
import argparse
import csv
import time
from functools import partial
from os import cpu_count
import pandas as pd
import os
import re

parser = argparse.ArgumentParser()
parser.add_argument('--site_openapi', type=str, default="http://aiopen.etri.re.kr:8000/WiseNLU_spoken", help='<변수에 대한 설명을 넣어주세요>')
parser.add_argument('--site_papago', type=str, default="https://openapi.naver.com/v1/papago/n2mt", help='<변수에 대한 설명을 넣어주세요>')
parser.add_argument('--code', type=str, default="ner", help='<변수에 대한 설명을 넣어주세요>')
parser.add_argument('--encoding_type', type=str, default="cp949", help='<변수에 대한 설명을 넣어주세요>')

parser.add_argument('--src_lang', type=str, default="ko", help='<변수에 대한 설명을 넣어주세요>')

parser.add_argument('--tar_langs', type=str, default="en,zh-CN,ja", help='<변수에 대한 설명을 넣어주세요>')

parser.add_argument('--key_file', type=str, default="./api_token.json", help='<변수에 대한 설명을 넣어주세요>')
parser.add_argument('--input_file', type=str, default="./00_건축물 정보(단문)_202107_하스스튜디오.xlsx", help='<변수에 대한 설명을 넣어주세요>')
parser.add_argument('--processed_file', type=str, default="./data/kimchungup!.csv", help='<변수에 대한 설명을 넣어주세요>')
parser.add_argument('--output_file', type=str, default="./results/result.csv", help='<변수에 대한 설명을 넣어주세요>')

parser.add_argument('--do_ner', type=bool, default=True, help='<변수에 대한 설명을 넣어주세요>')
parser.add_argument('--ignore_header', type=bool, default=True, help='<변수에 대한 설명을 넣어주세요>')
parser.add_argument('--num_cores', type=int, default=None, help='<변수에 대한 설명을 넣어주세요>')
# 아래 코드는 개체명 인식을 할 문장의 최대 길이 입니다. 1000으로 설정하면 1000보다 커지지 않는 하나의 문자열을 만듭니다(이를 기준으로 개체명 인식을 진행)
parser.add_argument('--max_sen_len', type=int, default=1000, help='<변수에 대한 설명을 넣어주세요>')
# 아래에 분류 코드를 원하시는대로 추가해주세요.
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
    # 전처리가 필요한 경우 여기에 작성해줍니다.
    if isinstance(text, str):
        text = text.splitlines()
    texts = [[]]
    for t in text:
        if 1000 < len(' '.join(texts[-1])):
            texts.append([texts[-1].pop()])
        texts[-1].append(t)
    texts = [''.join(t) for t in texts if t]
    texts = list(compress(texts, texts))
    return texts


def read_text_by_lines(path):
    _, ext = os.path.splitext(path)
    if ext == '.txt':
        with open(path, encoding='utf-8') as f:
            sentences = preprocessing(f.read())
    elif ext == '.xlsx':
        df = pd.read_excel(path)
        sentences = preprocessing(df['contents'].tolist())
    elif ext == '.csv':
        df = pd.csv(path)
        sentences = preprocessing(df['contents'].tolist())
    else:
        raise ValueError
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
    # total = [한국어단어리스트, 영어단어리스트, 중국어단어리스트, 일본어단어리스트] 입니다.
    total = [dic_words[lang] for lang in languages.split(',')]
    with open(path, 'w', encoding=encoding) as w:
        w.write(header)
        for i, words in enumerate(zip(*total)):
            # join 함수를 통해서 ,를 각 데이터 사이에 추가합니다.
            w.write(f'{i+1},{",".join(words)}\n')


def run_imap_multiprocessing(func, argument_list, num_processes):
    pool = Pool(processes=num_processes)
    result_list_tqdm = []
    for result in pool.imap(func=func, iterable=argument_list):
        result_list_tqdm.append(result)
    return result_list_tqdm


if __name__ == '__main__':
    # 속도 측정을 위한 코드입니다
    start = time.time()
    args = parser.parse_args()
    # 입력파일 경로, 출력파일 경로입니다
    ACCESS, ID, SECRET = read_json_key(args.key_file)
    # 입력언어, 출력언어(,로 구분)입니다.

    if args.do_ner:
        # 원본 코드에서도 주석처리되서 실행되지 않았고, 데이터가 없어서 검증하지는 않았습니다.
        # readline_data_txt > read_text_by_lines
        # word_ko_append는 삭제하였습니다.
        assert os.path.isfile(args.input_file), f'There is no file on the path; {args.input_file}'
        src_words = []
        for sw in read_text_by_lines(args.input_file):
            src_words += ner_chk(sw, open_api_url=args.site_openapi, access_key=ACCESS,
                                 anly_code=args.code, ner_types=args.ner_types.split(','))
        src_words = list(set(src_words))
    else:
        # "./data/KimChungup!.csv" 파일을 불러옵니다
        assert os.path.isfile(args.processed_file), f'There is no file on the path; {args.processed_file}'
        src_words = read_words(path=args.processed_file,
                               encoding=args.encoding_type,
                               ignore_header=args.ignore_header)

    # request를 선언하고 header를 추가합니다.
    req = request.Request(args.site_papago)
    req.add_header("X-Naver-Client-Id", ID)
    req.add_header("X-Naver-Client-Secret", SECRET)

    # 타깃 언어('en','zh-CN','ja')를 키로 빈 리스트를 값으로 하는 딕셔너리를 만듭니다.
    output = {k: [] for k in args.tar_langs.split(',')}
    num_cores = args.num_cores if args.num_cores else cpu_count()
    #타깃 언어 별로 반복합니다.

    for lang in args.tar_langs.split(','):
        # 멀티프로세싱으로 코드가 실행됩니다.
        ## 번역 함수를 선언합니다.
        func = partial(translate, req=req, tar_lang=lang)
        ## 각 단어(src_words)에 대하여 (for 루프의) 'lang'에 대응되는 언어로 번역을 합니다(멀티 프로세싱).
        ## 이후, output 딕셔너리에 lang 키에 해당되는 값(초기에는 빈 리스트)에 번역된 값(리스트)를 더합니다.
        output[lang] += run_imap_multiprocessing(func, src_words, num_processes=num_cores)

    # 한국어(번역 전 문장)를 추가합니다.
    output[args.src_lang] = src_words
    # output을 파일로 저장합니다.
    save_csv(args.output_file, output)

    # 속도 비교를 위한 출력입니다(실제 작동시에는 제거하셔도 됩니다.).
    print(time.time()-start)
    # 평균 2.7초입니다(로컬[컴퓨터]환경에 따라 달라질 수 있습니다.)
