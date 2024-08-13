import os
import pandas as pd
import argparse

def labeling_file(label_path, sorted_list, file_path, file_format):
    labeling = pd.read_excel(label_path)
    labeling['combined'] = labeling['file name'].astype(str) + '_' + labeling['type'].astype(str) + '_' + labeling['axis'].astype(str) #라벨링된 항목들을 병합
    labeling_list = labeling['combined'].tolist() 
    for idx in range(len(sorted_list)):
        old_name = sorted_list[idx]
        new_name = labeling_list[idx] #라벨링된 파일명으로 변경
        old_file = os.path.join(file_path, old_name)
        labeled_file = os.path.join(file_path, new_name+file_format)
        os.rename(old_file, labeled_file)
    return 

parser = argparse.ArgumentParser()
parser.add_argument("-data", dest="data_path", action="store", default="data_ko")
parser.add_argument("-caption", dest="cap_path", action="store", default="cap_ko")
parser.add_argument("-title", dest="tit_path", action="store", default="tit_ko")
parser.add_argument("-labeling", dest="labeling_path", action="store")
args = parser.parse_args()

if not args.labeling_path: 
    #라벨링 파일이 없다면 생성
    data = {'file name': range(1,101), #라벨링 범위
        'type': ['4'] * 100, #차트유형 * 범위
        'axis': ['0'] * 100} #차트방향 * 범위
    df = pd.DataFrame(data)
    df.to_excel('labeling.xlsx') #경로 지정
    label_path = 'labeling.xlsx'
else:
    label_path = args.labeling_path

data_list = [file for file in os.listdir(args.data_path)]
cap_list = [file for file in os.listdir(args.cap_path)]
tit_list = [file for file in os.listdir(args.tit_path)]
#img_path = 'image path'
#img_list = [file for file in os.listdir(img_path)]


sorted_data_list = sorted(data_list, key=lambda x: int(x.split('.')[0])) #순서대로 정렬
sorted_cap_list = sorted(cap_list, key=lambda x: int(x.split('.')[0])) #순서대로 정렬
sorted_tit_list = sorted(tit_list, key=lambda x: int(x.split('.')[0])) #순서대로 정렬
  
labeling_file(label_path, sorted_data_list, args.data_path, 'csv')
labeling_file(label_path, sorted_cap_list, args.cap_path, '.txt')
labeling_file(label_path, sorted_tit_list, args.tit_path, '.txt')

