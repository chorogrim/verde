#!/usr/bin/env python
# coding: utf-8

# In[3]:


pip install easyocr


# In[20]:


import easyocr
import matplotlib.pyplot as plt
import cv2

# EasyOCR 리더 객체 생성 (한국어와 영어 설정)
reader = easyocr.Reader(['ko', 'en'])

# 이미지 파일 경로
image_path = './image2.jpg'

# 이미지 읽기
image = cv2.imread(image_path)

# 텍스트 추출
results = reader.readtext(image_path)

# 추출된 텍스트 출력

for (bbox, text, prob) in results:
    print(f'Text: {text}, Probability: {prob}')
    
    # 바운딩 박스 좌표 추출
    (top_left, top_right, bottom_right, bottom_left) = bbox
    top_left = tuple([int(val) for val in top_left])
    bottom_right = tuple([int(val) for val in bottom_right])

    # 바운딩 박스 그리기
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

    # 텍스트 표시
    cv2.putText(image, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

# 이미지 출력
plt.figure(figsize=(10, 10))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()


# In[25]:


import easyocr
import cv2
import os

# EasyOCR 리더 객체 생성 (한국어와 영어 설정)
reader = easyocr.Reader(['ko', 'en'])

def extract_text_to_text_file(image_path, output_text_path):
    # 이미지 읽기
    image = cv2.imread(image_path)
    
    # 텍스트 추출
    results = reader.readtext(image_path)
    
    # 텍스트 파일에 저장
    with open(output_text_path, 'w', encoding='utf-8') as f:
        for (bbox, text, prob) in results:
            f.write(f'Text: {text}\n')
            f.write(f'Bounding Box: {bbox}\n')
            f.write(f'Probability: {prob}\n')
            f.write('\n')
    
    print(f"Extracted data saved to {output_text_path}")

# 예제 사용법
image_path = './image2.jpg'
output_text_path = './output.txt'

extract_text_to_text_file(image_path, output_text_path)


# In[7]:


pip install easyocr pillow


# In[37]:


import easyocr
from PIL import Image, ImageDraw, ImageFont

# EasyOCR Reader 객체 생성
reader = easyocr.Reader(['ko', 'en'], gpu=False)

# 이미지 파일 경로
image_path = './image8.jpg'

# 이미지 로드
image = Image.open(image_path)

# OCR 처리
results = reader.readtext(image_path)

# 이미지에 텍스트와 위치 표시
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("./batang.ttc", 50)  # 원하는 폰트를 지정하세요.


for (bbox, text, prob) in results:
    # bbox는 사각형의 좌표를 포함합니다. [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    # Pillow의 polygon 함수는 리스트가 아닌 튜플을 받아야 합니다.
    p0, p1, p2, p3 = [tuple(coord) for coord in bbox]
    draw.polygon([p0, p1, p2, p3], outline="green")
    draw.text(p0, text, fill="purple", font=font)

# 결과 이미지 저장
output_path = './result_image.jpg'
image.save(output_path)

# 결과 이미지 보기
image.show()


# In[ ]:




