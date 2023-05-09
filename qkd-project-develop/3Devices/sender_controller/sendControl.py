# -*- coding: utf-8 -*-
import hashlib
import json, struct
import threading
from socket import *
import time
import os
import sys
import numpy as np
from numpy.linalg import norm
import PySide2
from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader

import protocol
import qkd

main_win = None

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

num_of_qubits = 100
listofBasis = list()
listofBits = list()
listofQubits = list()


class LoginWin:

    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('ui/senderControl.ui')
        # self.ui.droneIPEdit.setText("192.168.43.148")
        # self.ui.recvIPEdit.setText("192.168.43.151")
        self.ui.droneIPEdit.setText("127.0.0.1")
        self.ui.recvIPEdit.setText("127.0.0.1")
        self.ui.piPortEdit.setText("20001")
        self.ui.receiverPortEdit.setText("20002")
        self.ui.qubitsNum.setText("100")
        self.ui.ConnectPushButton.clicked.connect(self.connectRecv)
        self.ui.DronePushButton.clicked.connect(self.droneFly)
        self.ui.GeneratePushButton.clicked.connect(self.generate_qubits)
        self.ui.sendPushButton.clicked.connect(self.send_qubits)

    def droneFly(self):
        sc = socket(AF_INET, SOCK_STREAM)
        sc.connect((self.ui.droneIPEdit.displayText(), int(self.ui.piPortEdit.displayText())))

        date = sc.recv(1024)  # b'had connected'
        print(date.decode('utf-8'))
        sc.send(protocol.make_dronefly_info('aa'))

    def connectRecv(self):
        sc = socket(AF_INET, SOCK_STREAM)
        sc.connect((self.ui.droneIPEdit.displayText(), int(self.ui.piPortEdit.displayText())))

        date = sc.recv(1024)  # b'had connected'
        print(date.decode('utf-8'))
        sc.send(
            protocol.make_recvip_info(self.ui.recvIPEdit.displayText(), int(self.ui.receiverPortEdit.displayText()))
        )

    def generate_qubits(self):
        global listofBasis
        global num_of_qubits
        global listofBits
        global listofQubits
        try:
            num_of_qubits = int(self.ui.qubitsNum.displayText())
        except:
            self.dlg = MyDialog()
            self.dlg.exec_()
            return
        listofBasis = list()
        listofBits = list()
        listofQubits = list()

        sc = socket(AF_INET, SOCK_STREAM)
        sc.connect((self.ui.droneIPEdit.displayText(), int(self.ui.piPortEdit.displayText())))

        date = sc.recv(1024)  # b'had connected'
        print(date.decode('utf-8'))

        sc.send(protocol.make_generate_qubits_request(num_of_qubits))
        qubitsbytes = sc.recv(3 * num_of_qubits + 256)
        print(qubitsbytes)
        print(len(qubitsbytes))

        listofQubits = qkd.bytestoListofQubits(qubitsbytes)

        for i in range(num_of_qubits):
            listofBits.append(qubitsbytes[3 * i])
            listofBasis.append(qubitsbytes[3 * i + 1])

        sc.send(b'Qubits received')

        self.ui.BasePlainTextEdit.setPlainText(qkd.listtoString(qkd.listofBasistoSymbol(listofBasis)))
        self.ui.BitPlainTextEdit.setPlainText(qkd.listtoString(qkd.listofBitstoSymbol(listofBits)))
        self.ui.QubitPlainTextEdit.setPlainText(qkd.listtoString(qkd.listofQubitstoSymbol(listofQubits)))

    def send_qubits(self):
        global listofBasis
        global num_of_qubits
        global listofBits
        global listofQubits
        sc = socket(AF_INET, SOCK_STREAM)
        sc.connect((self.ui.droneIPEdit.displayText(), int(self.ui.piPortEdit.displayText())))

        date = sc.recv(1024)  # b'had connected'
        print(date.decode('utf-8'))
        sc.send(protocol.make_send_qubits_request())

        recvBasisB = sc.recv(num_of_qubits + 256)
        recvListofBasis = qkd.bytestolist(recvBasisB)
        print(b"recvBasisB " + recvBasisB)
        self.ui.recvBasePlainTextEdit.setPlainText(qkd.listtoString(qkd.listofBasistoSymbol(recvListofBasis)))

        basisCompare, qber = qkd.compareBasis(listofBasis, recvListofBasis)
        print("QBER: ", qber * 100, "%")
        self.ui.qberEdit.setText(str(qber * 100) + '%')

        listofFinalkeyStr = qkd.showFinalkeys(listofBits, basisCompare)
        self.ui.finalKeyTextEdit.setPlainText(qkd.listtoString(listofFinalkeyStr))

    def open_new_window(self):
        # 实例化一个对话框类
        self.dlg = MyDialog()
        # 显示对话框，代码阻塞在这里，
        # 等待对话框关闭后，才能继续往后执行
        self.dlg.exec_()
    # def onLogin(self):
    #     global main_win
    #     # 实例化另外一个窗口
    #     main_win = Window_Main()
    #     # 显示新窗口
    #     main_win.ui.show()
    #     # 关闭自己
    #     self.ui.close()


class MyDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Connecting')

        self.resize(500, 400)
        self.textEdit = QtWidgets.QPlainTextEdit(self)
        self.textEdit.setPlaceholderText("Connecting")
        self.textEdit.move(10, 25)
        self.textEdit.resize(300, 350)

        self.button = QtWidgets.QPushButton('Cancel', self)
        self.button.move(380, 80)
        self.button.clicked.connect(self.open_new_window)

    def open_new_window(self):
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    wm = LoginWin()
    wm.ui.show()
    sys.exit(app.exec_())
