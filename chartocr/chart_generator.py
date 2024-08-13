import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os
import math
import re
import plotly.io as pio
import natsort 
import argparse

def get_title(txt_file):
  try:
    with open(txt_file, 'r', encoding='cp949')as fp:
      title = fp.read()
  except UnicodeDecodeError:
    with open(txt_file, 'r', encoding='utf-8')as fp:
      title = fp.read()
  return title

def extract_info(csv_file):
  without_extension = csv_file.split('.')[0]
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

def sorting_values(df, column):
  pattern1 =  r'\d{4}년 \d+월' #ex. 2018년 3월
  pattern2 = r'\d{4}년 \d+분기' #ex. 2018년 3분기
  pattern3 = r"Q[1-4]\ '\d{2}" #ex. Q3'17

  if any(re.search(pattern1, value) for value in df[str(column)]):
    try:
        df[['Year', 'Month']] = df[str(column)].str.extract(r"(\d{4})년 (\d+)월")  # 'Year'와 'Month' 열 추출 및 생성
        df['Year'] = df['Year'].apply(lambda x: int(x))  # 'Year' 열을 숫자로 변환
        df['Month'] = df['Month'].apply(lambda x: int(x))  # 'Month' 열을 숫자로 변환
        df.sort_values(['Year', 'Month'], ascending=True, inplace=True)  # 'Year'와 'Month' 열을 기준으로 정렬
        df.reset_index(drop=True, inplace=True)
        sorted_df = df.drop(['Year', 'Month'], axis=1)
        return sorted_df
    except ValueError:
      df[['Year', 'Month']] = df[str(column)].str.extract(r"(\d{4})년 (\d+)월")  # 'Year'와 'Month' 열 추출 및 생성
      df['Year'] = df['Year'].fillna(0)  # NaN 값을 0으로 대체
      df['Year'] = df['Year'].apply(lambda x: int(x))  # 'Year' 열을 숫자로 변환
      df['Month'] = df['Month'].fillna(0)  # NaN 값을 0으로 대체
      df['Month'] = df['Month'].apply(lambda x: int(x))  # 'Month' 열을 숫자로 변환
      df.sort_values(['Year', 'Month'], ascending=True, inplace=True)  # 'Year'와 'Month' 열을 기준으로 정렬
      df.reset_index(drop=True, inplace=True)
      sorted_df = df.drop(['Year', 'Month'], axis=1)
      return sorted_df
  elif any(re.search(pattern2, value) for value in df[str(column)]):
    try:
        df[['Year', 'Quarter']] = df[str(column)].str.extract(r"(\d{4})년 (\d+)분기")  # 'Year'와 'Quarter' 열 추출 및 생성
        df['Year'] = df['Year'].apply(lambda x: int(x))  # 'Year' 열을 숫자로 변환
        df['Quarter'] = df['Quarter'].apply(lambda x: int(x))  # 'Quarter' 열을 숫자로 변환
        df.sort_values(['Year', 'Quarterh'], ascending=True, inplace=True)  # 'Year'와 'Quarter' 열을 기준으로 정렬
        df.reset_index(drop=True, inplace=True)
        sorted_df = df.drop(['Year', 'Quarter'], axis=1)
        return sorted_df
    except ValueError:
      df[['Year', 'Quarter']] = df[str(column)].str.extract(r"(\d{4})년 (\d+)분기")  # 'Year'와 'Quarter' 열 추출 및 생성
      df['Year'] = df['Year'].fillna(0)  # NaN 값을 0으로 대체
      df['Year'] = df['Year'].apply(lambda x: int(x))  # 'Year' 열을 숫자로 변환
      df['Quarter'] = df['Quarter'].apply(lambda x: int(x))  # 'Quarter' 열을 숫자로 변환
      df.sort_values(['Year', 'Quarterh'], ascending=True, inplace=True)  # 'Year'와 'Quarter' 열을 기준으로 정렬
      df.reset_index(drop=True, inplace=True)
      sorted_df = df.drop(['Year', 'Quarter'], axis=1)
      return sorted_df
  elif any(re.search(pattern3, value) for value in df[str(column)]):
    try:
      df[['Quarter', 'Year']] = df[str(column)].str.extract(r"(Q[1-4]) '(\d{2})")  # 'Quarter'와 'Year' 열 추출 및 생성
      df['Year'] = df['Year'].apply(lambda x: int(x))  # 'Year' 열을 숫자로 변환
      df.sort_values(['Year', 'Quarter'], ascending=True, inplace=True)  # 'Year'와 'Quarter' 열을 기준으로 정렬
      df.reset_index(drop=True, inplace=True)
      sorted_df = df.drop(['Year', 'Quarter'], axis=1)
      return sorted_df
    except ValueError:
      df[['Quarter', 'Year']] = df[str(column)].str.extract(r"(Q[1-4]) '(\d{2})")  # 'Quarter'와 'Year' 열 추출 및 생성
      df['Year'] = df['Year'].fillna(0)  # NaN 값을 0으로 대체
      df['Year'] = df['Year'].apply(lambda x: int(x))  # 'Year' 열을 숫자로 변환
      df.sort_values(['Year', 'Quarter'], ascending=True, inplace=True)  # 'Year'와 'Quarter' 열을 기준으로 정렬
      df.reset_index(drop=True, inplace=True)
      sorted_df = df.drop(['Year', 'Quarter'], axis=1)
      return sorted_df
  else:
          #print(f"No match found for value:")
          return df

