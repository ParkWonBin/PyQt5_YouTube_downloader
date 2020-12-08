import sys
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QApplication, QLabel

class move :
    def __init__(self):
        self.setWindowFlags(Qt.FramelessWindowHint)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        self.mouseButtonKind(event.buttons())

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        if self.is_clicked_L:
            self.move(self.x() + delta.x(), self.y() + delta.y())
        else:
            self.resize(self.width() + delta.x(), self.height() + delta.y())
        self.oldPos = event.globalPos()

    def mouseButtonKind(self, buttons):
        if buttons & Qt.LeftButton: self.is_clicked_L = True
        if buttons & Qt.RightButton: self.is_clicked_L = False
        if buttons & Qt.MidButton:  sys.exit(app.exec_())

class Window(QMainWindow,move):
    def paintEvent(self, event):
        qp = QPainter(self)
        qp.drawImage(0, 0, self.image.scaled(self.size()))

    def __init__(self):
        super().__init__()
        self.image = QImage('image.jpg')
        self.canvas = QWidget()

        # 레이아웃 및 캔버스 배치
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.setContentsMargins(0, 0, 0, 0)

        content = QWidget()
        content.setLayout(layout)
        self.setCentralWidget(content)

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