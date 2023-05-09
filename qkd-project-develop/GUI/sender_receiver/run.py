# -*- coding: utf-8 -*-
import hashlib
import json, struct
import threading
import traceback
from socket import *
import time
import os
import sys
import numpy as np
from PySide2.QtWidgets import QMessageBox
from numpy.linalg import norm
import PySide2
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtUiTools import QUiLoader
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
        self.ui = QUiLoader().load('ui/sender.ui')
        # self.ui.portEdit.setText("20004")
        # self.ui.qubitsNum.setText("100")
        # 限制host 的输入
        regx = QtCore.QRegExp("\\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?["
                              "0-9][0-9]?)\\b")
        validator_host = QtGui.QRegExpValidator(regx)
        self.ui.hostEdit.setValidator(validator_host)

        regx = QtCore.QRegExp("^([0-9]|[1-9]\\d|[1-9]\\d{2}|[1-9]\\d{3}|[1-5]\\d{4}|6[0-4]\\d{3}|65[0-4]\\d{2}|655["
                              "0-2]\\d|6553[0-5])$")
        validator_Port = QtGui.QRegExpValidator(regx)
        self.ui.portEdit.setValidator(validator_Port)
        self.ui.lineEdit.setValidator(validator_Port)
        self.ui.qubitsNum.setValidator(validator_Port)

        self.ui.GeneratePushButton.clicked.connect(self.generate_qubits)
        self.ui.sendPushButton.clicked.connect(self.send_qubits)

    def generate_qubits(self):
        global listofBasis
        global num_of_qubits
        global listofBits
        global listofQubits
        try:
            #需要默认值
            num_of_qubits = int(self.ui.qubitsNum.text().strip()) or 100
            listofBasis = list()
            listofBits = list()
            listofQubits = list()
            listofBasis = qkd.generateRandomBasis(num_of_qubits)
            listofBits = qkd.generateRandomBits(num_of_qubits)
            listofQubits = qkd.generateQubits(listofBasis, listofBits)
            self.ui.BasePlainTextEdit.setPlainText(qkd.listtoString(qkd.listofBasistoSymbol(listofBasis)))
            self.ui.BitPlainTextEdit.setPlainText(qkd.listtoString(qkd.listofBitstoSymbol(listofBits)))
            self.ui.QubitPlainTextEdit.setPlainText(qkd.listtoString(qkd.listofQubitstoSymbol(listofQubits)))

        except:
            # traceback.print_exc()
            message_error = QMessageBox(QMessageBox.Warning, 'Warning', 'input error!')
            message_error.exec_()
            # self.dlg = MyDialog()
            # self.dlg.exec_()
            return
        # except ValueError:
        #     message_error = QMessageBox(QMessageBox.Warning, 'Warning', 'input error')
        #     message_error.exec_()

        # 若-222/33333 不是overflow
        # except OverflowError:
        #     message_error = QMessageBox(QMessageBox.Warning, 'Warning', 'input error')
        #     message_error.exec_()

    def send_qubits(self):
        global listofBasis
        global listofBits
        global listofQubits
        try:
            port = int(self.ui.portEdit.text()) or 20000
        except:
            message_error = QMessageBox(QMessageBox.Warning, 'Warning', 'Please input the port again')
            message_error.exec_()
            return
        # SendTh = threading.Thread(target=self.qubitsSender, args=(listofQubits, listofBasis, port,))
        # SendTh.start()
        self.qubitsSender( listofQubits, listofBasis, port)
        # SendTh.join()

    def qubitsSender(self, listofQubits, listofBasis, port):
        sender = socket(AF_INET, SOCK_STREAM)
        # 超过这个范围？
        send_buf = 4096
        blocksize = 1024 * 1024 * 3  # blocksize:3MB
        try:
            sender.bind(('', port))
            sender.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            # 设置超时时间 异常处理
            # val = struct.pack("QQ", 5, 50000)
            sender.listen(5)
            print('waiting for conn')
            conn, addr = sender.accept()
            # print(conn)

            # print("num_of_qubits\n", str(num_of_qubits))
            conn.sendall(str(num_of_qubits).encode())
            conn.recv(1024)  # "num received"
            qubitsStr = ""
            for i in listofQubits:
                qubitsStr += i.toString()
            conn.sendall(qubitsStr.encode())
            conn.recv(1024)  # "qubits received and measured"
            basisStr=""
            for i in listofBasis:
                if i==0:
                    basisStr+="0"
                else:
                    basisStr+="1"
            conn.sendall(basisStr.encode())
            recvBasisStr = conn.recv(4096 * 1024).decode()
            listofRecvBasis = list()
            for i in recvBasisStr:
                if i == "0":
                    listofRecvBasis.append(0)
                else:
                    listofRecvBasis.append(1)
            prin_res = qkd.listtoString(qkd.listofBasistoSymbol(listofRecvBasis))
            self.ui.plainTextEdit_4.setPlainText(prin_res)
            res_ls = []
            print("received basis is:", prin_res)
            print("will transmit photo")
            # SendTh = threading.Thread(target=self.dataSender, args=(listofQubits, listofBasis, port,))
            time.sleep(1)
            SendTh = threading.Thread(target=self.dataSender, args=(listofQubits, listofBasis, port))
            SendTh.start()
        except:
            message_error = QMessageBox(QMessageBox.Critical, 'reminder', 'connection fail')
            message_error.exec_()
            return

    def dataSender(self, listofQubits, listofBasis, port):
        print("photo will send in 10 seconds")
        time.sleep(8)
        try:
            s = socket(AF_INET, SOCK_STREAM)
            # 改成服务器IP
            s.connect(('192.168.56.1', 6666))
            print("start send")
        except error as msg:
            print(msg)
            print(sys.exit(1))

        while True:
            try:
                filepath = input('input the file: ')
            # filepath = 'test.png'
            except:
                print("input again")
                filepath = input('input the file: ')
            fhead = struct.pack(b'128sl', bytes(os.path.basename(filepath), encoding='utf-8'),
                                os.stat(filepath).st_size)
            s.send(fhead)
            print('client filepath: {0}'.format(filepath))

            fp = open(filepath, 'rb')
            while 1:
                data = fp.read(1024)
                if not data:
                    print('{0} file send over...'.format(filepath))
                    break
                s.send(data)
            s.close()
            break



    def open_new_window(self):
        # 实例化一个对话框类
        self.dlg = MyDialog()
        # 显示对话框，代码阻塞在这里，
        # 等待对话框关闭后，才能继续往后执行
        self.dlg.exec_()


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