def get_input(df, ori):
#chart classify(simple이면 0, multi이면 1)

  classify_type = 'simple'
  if len(df.columns) > 2:
     classify_type = 'multi'
  #x, y input(x축:value, 축:label)
  if classify_type == 'simple': #simple chart 경우
    if ori =='1':#차트 방향이 '가로'
      x_val = df.columns[1]
      y_val = df.columns[0]
      if df[str(x_val)].astype(str).str.contains('%').any():
        df[str(x_val)] = df[str(x_val)].str.replace('%', '')  # % 기호 제거
        x_val = x_val
    #차트 방향이 '세로' 혹은 or line,pie, table의 기본형
    else: #(x축:label, 축:value)
      x_val = df.columns[0]
      y_val = df.columns[1]

  else:#multi chart의 경우(classification_type = 'multi')
    if ori =='1' :#차트 방향이 '가로'
        y_val = df.columns[0] #x축
        x_val = []
        for idx in range(1, len(df.columns)): #y축 값
          val =df.columns[idx]
          if df[str(idx)].astype(str).str.contains('%').any():
            df[str(idx)]= df[str(idx)].str.replace('%', '')
            x_val.append(str(val))
          else:
            x_val.append(str(val))
    else:#차트 방향이 '세로' 혹은 or line,pie, table의 기본형
        x_val = df.columns[0] #x축
        y_val = []
        for idx in range(1, len(df.columns)): #y축 값
          val =df.columns[idx]
          if df[str(idx)].astype(str).str.contains('%').any():
            df[str(idx)]= df[str(idx)].str.replace('%', '')
            y_val.append(str(val))
          else:
            y_val.append(str(val))
  return classify_type, x_val, y_val

