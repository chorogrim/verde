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


# parser.add_argument(변수 이름, type=bool,str,int.., default = 입력을 하지 않았을 때,
# 어떻게 기본적으로 부여가 되는지 기본값들을 말해줌, help = 잘못 입력하거나, 어떤 변수들이
# 있는지 보고 싶을 때 * bool= 파이썬 자료형 파일, int = 숫자형, str = 문자열)

parser = argparse.ArgumentParser()
parser.add_argument('--site_openapi', type=str, default="http://aiopen.etri.re.kr:8000/WiseNLU_spoken", help='<ETRI OPEN API의 사이트 주소를 입력하세요>')
parser.add_argument('--site_papago', type=str, default="https://openapi.naver.com/v1/papago/n2mt", help='<PAPAGO API 의 사이트 주소를 입력하세요>')
parser.add_argument('--code', type=str, default="ner", help='<ETRI OPEN API에서 요청할 코드를 설정해주세요(default:ner)>')
parser.add_argument('--encoding_type', type=str, default="cp949", help='<NER분석은 되었지만 번역은 되지 않은 파일의 인코딩 타입을 입력하세요>')

parser.add_argument('--src_lang', type=str, default="ko", help='<번역할 언어를 설정해 주세요(default: ko)>')

parser.add_argument('--tar_langs', type=str, default="en,zh-CN,ja", help='<어떤 언어로 번역할 지를 설정해줍니다(쉼표로 분리, default:en,zh-CN,ja)>')

parser.add_argument('--key_file', type=str, default="/home1/ncloud/chorog/hasstudio/api_token.json", help='<API KEY가 저장되어 있는 경로를 설정해주세요>')
parser.add_argument('--input_file', type=str, default="/home1/ncloud/chorog/hasstudio/txt.data/data6.txt", help='<NER을 실행하고 번역을 할 데이터를 입력해주세요>')
parser.add_argument('--processed_file', type=str, default="./data/kimchungup!.csv", help='<NER분석은 되었지만 번역은 되지 않은 파일의 경로를 설정해주세요>')
parser.add_argument('--output_file', type=str, default="./result#.csv", help='<최종 결과를 저장할 경로를 설정해주세요>')
parser.add_argument('--do_ner', type=bool, default=True, help='<NER을 실행할 지를 설정해주세요(default:True)>')
parser.add_argument('--ignore_header', type=bool, default=True, help='<NER분석은 되었지만 번역은 되지 않은 파일을 읽어올 때 header(첫줄)을 읽어올지 설정해주세요>')
parser.add_argument('--num_cores', type=int, default=None, help='<멀티프로세싱을 위해 CPU CORE의 개수를 설정해주세요>')
parser.add_argument('--max_sen_len', type=int, default=1000, help='<NER을 할 문장의 최대 길이를 설정해주세요(default:1000)>')
parser.add_argument('--ner_types', type=str, default="AF_BUILDING,PS_NAME,OGG_ART,OGG_MEDICINE,OGG_LIBRARY,AF_CULTURAL_ASSET,OGG_ECONOMY,OGG_HOTEL,CV_BUILDING_TYPE,EV_WAR_REVOLUTION,EV_ACTIVITY,TR_SOCIAL_SCIENCE,TR_ART,LC_TOUR,AFW_ART_CRAFT,TM_SHAPE,EV_FESTIVAL", help='<NER을 실행후 추출할 태그를 설정해주세요(쉼표로 구분)>')
parser.add_argument('--ner_types_first', type=str, default="LC,PS,FD,TR,AF,OGG,LCP,LCG,CV,DT,EV,", help='<NER을 실행후 추출할 상위 태그를 설정해주세요(쉼표로 구분)>')



def read_json_key(path):
    '''
    param : 
        path : json키의 경로
        
    output : 
        ACESS KEY : ETRI API KEY
        CLIENT_ID :  NAVER PAPAGO API KEY
        CLIENT_SECRET : NAVER PAPAGO API KEY
    '''
    with open(path, 'r', encoding='utf-8') as r:
        content = json.load(r)
    return content["ACCESS"], content["CLIENT_ID"], content["CLIENT_SECRET"]


def read_words(path, encoding='cp949', ignore_header=True):
    '''
     param : 
        path : 미리 ner 처리된 단어의 csv file 경로
        encoding : encoding method
        ignore_header : header(csv의 첫줄)를 읽어올 것인가를 설정
        
    output : 
        return : 읽어온 csv 파일 중  단어 list
    '''
    with open(path, 'r', encoding=encoding) as r:
        contents = csv.reader(r)
        contents = [c[1] for c in contents]
    if ignore_header:
        contents = contents[1:]
    return contents


