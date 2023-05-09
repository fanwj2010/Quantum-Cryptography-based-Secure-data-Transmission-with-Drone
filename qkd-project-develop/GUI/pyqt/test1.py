from socket import socket

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QPushButton
# import sys
# import requests
#
# from hyDM.lib.share import SI
# from setting import Ui_configuration


# import file_sever
# import file_client


# 这个类中要配置好server 和client 的IP以及端口
# 未考虑输入不符合规格的问题
class SettingWindow:
    # 先分别构造出每个窗口
    def __init__(self):
        self.ui = uic.loadUi("setting.ui")
        # self.ui.connectPushButton.connectclicked.connect(self.OpenServerWindow)

    #
    #


    # self.ui.button.clicked.connect(self.handleCalc)
    # 在选定为server后配置server的信息
    # def SeverInfo(self):
    #     ip = self.setting.IPlineEdit.text()
    #     port = self.setting.portLineEdit.text()
    #     ip_port = (ip, port)
    #     s = socket.socket()
    #     s.connect(ip_port)
    #
    # 在选定为client后配置client的信息
    # def ClientInfo(self):
    #     ip = self.ui.IPlineEdit.text()
    #     port = self.ui.portLineEdit.text()
    #     ip_port = (ip, port)
    #     s = socket.socket()
    #     s.connect(ip_port)
    # 打开server窗口
    # def OpenServerWindow(self):
    #     SI.server = ServerWindow()
    #     SI.server.ui.show()
    # self.client = uic.loadUi("client.ui")
    # def SeverWindow(self, port):
    #     print(f'在{port}端监听')
    #     client_socket, address = s.accept()

# server窗口
# class ServerWindow(QtWidgets.QDialog):
#     def __init__(self):
#         self.ui = uic.loadUi("server.ui")
#

if __name__ == '__main__':
    app = QApplication([])
    windowSetting = SettingWindow()
    windowSetting.ui.show()
    app.exec_()
    # window_sever = ServerWindow()

    # windowSetting.Ui_configuration.connectPushButton.clicked.connect(window_sever.show())
    # sys.exit(app.exec_())
