# 날짜와 시간 표시하기
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QDate, Qt


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.date = QDate.currentDate() # currentDate() 메서드를 통해 현재 날짜를 얻고
        self.initUI()

    def initUI(self):
        self.statusBar().showMessage(self.date.toString(Qt.DefaultLocaleLongDate)) # showMessage() 메서드로 상태표시줄에 현재 날짜를 표시
        self.setWindowTitle('Date')
        self.setGeometry(300, 300, 400, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())