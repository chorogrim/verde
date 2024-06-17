# 1. 창 띄우기
import sys
from PyQt5.QtWidgets import QApplication, QWidget


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Test Application') # 타이틀바에 나타나는 창의 제목을 설정
        self.move(300, 300) # 위젯을 스크린의 x=300px, y=300px의 위치로 이동
        self.resize(400, 200) # 위젯의 크기를 너비 400px, 높이 200px로 조절
        self.show() # 위젯을 스크린에 보여줌


if __name__ == '__main__': # 현재 모듈의 이름이 저장되는 내장 변수
   app = QApplication(sys.argv) # 어플리케이션 객체를 생성
   ex = MyApp()
   sys.exit(app.exec_())
