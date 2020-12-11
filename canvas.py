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

class Window(QMainWindow,move):
    def paintEvent(self, event):
        qp = QPainter(self)
        qp.drawImage(0, 0, self.image.scaled(self.size()))

    def load_img(self,url):
        qPixmapVar = QPixmap()
        is_web = bool('http' in url)

        if not is_web:
            qPixmapVar.load(url)
        else:
            web_img = urllib.request.urlopen(url).read()
            qPixmapVar.loadFromData(web_img)
        return qPixmapVar

    def __init__(self):
        super().__init__()
        self.canvas= QWidget()
        self.image = QImage('image.jpg')

        # 레이아웃 및 캔버스 배치
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.setContentsMargins(0, 0, 0, 0)

        content = QWidget()
        content.setLayout(layout)
        self.setCentralWidget(content)

        ####################
        url = "image.jpg"
        url = 'https://img.youtube.com/vi/WGUyDrzf93c/maxresdefault.jpg'
        self.Desk2 = QLabel(self.canvas)
        self.Desk2.setPixmap(self.load_img(url))

        ################
        self.Desk = QLabel(' \n123  \n ', self.canvas)
        self.Desk.setStyleSheet("color: black;"
                                "background-color: #FFFFFF;"
                                "border-style: solid;"
                                "border-width: 4px;"
                                "border-color: #AAAAAA")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())