import sys, urllib.request
from PyQt5.QtGui import QImage, QPainter,QPixmap
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QApplication, QLabel

class move :
    def __init__(self):
        self.setWindowFlags(Qt.FramelessWindowHint)

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

class canvas(QMainWindow,move):
    def paintEvent(self, event):
        qp = QPainter(self)
        qp.drawImage(0, 0, self.image.scaled(self.size()))

    def load_img(self,url):
        qPixmapVar = QPixmap()
        is_web = bool('http' in url)

        if is_web:
            web_img = urllib.request.urlopen(url).read()
            qPixmapVar.loadFromData(web_img)
        else:
            qPixmapVar.load(url)

        return qPixmapVar

    def __init__(self):
        super().__init__()
        self.canvas= QWidget()

        # 레이아웃 및 캔버스 배치
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.setContentsMargins(0, 0, 0, 0)

        content = QWidget()
        content.setLayout(layout)
        self.setCentralWidget(content) # 그림을 겹치기 위한 레이아웃

        # 이미지 표현 방법 1
        # 배경 그리기 : self의 paint event로 배경을 그림
        # 이미지변환 : https://beausty23.tistory.com/76
        url = 'https://img.youtube.com/vi/cbuZfY2S2UQ/maxresdefault.jpg'
        self.image = self.load_img(url).toImage()

        # 이미지 표현 방법 2
        # 배경 위에 떠있는 canvas에 라벨을 추가한 것임
        url = "image.jpg"
        self.Desk2 = QLabel(self.canvas)
        self.Desk2.setPixmap(self.load_img(url))

        # 텍스트 표현 방법
        self.Desk = QLabel(' \n123  \n ', self.canvas)
        self.Desk.setStyleSheet("color: black;"
                                "background-color: #FFFFFF;"
                                "border-style: solid;"
                                "border-width: 4px;"
                                "border-color: #AAAAAA")

if __name__ == "__main__":
    # desinger랑 같이 사용하는 방법
    # https://stackoverflow.com/questions/51768266/painting-in-a-qlabel-with-paintevent
    app = QApplication(sys.argv)
    window = canvas()
    window.show()
    sys.exit(app.exec_())