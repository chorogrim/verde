from flask import Flask, request, jsonify, render_template, Response
from PIL import Image
import pytesseract
import cv2
import numpy as np
import json


# Tesseract의 경로 설정 (Windows에서만 필요)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Flask 애플리케이션 객체 생성
app = Flask(__name__)

def ocr_core(img):
    """
    이미지를 입력으로 받아 텍스트를 추출
    """
    text = pytesseract.image_to_string(img, lang='kor') # 이미지에서 한국어 텍스트 추출
    return text # 추출된 텍스트를 반환

def extract_text_with_coords(image_path):
    """
    이미지 파일 경로를 입력으로 받아 텍스트와 해당 좌표를 추출
    """
    img = cv2.imread(image_path) # 이미지를 읽어옴
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 이미지를 회색조로 변환
    blur = cv2.GaussianBlur(gray, (5, 5), 0) # 노이즈를 줄이기 위해 이미지를 가우시안 블러 처리
    ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) # 이미지 이진화 수행

    # 컨투어(윤곽선) 찾기
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # 이진화된 이미지에서 컨투어 찾기

    data = [] # 텍스트와 좌표 정보를 저장할 리스트

    for contour in contours: # 각 컨투어에 대해 반복
        x, y, w, h = cv2.boundingRect(contour) # 컨투어의 경계 상자 계산
        roi = img[y:y + h, x:x + w] # 경계 상자 내부의 관심 영역을 추출
        text = pytesseract.image_to_string(roi, lang='kor').strip() # roi에서 텍스트를 추출
        if text: # 텍스트가 존재하는 경우
            data.append({ # 데이터를 리스트에 추가
                'text': text,
                'x': x,
                'y': y,
                'w': w,
                'h': h
            })
            # # 경계 상자 그리기
            # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return data

@app.route('/')
def home(): # 홈페이지 요청을 처리
    return render_template('index.html') # 템플릿을 렌더링하여 응답으로 반환

@app.route('/upload', methods=['POST']) # 파일 업로드 요청을 처리하는 url 경로 지정
def upload_file(): # 파일 업로드 요청을 처리
    if 'file' not in request.files: # 요청에 파일이 포함되어 있는지 확인
        return jsonify({'error': 'No file part'}) # 파일이 없으면 오류 메시지를 json 형태로 반환

    file = request.files['file'] # 업로르된 파일 가져옴
    if file.filename == '': # 파일이 선택되지 않았는지 확인
        return jsonify({'error': 'No selected file'}) # 파일이 선택되지 않았으면 오류 메시지를 json 형태로 반환

    if file: # 파일이 존재하면 처리
        img = Image.open(file.stream) # 업로드된 파일을 이미지로 열기
        img.save("./uploaded_image.png") # 이미지 저장
        
        ocr_data = extract_text_with_coords("./uploaded_image.png") # 이미지에서 텍스트와 좌표 추출
        
        # 데이터 품질 확인 
        data_quality = [] 
        for item in ocr_data: # 각 추출된 데이터 항목에 대해 반복
            if item['text']:  # 텍스트가 존재하면 
                item['quality'] = 'Good' # 데이터 품질을 good으로 설정
            else: # 텍스트가 존재하지 않다면
                item['quality'] = 'Poor' # 데이터 품질을 poor로 설정
            data_quality.append(item) # 데이터 품질 정보를 리스트에 추가
        
        response = Response(json.dumps(data_quality, ensure_ascii=False), content_type='application/json; charset=utf-8') # 한글을 포함한 비아스키 코드가 올바르게 인코딩
        return response

if __name__ == '__main__':
    app.run(debug=True)
