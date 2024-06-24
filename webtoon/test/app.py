from flask import Flask, request, jsonify, render_template
from PIL import Image
import pytesseract
import cv2
import numpy as np


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


app = Flask(__name__)

# Tesseract의 경로 설정 (Windows에서만 필요)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ocr_core(img):
    """
    이 함수는 이미지에서 텍스트를 추출합니다.
    """
    text = pytesseract.image_to_string(img, lang='kor')
    return text

def extract_text_with_coords(image_path):
    """
    이미지에서 텍스트와 해당 좌표를 추출합니다.
    """
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 컨투어 찾기
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    data = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        roi = img[y:y + h, x:x + w]
        text = pytesseract.image_to_string(roi, lang='kor').strip()
        if text:
            data.append({
                'text': text,
                'x': x,
                'y': y,
                'w': w,
                'h': h
            })

    return data

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        img = Image.open(file.stream)
        img.save("./uploaded_image.png")
        
        ocr_data = extract_text_with_coords("./uploaded_image.png")
        
        # 데이터 품질 확인 (여기서는 단순히 텍스트가 존재하는지 확인)
        data_quality = []
        for item in ocr_data:
            if item['text']:  # 텍스트가 존재하면 데이터 품질이 양호하다고 판단
                item['quality'] = 'Good'
            else:
                item['quality'] = 'Poor'
            data_quality.append(item)
        
        return jsonify(data_quality)

if __name__ == '__main__':
    app.run(debug=True)