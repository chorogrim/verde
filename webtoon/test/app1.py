import os
import easyocr
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from threading import Thread

# Flask 애플리케이션 생성
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# EasyOCR Reader 객체 생성
reader = easyocr.Reader(['ko', 'en'], gpu=False)

# 업로드 폴더가 없으면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def upload_form():
    return render_template('./index.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # OCR 처리
        results = reader.readtext(filepath)
        
        # 이미지에 텍스트와 위치 표시
        image = Image.open(filepath)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("./batang.ttc", 20)  # 원하는 폰트를 지정하세요.
        
        for (bbox, text, prob) in results:
            p0, p1, p2, p3 = [tuple(coord) for coord in bbox]
            draw.polygon([p0, p1, p2, p3], outline="green")
            draw.text(p0, text, fill="purple", font=font)
        
        result_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result_' + filename)
        image.save(result_image_path)
        
        return render_template('./result.html', results=results, image_url=result_image_path)

# Flask 애플리케이션을 백그라운드 스레드에서 실행
def run_flask():
    app.run(port=5000, debug=False)

flask_thread = Thread(target=run_flask)
flask_thread.start()