def axes_range(input_list):
    #기존 최솟값, 최댓값
    old_min = min(input_list)
    old_max = max(input_list)
    #새로운 최솟값,최댓값 선언 (범주용)
    new_min = 0
    new_max = 0
    # 소수인 경우
    if isinstance(old_min, float) or isinstance(old_max, float):
      int_min = math.floor(old_min )
      int_max = math.ceil(old_max )
      try:
          min_digits = int(math.log10(abs(int_min)))
      except ValueError:
          min_digits = 0
      try:
          max_digits = int(math.log10(abs(int_max)))
      except ValueError:
          max_digits = 0
      new_min = old_min
      if max_digits == 0 and old_max < 5:
        new_max = 5
      elif max_digits == 0 and old_max >5:
        new_max = 10
      else:
        new_max = (int(int_max / (10 ** max_digits)) + 1) * (10 ** max_digits)
      return(new_min, new_max)
    else:
        #로그오류 경우
        try:
          min_digits = int(math.log10(abs(old_min)))
        except ValueError:
            min_digits = 0
        try:
            max_digits = int(math.log10(abs(old_max)))
        except ValueError:
            max_digits = 0

        # digits가 모두 0인 경우
        if min_digits == 0 and max_digits == 0:
          if old_min < 0 :  # 음수/0인 경우
            #old_min = -1
            #new_min = (int(old_min / (10 ** min_digits))) * (10 ** (min_digits+1))
            new_min = old_min
            if old_max < 0 or old_max == 0:
              new_max = 0
            else:
              new_max = 10
          elif old_min == 0:
            new_min = 0
            if old_max < 0 or old_max == 0:
              new_max = 0
            else:
              new_max = 10
          else:
            new_min = old_min
            if old_max < 0 or old_max == 0:
              new_max = 0
            else:
              new_max = 10

        elif min_digits != 0 and max_digits == 0:
          new_min = (int(old_min / (10 ** min_digits)) -1 ) * (10 ** (min_digits))
          if old_max < 0 or old_max == 0:
            new_max = 0
          else:
            new_max = 10


        elif min_digits == 0 and max_digits != 0:
          if old_min < 0:  # 음수/0인 경우
            new_min = old_min
            new_max = (int(old_max / (10 ** max_digits)) +1 ) * (10 ** (max_digits))
          elif old_min == 0:
            new_min = 0
            new_max = (int(old_max / (10 ** max_digits)) +1 ) * (10 ** (max_digits))
          else:
            new_min = old_min
            new_max = (int(old_max / (10 ** max_digits)) +1 ) * (10 ** (max_digits))

        else:# min_digits != 0 and max_digits != 0
          new_min = (int(old_min / (10 ** min_digits)) -1 ) * (10 ** (min_digits))
          new_max = (int(old_max / (10 ** max_digits)) +1 ) * (10 ** (max_digits))

        return(new_min, new_max)
    
def remove_special_characters(range_list):
  removed_chr  =[]
  removed_checkpoint = 0
  for val in range_list:
    if isinstance(val, str) and '%' in val:
      try:
        val = int(val.replace('%', ''))  # % 기호 제거
        removed_chr.append(val)
        removed_checkpoint = 1
      except ValueError: #소수인 경우
        val = float(val.replace('%', ''))  # % 기호 제거
        removed_chr.append(val)
        removed_checkpoint = 1
    elif isinstance(val, list) and '%' in val:
      try:
        val = int(val.replace('%', ''))  # % 기호 제거
        removed_chr.append(val)
        removed_checkpoint = 1
      except ValueError: #소수인 경우
        val = float(val.replace('%', ''))  # % 기호 제거
        removed_chr.append(val)
    else:
      try:
        val = int(val)
        removed_chr.append(val)
      except ValueError: #문자만 있는 경우
        val = 0
        removed_chr.append(val)
  return removed_chr, removed_checkpoint

parser = argparse.ArgumentParser()
parser.add_argument("-data", dest="data_path", action="store", default="/Users/angsubeng/Downloads/Chart2text_datasets/data_ko/")
parser.add_argument("-title", dest="tit_path", action="store", default="/Users/angsubeng/Downloads/Chart2text_datasets/tit_ko/")
args = parser.parse_args()

csv_list = natsort.natsorted([file for file in os.listdir(args.data_path)])
err_list = []

#output 경로 생성(bar-1, line-2, pie-3, table-4)

output_bar = args.data_path+'bar'
if not os.path.exists(output_bar):
    os.mkdir(args.data_path+'bar') #폴더 생성
output_line = args.data_path+'line'
if not os.path.exists(output_line):
    os.mkdir(args.data_path+'line') #폴더 생성
output_pie = args.data_path+'pie'
if not os.path.exists(output_pie):
    os.mkdir(args.data_path+'pie') #폴더 생성
output_table = args.data_path+'table'
if not os.path.exists(output_table):
    os.mkdir(args.data_path+'table') #폴더 생성


