# 2. 어플리케이션 아이콘 넣기
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Icon') # 타이틀바에 나타나는 창의 제목을 설정
        self.setWindowIcon(QIcon('web.png)')) # QIcon()에 보여질 이미지를 입력
        self.setGeometry(300, 300, 300, 200) # 
        self.show() # 위젯을 스크린에 보여줌


if __name__ == '__main__': # 현재 모듈의 이름이 저장되는 내장 변수
   app = QApplication(sys.argv) # 어플리케이션 객체를 생성
   ex = MyApp()
   sys.exit(app.exec_())
