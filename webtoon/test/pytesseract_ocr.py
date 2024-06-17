# 필요한 라이브러리 불러오기
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QMessageBox, QVBoxLayout, QWidget, QPushButton, QLabel, QScrollArea
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor
from PyQt5.QtCore import Qt, QRect
from PIL import Image
import pytesseract


'''
코드의 전반적인 흐름:
1. 애플리케이션이 시작되면 창과 UI 요소가 초기화됨
2. 사용자가 이미지를 열면, 이미지가 표시되고 OCR을 통해 텍스트와 좌표가 추출됨
3. 추출된 텍스트와 좌표가 텍스트 편집기에 표시되며, 이미지 위에 경계 상자가 그려짐
4. 사용자가 저장 버튼을 클릭하면 텍스트 편집기의 내용이 텍스트 파일로 저장됨
'''

class OCRQualityChecker(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('OCR test') # 창의 제목 설정

        # 메인 위젯과 레이아웃 생성
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # 이미지를 표시할 QLabel 생성하고 중앙에 정렬
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        # ocr 결과를 표시할 QTextEdit 위젯 생성하고 레이아웃에 추가
        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)

        # 저장 버튼 생성 후 클릭시 save_file 메서드를 호출하도록 연결
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_file)
        self.layout.addWidget(self.save_button)

        # 메뉴 바를 생성하고 파일 메뉴 추가
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        # 액션 클릭시 open_file 메서드를 호출하도록 연결
        open_file_action = QAction('Open Image', self)
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        # 창의 크기와 위치를 설정한 후, 창을 표시
        self.setGeometry(300, 300, 800, 600)
        self.show()

    # 파일 열기 대화상자를 열어 이미지 선택 -> 파일을 선택하면 이미지를 QImage로 불러와 표시하고 Pillow를 사용하여 pytesseract로 OCR 수행
    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)", options=options)
        if file_name:
            try:
                # Display the image
                self.image = QImage(file_name)
                self.image_label.setPixmap(QPixmap.fromImage(self.image))

                # Perform OCR for Korean language with bounding boxes
                pil_image = Image.open(file_name)
                self.ocr_result = pytesseract.image_to_data(pil_image, lang='kor', output_type=pytesseract.Output.DICT)
                self.display_ocr_results()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file: {e}")

    # QPainter를 사용해 OCR 결과의 경계 상자를 이미지에 그리기
    def display_ocr_results(self):
        painter = QPainter(self.image)
        painter.setPen(QColor(255, 0, 0))

        self.text_edit.clear()
        num_boxes = len(self.ocr_result['level'])
        for i in range(num_boxes):
            x, y, w, h = (self.ocr_result['left'][i], self.ocr_result['top'][i], 
                          self.ocr_result['width'][i], self.ocr_result['height'][i])
            text = self.ocr_result['text'][i]
            if text.strip():
                self.text_edit.append(f"({x}, {y}, {w}, {h}): {text}")
                painter.drawRect(QRect(x, y, w, h))

        self.image_label.setPixmap(QPixmap.fromImage(self.image))
        painter.end()

    # 저장 대화상자를 열어 파일 이름을 입력받고, 입력받은 파일 이름으로 텍스트 편집기의 내용을 파일로 저장
    def save_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Text File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    data = self.text_edit.toPlainText()
                    f.write(data)
                    QMessageBox.information(self, "Success", "File saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file: {e}")

# PyQt 애플리케이션을 생성하고 OCRQualityChecker 인스턴스를 생성
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = OCRQualityChecker()
    sys.exit(app.exec_())
