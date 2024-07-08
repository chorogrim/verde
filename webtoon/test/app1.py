import os
import easyocr
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename


# Flask 애플리케이션 생성
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# EasyOCR Reader 객체 생성 (GPU 사용)
reader = easyocr.Reader(['ko', 'en'], gpu=True)

# 업로드 폴더가 없으면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def upload_form(): # 업로드된 파일 처리
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
    try:
        if 'file' not in request.files: # file이 포함되어 있지 않은 경우
            return redirect(request.url) # 현재 url로 재요청하여 업로드 폼을 다시 표시
        file = request.files['file'] # 요청에서 file 가져오기
        if file.filename == '': # 파일 이름이 빈 문자열인 경우
            return redirect(request.url) # 현재 url로 재요청
        if file: # 파일이 존재하는 경우
            filename = secure_filename(file.filename) # secure_filename 함수를 사용하여 안전한 파일 이름 생성
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename) # 파일의 저장 경로 생성
            file.save(filepath) # 파일을 해당 경로에 저장
            
            # OCR 처리
            results = reader.readtext(filepath)
            
            # 이미지에 텍스트와 위치 표시
            image = Image.open(filepath)
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype("./batang.ttc", 20)  # 원하는 폰트로 지정
            
            for (bbox, text, prob) in results:
                p0, p1, p2, p3 = [tuple(coord) for coord in bbox] # 바운딩 박스의 각 좌표를 튜플로 반환
                draw.polygon([p0, p1, p2, p3], outline="green") # 바운딩 박스의 좌표를 따라 녹색으로 텍스트 표현
                draw.text(p0, text, fill="purple", font=font) # 바운딩 박스의 첫 번째 좌표에 ocr로 인식된 텍스트를 보라색으로 표현
            
            result_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result_' + filename) # 결과 이미지를 저장할 경로 생성
            image.save(result_image_path) # 이미지를 해당 경로에 저장
            
            return render_template('result.html', results=results, image_url=result_image_path) # result_html 템플릿을 렌더링하여 반환
        
    except Exception as e: # 오류 떴을 때 예외처리
        app.logger.error(f"Error processing the image: {e}")
        return "An error occurred while processing the image.", 500

if __name__ == "__main__":
    app.run(port=5001, debug=True)
