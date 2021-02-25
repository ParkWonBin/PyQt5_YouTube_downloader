import os, sys, pyperclip, urllib.request
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPoint, QEvent,QSize
from PyQt5.QtGui import QImage, QPainter, QPixmap
from PyQt5 import uic
from App import yt_downloader

# UI 불러오기
UI_load = uic.loadUiType("YouTube_downloader.ui")[0]

class pwb_Frameless(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.debug = False

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        btn = event.buttons()
        if btn & Qt.LeftButton: self.is_clicked_L = True
        if btn & Qt.RightButton: self.is_clicked_L = False
        if btn & Qt.MidButton:  sys.exit(app.exec_())

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        if self.is_clicked_L:
            self.move(self.x() + delta.x(), self.y() + delta.y())
        else:
            self.resize(self.width() + delta.x(), self.height() + delta.y())
        self.oldPos = event.globalPos()

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
            self.print('drop-dectected')

    def dropEvent(self, event):
        pass
        # print(event.mimeData().text().lstrip("file:///"))

    def print(self,*txt):
        if self.debug : print(*txt)

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.image = QImage()

    def set_image(self,url):
        qPixmapVar = QPixmap()

        if ('http' in url):
            web_img = urllib.request.urlopen(url).read()
            qPixmapVar.loadFromData(web_img)
        else:
            qPixmapVar.load(url)

        self.image = qPixmapVar.toImage() # QImage

    def paintEvent(self, event):
        if self.image.isNull():
            print('이미지가 없습니다.')
        else:
            qp = QPainter(self)
            qp.drawImage(0, 0, self.image.scaled(self.size()))

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
        # self.lbl_picture = QLabel(self.image_viewer)
        #self.loadImageFromWeb()

        # 이벤트 연결
        self.btn_MP3.clicked.connect(self.e_btn_MP3)
        self.btn_MP4.clicked.connect(self.e_btn_MP4)
        self.btn_exit.clicked.connect(self.e_btn_exit)
        self.search_btn.clicked.connect(self.e_search_btn)
        self.search_input.installEventFilter(self)
        self.image_viewer.installEventFilter(self)

    def eventFilter(self, obj, event):
        # search_input 에 클립보드 복사해서 넣기
        if obj != self.search_input: pass
        elif event.type() == QEvent.FocusIn:
            clip = pyperclip.paste()
            if 'youtube.com/' in clip:
                self.search_input.setText(clip)
                self.e_search_btn()
            else :
                self.search_input.setText('')
        elif event.type() == QEvent.FocusOut:
            if not self.search_input.text():
                self.print('내용없음')
                self.search_input.setText('유튜브 주소를 입력해주세요.')

        return super(WindowClass, self).eventFilter(obj, event)
    def e_search_btn(self):
        self.print("search_btn clicked")
        url = self.search_input.text()
        self.App.set_url(url)

        self.print(url,self.App.thumbnail)
        self.print(self.image_viewer.size())
    def e_btn_MP4(self):
        self.print('MP4_clicked')
        self.App.download_mp4()
        self.App.get_dir()
    def e_btn_MP3(self):
        self.print('MP3_clicked')
        self.App.download_mp3()
        self.App.get_dir()
    def e_btn_exit(self):
        self.print('exit_clicked')
        self.close()
    def dropEvent(self, event):
        drop = event.mimeData().text().lstrip("file:///")
        self.print(drop)
        if os.path.isdir(drop):
            self.print("다운로드 폴더변경")
            self.App.set_dir(drop)
        else: self.print("폴더 아님")


if __name__ == '__main__':
    # GUI 관련
    app = QApplication(sys.argv) #QApplication : 프로그램을 실행
    myWindow = WindowClass() # WindowClass의 인스턴스 생성
    myWindow.show() # 프로그램 화면을 보여주는 코드
    app.exec_() # 프로그램을 이벤트루프로 진입시킴

# ui 파일 적용 : https://wikidocs.net/35482
# 비동기 : https://m.blog.naver.com/townpharm/220959370280
#이미지 불러오기 : https://learndataanalysis.org/how-to-display-image-from-the-web-with-qlabel-widget-in-pyqt5/
