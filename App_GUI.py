import sys,os
import pyperclip
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPoint, QByteArray, QSize, QEvent
from PyQt5 import uic
from App import yt_downloader

# UI 불러오기
UI_load = uic.loadUiType("YouTube_downloader.ui")[0]

# 프레임 없는 창
class pwb_Frameless(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.debug = False

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

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
            self.print('drop-dectected')

    def dropEvent(self, event):
        pass
        # print(event.mimeData().text().lstrip("file:///"))

    def print(self,*txt):
        if self.debug : print(*txt)

# GUI 프로그램
class WindowClass(QDialog, UI_load, pwb_Frameless) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.debug = True
        self.print("GUI-YouTube-downloader start!")

        # 창 크기 맞춰 레이아웃 크기 조절
        self.setLayout(self.main_layout)

        # GUI에서 App 사용
        self.App = yt_downloader()

        # 이벤트 연결
        self.btn_MP3.clicked.connect(self.e_btn_MP3)
        self.btn_MP4.clicked.connect(self.e_btn_MP4)
        self.btn_exit.clicked.connect(self.e_btn_exit)
        self.search_btn.clicked.connect(self.e_search_btn)
        self.search_input.installEventFilter(self)
        self.search_input.setFocus()

    def eventFilter(self, obj, event):
        if obj != self.search_input: pass
        elif event.type() == QEvent.FocusIn:
            # 클립보드 복사
            clip = pyperclip.paste()
            if 'youtube.com/' in clip:
                self.search_input.setText(clip)
            else :
                self.search_input.setText('')
        elif event.type() == QEvent.FocusOut:
            if not self.search_input.text():
                self.print('내용없음')
                self.search_input.setText('유튜브 주소를 입력해주세요.')
        return super(WindowClass, self).eventFilter(obj, event)

    def e_search_btn(self):
        self.print("search_btn clicked")
        self.print(self.search_input.text())
    def e_btn_MP4(self):
        self.print('MP4_clicked')
        #self.App.download_mp4()
    def e_btn_MP3(self):
        self.print('MP3_clicked')
        #self.App.download_mp3()
    def e_btn_exit(self):
        self.print('exit_clicked')
        # self.close()
    def dropEvent(self, event):
        drop = event.mimeData().text().lstrip("file:///")
        self.print(drop)
        if os.path.isdir(drop):
            self.print("다운로드 폴더변경")
            # self.App.set_dir(drop)
        else: self.print("폴더 아님")


if __name__ == '__main__':
    # GUI 관련
    app = QApplication(sys.argv) #QApplication : 프로그램을 실행
    myWindow = WindowClass() # WindowClass의 인스턴스 생성
    myWindow.show() # 프로그램 화면을 보여주는 코드
    app.exec_() # 프로그램을 이벤트루프로 진입시킴

# ui 파일 적용 : https://wikidocs.net/35482
# 비동기 : https://m.blog.naver.com/townpharm/220959370280