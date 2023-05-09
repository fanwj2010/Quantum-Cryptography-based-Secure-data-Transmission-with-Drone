from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTextEdit
import sys
from PyQt5.uic import loadUi  # 需要导入的模块
import socket

def fly():
    print('fly')
    s.send("0".encode())
    pass


def photo():
    print('photo')
    s.send("1".encode())
    pass





class sender(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(300, 300)

        loadUi("ui/test.ui", self)  # 加载UI文件


        self.photo.clicked.connect(photo)
        self.fly.clicked.connect(fly)



if __name__ == '__main__':
    address = ('127.0.0.1', 31500)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)
    app = QApplication(sys.argv)
    receiver = sender()
    receiver.show()
    sys.exit(app.exec_())
