import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPoint, QByteArray, QSize, QEvent
from PyQt5 import uic
from App import yt_downloader

class pwb_Frameless(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        self.mouseButtonKind(event.buttons())

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        if self.is_clicked_L:
            self.move(self.x() + delta.x(), self.y() + delta.y())
        else:
            self.resize_window(self.width() + delta.x(), self.height() + delta.y())
        self.oldPos = event.globalPos()

    def mouseButtonKind(self, buttons):
        if buttons & Qt.LeftButton: self.is_clicked_L = True
        if buttons & Qt.RightButton: self.is_clicked_L = False
        if buttons & Qt.MidButton:  sys.exit(app.exec_())

    def resize_window(self, x, y):
        self.resize(x, y)

#화면을 띄우는데 사용되는 Class 선언
UI_load = uic.loadUiType("YouTube_downloader.ui")[0]
class WindowClass(QDialog, UI_load, pwb_Frameless) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setLayout(self.main_layout)
#        for i in dir(self):print(i)

if __name__ == '__main__':
    print('GUI')
    # App = yt_downloader()
    # App.set_url(input("youtube url을 입력하세요."))
    # App.get_dir()
    # App.download_mp3()

    # GUI 관련
    app = QApplication(sys.argv) #QApplication : 프로그램을 실행
    myWindow = WindowClass() # WindowClass의 인스턴스 생성
    myWindow.show() # 프로그램 화면을 보여주는 코드
    app.exec_() # 프로그램을 이벤트루프로 진입시킴

# ui 파일 적용 : https://wikidocs.net/35482