for csv_file in csv_list:
  csv_path = f'{args.data_path}{str(csv_file)}'
  txt_path1 = f'{args.tit_path}{str(csv_file)}'
  txt_path = os.path.splitext(txt_path1)[0]+'.txt'
  img_name = os.path.splitext(csv_file)[0]

  try:
    df = pd.read_csv(csv_path, encoding='cp949')
    encoding_method = 'cp949'
  except UnicodeEncodeError:
    df = pd.read_csv(csv_path, encoding='utf-8')
    encoding_method = 'utf-8'
  except pd.errors.EmptyDataError:
    err_list.append(csv_file)
    pass
  try:
    title = get_title(txt_path)
    c_type, ori, mode = extract_info(csv_file) #c_type: 차트 유형, ori:방향, mode: 차트 모드
    print(csv_file)
    classify_type, x_val, y_val= get_input(df, ori)

    if (
          not os.path.exists(f"{output_bar}/{img_name}")
          or not os.path.exists(f"{output_line}/{img_name}")
          or not os.path.exists(f"{output_pie}/{img_name}")
          or  not os.path.exists(f"{output_table}/{img_name}")):

      if c_type =='1':#bar
        if classify_type =='simple':
              #axes_range 파악
            if ori =='1':
                sorted_df = sorting_values(df, y_val) #정렬
                range_list=sorted_df[str(x_val)].tolist()
                new_min, new_max = axes_range(range_list)
                chart = go.Bar(x=sorted_df[str(x_val)], y=sorted_df[str(y_val)],orientation='h')
                layout = go.Layout(title=title)
                fig = go.Figure(data=chart, layout=layout)
                fig.update_xaxes(range=[new_min, new_max])
                #fig.show()
                fig.update_layout( font=dict({'family':'nanum'}))
                fig.update_traces(text=df[str(x_val)], textposition='outside', textfont=dict(color='black'))
                pio.write_image(fig, f"{output_bar}/{img_name}", engine="kaleido", format="png")
            else:
              sorted_df = sorting_values(df, x_val) #정렬
              range_list=sorted_df[str(y_val)].tolist()
              new_min, new_max = axes_range(range_list)
              chart = go.Bar(x=sorted_df[str(x_val)], y=sorted_df[str(y_val)])
              layout = go.Layout(title=title)
              fig = go.Figure(data=chart, layout=layout)
              fig.update_yaxes(range=[new_min, new_max])
              fig.update_layout( font=dict({'family':'nanum'}))
              fig.update_traces(text=df[str(y_val)], textposition='outside', textfont=dict(color='black'))
              pio.write_image(fig, f"{output_bar}/{img_name}", engine="kaleido", format="png")
      elif c_type =='3':
        sorted_df = sorting_values(df, x_val) #정렬
        fig = px.pie(sorted_df, values=y_val, names=x_val, title=title)
        fig.show()#차트 시각
        fig.update_layout( font=dict({'family':'nanum'}))
        pio.write_image(fig, f"{output_pie}/{img_name}", engine="kaleido", format="png")
      elif c_type =='4':
        if classify_type =='simple':
            sorted_df = sorting_values(df, x_val) #정렬
            layout = go.Layout(title=title)
            fig = go.Figure(layout=layout)
            fig.add_trace(go.Table(header = dict(values=[x_val,y_val]),
              cells = dict(values=[sorted_df[str(x_val)],sorted_df[str(y_val)]])))
            fig.update_layout( font=dict({'family':'nanum'}))
            pio.write_image(fig, f"{output_table}/{img_name}", engine="kaleido", format="png")


  except IndexError:
    err_list.append(csv_file)
    pass
  except TypeError:
    err_list.append(csv_file)
    pass
  except ValueError:
    err_list.append(csv_file)
    pass

'''
except TypeError:
err_list.append(csv_file)
pass
except ValueError:
err_list.append(csv_file)
pass
except KeyError:
err_list.append(csv_file)
pass
except FileNotFoundError:
err_list.append(csv_file)
pass
'''

#t생성한 이미지 수
print(5000-len(err_list))
# 빈 DataFrame 생성
err_df = pd.DataFrame(columns=['err_idx'])
# 리스트 요소를 하나씩 셀에 넣기
for i, value in enumerate(err_list):
    err_df.loc[i, 'err_idx'] = value
# DataFrame 출력
#print(err_df)
err_df.to_csv('err_output.csv', index=False)
