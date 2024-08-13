import os
import shutil
import argparse

def get_title(txt_file):
  try:
    with open(txt_file, 'r', encoding='cp949')as fp:
      title = fp.read()
  except UnicodeDecodeError:
    with open(txt_file, 'r', encoding='utf-8')as fp:
      title = fp.read()
  return title

def extract_info(file):
  without_extension = file.split('.')[0]
  split_elements = without_extension.split("_")
  info_num = len(split_elements)
  # 유형, 방향, 모드 지정
  if info_num == 4:
      c_type, ori, mode = split_elements[1:]
  elif info_num == 3:
      c_type, ori = split_elements[1:]
      mode = None  # 모드는 None으로 지정 또는 원하는 기본값 설정
  else:
      c_type = split_elements[1]
      ori= None
      mode = None
  return c_type, ori, mode

def path_creating(base_path):
    dst_path = {
        'bar': f'{base_path}/bar/',
        'line': f'{base_path}/line/',
        'pie': f'{base_path}/pie/',
        'table': f'{base_path}/table/'
    }
    for path in dst_path.values():
        os.makedirs(path, exist_ok=True)
    return dst_path

def saving_new_path(file_list, src_path, dst_path):
  for file in file_list:
    file_path = f'{src_path}/{file}'
    c_type, ori, mode = extract_info(file)  # c_type: 차트 유형, ori: 방향, mode: 차트 모드

    if c_type == '1':  # bar
        if ori == '1':
            src = file_path
            dst = dst_path['bar']
            shutil.move(src, dst)
    elif c_type == '2':  # line
        src = file_path
        dst = dst_path['line']
        shutil.move(src, dst)
    elif c_type == '3':  # pie
        src = file_path
        dst = dst_path['pie']
        shutil.move(src, dst)
    elif c_type == '4':  # table
        src = file_path
        dst = dst_path['table']
        shutil.move(src, dst)
  return

parser = argparse.ArgumentParser()
parser.add_argument("-data", dest="d_path", action="store", default="data_ko")
parser.add_argument("-caption", dest="c_path", action="store", default="cap_ko")
parser.add_argument("-title", dest="t_path", action="store", default="tit_ko")
parser.add_argument("-image", dest="i_path", action="store", default="image")
parser.add_argument("-root", dest="root_path", action="store")
args = parser.parse_args()

data_path = f'{args.root_path}/{args.d_path}'
cap_path = f'{args.root_path}/{args.c_path}'
tit_path = f'{args.root_path}/{args.t_path}'
img_path = f'{args.root_path}/{args.i_path}'

data_list = [file for file in os.listdir(data_path)]
cap_list = [file for file in os.listdir(cap_path)]
tit_list = [file for file in os.listdir(tit_path)]
img_list = [file for file in os.listdir(img_path)]

dst_data = path_creating(data_path)
dst_cap = path_creating(cap_path)
dst_tit = path_creating(tit_path)
dst_img = path_creating(img_path)

saving_new_path(data_list, data_path, dst_data)
saving_new_path(cap_list, cap_path, dst_cap)
saving_new_path(tit_list, tit_path, dst_tit)
saving_new_path(img_list, img_path, dst_img)