def preprocessing(text):
    '''
    param : 
        text : 전처리의 대상이 되는 문자열(str)
    
    output : 
        texts : 전처리가 적용된 문자열 list
    
    '''

    # 전처리가 필요한 경우 여기에 추가로 작성
    if isinstance(text, str):                                      # text를 개행으로 분리
        text = text.splitlines()                                   # 빈 이중 list를 만들어 줌
    texts = [[]]
    for t in text:
        if 1000 < len(' '.join(texts[-1])):                        # 문장 list의 문자열을 합한 총길이가 1000보다 크면
            texts.append([texts[-1].pop()])                        # 마지막 문장을 뽑아서 다음 빈 list에 추가
        texts[-1].append(t)                                        # 문장 list에 문장 t를 추가
    texts = [''.join(t) for t in texts if t]                       # list 내 문장 list를 결합(1000자 미만)
    texts = list(compress(texts, texts))                           # list 내 문자열 중 ''를 제거
    return texts


def read_text_by_lines(path):
    '''
    param : 
        path : ner을 진행할 파일의 경로를 입력
    output :
        sentences : processing 함수가 적용된 문자열 list
    '''
    _, ext = os.path.splitext(path)                                 # 이름과 경로를 분리
    if ext == '.txt':                                               # 만약 '.txt.data file 이면..'
        with open(path, encoding='utf-8') as f:               
            sentences = preprocessing(f.read())
    elif ext == '.xlsx':                                            # 만약 './xlsx file 이면..'
        df = pd.read_excel(path)                                    # pandas를 이용해 읽어옴
        sentences = preprocessing(df['contents'].tolist())          # content열에 있는 데이터를 preprocessing함
    elif ext == '.csv':                                             # 만약 '.csv file 이면..'
        df = pd.csv(path)                                           # pandas를 이용해 읽어옴
        sentences = preprocessing(df['contents'].tolist())
    else:                                                           # 아니면 error
        raise ValueError                                            # raise는 에러를 일부러 발생시키는 기능을 해서
    return sentences                                                # 정의되지 않은 형식의 파일을 넣으면 에러가 발생


def ner_chk(text, open_api_url, access_key, anly_code, ner_types, ner_types_first):  # 외부에서 받아오게끔 ner_chk를 변경(parser.add_argument에서 받게끔 변경)
    '''
    params:
        text : ner 분석을 할 text
        open_api_url : OPEN API url 값
        access_key : OPEN API KEY 값
        anal_code : OPEN API에서 분석 KEY(기본:ner)
        ner_types : NER 분석 후 저장하고자 하는 ner 태그 list
    output:
        data : 분석된 결과를 저장한 list
    '''
    
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
    data = json.loads(response.data.decode("utf-8"))['return_object']['sentence'][0]['NE']         # json.loads 로 response의 데이터를 json형식으로 불러옴(dictionary). 읽어온 데이터의 'return_object' > 'sentence' > 0 > 'NE' 를 추출 하여 data로 정의
    print('results: ',data)
    data = [d for d in data if isinstance(d['text'], str)]
    data = [d['text'] for d in data if (d['type'] in ner_types) or d['type'].split('_')[0] in ner_types_first]      # 데이터의 타입(type)이 ner_type에 있고 d['text']가 문자열이면 해당 d['text']를 list의 원소로 함
    return data if data else []                                                                    # 만약 data가 있으면 그대로, 없으면 빈list를 반환


def translate(word, req, tar_lang='en'):
    '''
    param : 
    word : 번역 할 단어
    req : PAPAGO와 관련하여 생성한 request
    tar_lang : 타깃 언어(번역의 결과가 되는 언어)
     output : 
        API 호출 결과값
     '''
    data = f"source=ko&target={tar_lang}&text={parse.quote(word)}"
    response = request.urlopen(req, data=data.encode("utf-8"))
    if response.getcode() == 200:
        return json.loads(response.read())['message']['result']['translatedText']
    else:
        print("Error Code:" + response.getcode())

 # total = [ko_list, en_list, ch_list, ja_list]
def save_csv(path, dic_words, encoding='utf-8', languages='ko,en,zh-CN,ja', header='NO, Noun_KR, Noun_EN, Noun_CH, Noun_JA \n'):
    '''
    결과물을 ko,en,zh-CN,ja 이 순서대로 번역된 결과를 csv file로 저장하는 함수
     
    params:
        path : 저장하고자 하는 경로
        dic_words : (언어, 번역결과)가 각각 KEY,VALUE 으로 저장된 dict
        encoding : 저장하고자 하는 파일의 encoding option
        languages : 저장하고자 하는 언어를 쉼표로 구분하여 표시한 문자열
        header: 번역 결과의 header(열 이름)를 표시한 문자열 (쉼표로 구분)
    output:
        None (경로에 파일 저장)
        csv format file save
            csv header : 
                NO : 
                Noun_KR : 한국어 단어
                Noun_EN : 영어 단어
                Noun_CH : 중국어 단어
                Noun_JA : 일본어 단어 
    '''
   
    total = [dic_words[lang] for lang in languages.split(',')]
    with open(path, 'w', encoding=encoding) as w:
        w.write(header)
        for i, words in enumerate(zip(*total)):
            w.write(f'{i+1},{",".join(words)}\n')                     # join 함수를 통해서 ,를 각 데이터 사이에 추가                            


