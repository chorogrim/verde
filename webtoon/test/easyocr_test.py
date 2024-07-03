import easyocr
import matplotlib.pyplot as plt
import cv2

# EasyOCR 리더 객체 생성 (한국어, 영어로 설정)
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
