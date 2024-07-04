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
font = ImageFont.truetype("./batang.ttc", 50)  # 원하는 폰트를 지정

for (bbox, text, prob) in results:
    # bbox는 사각형의 좌표를 포함 [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    # Pillow의 polygon 함수는 리스트가 아닌 튜플
    p0, p1, p2, p3 = [tuple(coord) for coord in bbox]
    draw.polygon([p0, p1, p2, p3], outline="green")
    draw.text(p0, text, fill="purple", font=font)

# 결과 이미지 저장
output_path = './result_image.jpg'
image.save(output_path)

# 결과 이미지 보기
image.show()



