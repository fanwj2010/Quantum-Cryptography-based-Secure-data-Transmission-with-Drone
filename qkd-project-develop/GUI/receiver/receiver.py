import json,struct
import sys
import threading
from socket import *

from PySide2.QtWidgets import QMessageBox

import qkd
import time
import os
import PySide2
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Signal,QObject
import qkd


main_win = None

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

num_of_qubits=100
listofBasis=list()
listofBits=list()
listofQubits=list()
finalKey=list()

# # 自定义信号源对象类型，一定要继承自 QObject
# class MySignals(QObject):
#
#     # 定义一种信号，两个参数 类型分别是： QTextBrowser 和 字符串
#     # 调用 emit方法 发信号时，传入参数 必须是这里指定的 参数类型
#     line_text_print = Signal(PySide2.QtWidgets.QLineEdit,str)
#     plain_text_print=Signal(PySide2.QtWidgets.QPlainTextEdit,str)
#     # 还可以定义其他种类的信号
#     update_table = Signal(str)
#
# # 实例化
# global_ms = MySignals()

class LoginWin:

    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('ui/receiver.ui')
        # self.ui.hostLineEdit.setText("127.0.0.1")
        # self.ui.portLlineEdit.setText("20004")
        self.ui.lenLineEdit.setPlaceholderText("Unknown")
        # self.ui.GeneratePushButton.clicked.connect(self.generate_qubits)
        self.ui.connectPushButton.clicked.connect(self.receiveQubits)
        # 限制host 的输入
        regx = QtCore.QRegExp("\\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?["
                              "0-9][0-9]?)\\b")
        validator_host = QtGui.QRegExpValidator(regx)
        self.ui.hostLineEdit.setValidator(validator_host)
        # 限制 port port2 以及qubitlen 的输入
        regx = QtCore.QRegExp("^([0-9]|[1-9]\\d|[1-9]\\d{2}|[1-9]\\d{3}|[1-5]\\d{4}|6[0-4]\\d{3}|65[0-4]\\d{2}|655["
                              "0-2]\\d|6553[0-5])$")
        validator_Port = QtGui.QRegExpValidator(regx)
        self.ui.portLlineEdit.setValidator(validator_Port)
        self.ui.lenLineEdit.setValidator(validator_Port)
        # self.ui.keyPlainTextEdit.setPlainText(qkd.listtoString(qkd.listofBitstoSymbol(finalKey)))

    def receiveQubits(self):
        while True:
            try:
                ipaddr = self.ui.hostLineEdit.text()
                port = int(self.ui.portLlineEdit.text())
                receiver = socket(AF_INET, SOCK_STREAM)
                receiver.connect((ipaddr, port))
                break
            except Exception:
                message_error = QMessageBox(QMessageBox.Critical, 'reminder', 'Connection Fail!')
                message_error.exec_()
                return
        num_of_qubits=int(receiver.recv(4096*1024).decode())
        self.ui.lenLineEdit.setText(str(num_of_qubits))
        # print("num", num_of_qubits)
        receiver.sendall("num received".encode())
        qubitStr=receiver.recv(4096*1024).decode()
        print(qubitStr)
        listofQubits=list()
        # print(len(qubitStr))
        for i in range(int(len(qubitStr)/2)):
            listofQubits.append(qkd.Qubit(qubitStr[2*i], qubitStr[2*i+1]))

        print(qkd.listofQubitstoSymbol(listofQubits))


        print(num_of_qubits)
        listofBasis=qkd.generateRandomBasis(num_of_qubits)
        # global_ms.plain_text_print.emit(self.ui.basePlainTextEdit, qkd.ListtoString(qkd.listofBasistoSymbol(listofBasis)))
        self.ui.basePlainTextEdit.setPlainText(qkd.listtoString(qkd.listofBasistoSymbol(listofBasis)))
        listofBits=qkd.measureQubits(listofQubits, listofBasis)
        self.ui.bitsPlainTextEdit.setPlainText(qkd.listtoString(qkd.listofBitstoSymbol(listofBits)))
        receiver.sendall("qubits received and measured".encode())
        recvBasisStr = receiver.recv(4096 * 1024).decode()
        listofRecvBasis = list()
        for i in recvBasisStr:
            if i =="0":
                listofRecvBasis.append(0)
            else:
                listofRecvBasis.append(1)
        self.ui.recvBasePlainTextEdit.setPlainText(qkd.listtoString(qkd.listofBasistoSymbol(listofRecvBasis)))
        basisStr = ""
        for i in listofBasis:
            if i == 0:
                basisStr += "0"
            else:
                basisStr += "1"
        receiver.sendall(basisStr.encode())

        comparelist = qkd.compareBasis(listofBasis,listofRecvBasis)
        print("com", len(comparelist))
        # finalKey=list()
        for i in range(len(comparelist)):
            # print("loop",i)
            if comparelist[i] == 1:
                finalKey.append(listofBits[i])
                # print("key len",len(finalKey))
        self.ui.keyPlainTextEdit.setPlainText(qkd.listtoString(qkd.listofBitstoSymbol(finalKey)))
        print("photo received")
        SendTh = threading.Thread(target=self.socket_service, args=(listofQubits, listofBasis, port,))
        SendTh.start()


    def socket_service(self, listofQubits, listofBasis, port):
        print("photo will receive")
        try:
            s = socket(AF_INET, SOCK_STREAM)
            s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            s.bind(('', 6666))
            s.listen(10)
        except error as msg:
            print(msg)
            sys.exit(1)

        print("Wait")

        while True:
            sock, addr = s.accept()
            self.deal_data(sock, addr)
            break
        s.close()
        print("photo is well received")

    def deal_data(self, sock, addr):
        print("Accept connection from {0}".format(addr))

        while True:
            fileinfo_size = struct.calcsize('128sl')
            buf = sock.recv(fileinfo_size)
            if buf:
                filename, filesize = struct.unpack('128sl', buf)
                fn = filename.decode().strip('\x00')
                new_filename = os.path.join('./', 'new_' + fn)

                recvd_size = 0
                fp = open(new_filename, 'wb')

                while not recvd_size == filesize:
                    if filesize - recvd_size > 1024:
                        data = sock.recv(1024)
                        recvd_size += len(data)
                    else:
                        data = sock.recv(1024)
                        recvd_size = filesize
                    fp.write(data)
                fp.close()
            sock.close()
            break





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    wm = LoginWin()
    wm.ui.show()
    sys.exit(app.exec_())