def run_imap_multiprocessing(func, argument_list, num_processes):
    '''
     params:
        func : 멀티프로세싱을 적용 할 함수(ner_chk 함수)
        argument_list : 멀티프로세싱을 적용 할 대상(list)
        num_processes : 하나의 처리 유닛
     output:
        result_list_tqdm : func가 적용된 argument_list 
        argument_list = [a,b,c,d] >> func가 적용된 argument_list: [func(a), func(b), func(c), func(d)]
     '''   
    pool = Pool(processes=num_processes)                              # processes는 동시에 처리할 작업의 개수(하드웨어의 cpu core 개수보다 적어야 함)
    result_list_tqdm = []                                             # 빈 list를 만듦
    for result in pool.imap(func=func, iterable=argument_list):       # list의 각 원소에 대하여 병렬적으로 함수를 적용
        result_list_tqdm.append(result)                               # func = 적용 대상, iterble = 적용 할 함수
    return result_list_tqdm


if __name__ == '__main__':                                            
    start = time.time()                                               # 속도 측정을 위한 코드 (시작부분)
    args = parser.parse_args() 
    ACCESS, ID, SECRET = read_json_key(args.key_file)                 # 입력 파일 경로, 출력 파일 경로

    if args.do_ner:                                                   # 입력 언어, 츨력 언어(,로 구분)
        assert os.path.isfile(args.input_file), f'There is no file on the path; {args.input_file}'
        src_words = []
        for sw in read_text_by_lines(args.input_file):                # 텍스트가 저장된 list에 대해서 for문을 반복
            result = ner_chk(sw, open_api_url=args.site_openapi, access_key=ACCESS,
                                 anly_code=args.code, ner_types=args.ner_types.split(','), ner_types_first=args.ner_types_first.split(','))
            print('result:',result)
            src_words+=result
        src_words = list(set(src_words))
        print('results of NER:', src_words)
    else:
        assert os.path.isfile(args.processed_file), f'There is no file on the path; {args.processed_file}'
        src_words = read_words(path=args.processed_file,              # 기존 ner처리가 된 단어들을 읽어옴
                               encoding=args.encoding_type,
                               ignore_header=args.ignore_header)

    req = request.Request(args.site_papago)                           # request를 선언하고 header를 추가
    req.add_header("X-Naver-Client-Id", ID)
    req.add_header("X-Naver-Client-Secret", SECRET)

    output = {k: [] for k in args.tar_langs.split(',')}               # 타깃 언어('en','zh-CN','ja')를 키로 빈 리스트를 값으로 하는 dict를 만듦
    num_cores = args.num_cores if args.num_cores else cpu_count()
                                                                      # 타깃 언어 별로 반복
    for lang in args.tar_langs.split(','):                            # 멀티프로세싱으로 코드가 실행
        '''                                                           # 번역 함수를 선언. partial을 통해 translate의 word를 제외한 나머지 변수를 고정한 새로운 함수를 func라 정의
        partial 함수 사용
        - 함수를 만들어 넘길 때 자주 사용
        
        def sum(a,b)
            print(a+b)
         
        f = partial(sum,20)
        f(1)
        >> 21
        '''      
        func = partial(translate, req=req, tar_lang=lang)                                   # request, tar_lang 미리 설정해두는 함수 = partial
        output[lang] += run_imap_multiprocessing(func, src_words, num_processes=num_cores)  # 각 단어(src_words)에 대하여 (for 루프의) 'lang'에 대응되는 언어로 번역(멀티 프로세싱)
                                                                                            # 이후, output dic에 lang 키에 해당되는 값(초기에는 빈 list)에 번역된 값(list)를 더함
    output[args.src_lang] = src_words                                                       # 한국어(번역 전 문장)를 추가
    save_csv(args.output_file, output)                                                      # output file로 저장
    print(f'[{num_cores}-CORES]실행 시간(초):{time.time()-start}')                           # 속도 측정을 위한 코드 (끝 부분)
                                                                                            # 1-cores로 했을 때 29초 정도 나오고, 8-cores로 했을 때 20초 정도 나옴 