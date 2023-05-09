import json,struct
import sys
from socket import *
import qkd
import time
import os
import PySide2
from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Signal,QObject
import qkd


main_win = None

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

num_of_qubits=100
listofBasis=list()
listofBits = list()
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
        self.ui.hostLineEdit.setText("127.0.0.1")
        self.ui.portLlineEdit.setText("20004")
        self.ui.lenLineEdit.setText("Unknown")
        # self.ui.GeneratePushButton.clicked.connect(self.generate_qubits)
        self.ui.connectPushButton.clicked.connect(self.receiveQubits)


        # self.ui.keyPlainTextEdit.setPlainText(qkd.listtoString(qkd.listofBitstoSymbol(finalKey)))


    #     # 自定义信号的处理函数
    #     global_ms.plain_text_print.connect(self.printToGui)
    #
    # def printToGui(self, fb, text):
    #     fb.append(str(text))
    #     fb.ensureCursorVisible()

    def receiveQubits(self):
        ipaddr=self.ui.hostLineEdit.displayText()
        receiver=socket(AF_INET,SOCK_STREAM)
        while True:
            try:
                receiver.connect((ipaddr,20000+4))
                break
            except Exception:
                # try:
                #     receiver.connect((ipaddr,20000+5))
                #     break
                # except Exception:
                continue
        num_of_qubits=int(receiver.recv(4096*1024).decode())
        self.ui.lenLineEdit.setText(str(num_of_qubits))
        # print("num", num_of_qubits)
        receiver.sendall("num received".encode())
        qubitStr=receiver.recv(4096*1024).decode()
        print(qubitStr)
        listofQubits=list()
        # print(len(qubitStr))
        for i in range(int(len(qubitStr)/2)):
            listofQubits.append(qkd.Qubit(qubitStr[2*i],qubitStr[2*i+1]))

        print(qkd.listofQubitstoSymbol(listofQubits))


        print(num_of_qubits)
        listofBasis=qkd.generateRandomBasis(num_of_qubits)
        # global_ms.plain_text_print.emit(self.ui.basePlainTextEdit, qkd.ListtoString(qkd.listofBasistoSymbol(listofBasis)))
        self.ui.basePlainTextEdit.setPlainText(qkd.listtoString(qkd.listofBasistoSymbol(listofBasis)))
        listofBits=qkd.measureQubits(listofQubits,listofBasis)
        self.ui.bitsPlainTextEdit.setPlainText(qkd.listtoString(qkd.listofBitstoSymbol(listofBits)))
        receiver.sendall("qubits received and measured".encode())
        recvBasisStr = receiver.recv(4096 * 1024).decode()
        listofRecvBasis=list()
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

        comparelist=qkd.compareBasis(listofBasis,listofRecvBasis)
        print("com",len(comparelist))
        # finalKey=list()
        for i in range(len(comparelist)):
            # print("loop",i)
            if comparelist[i]==1:
                finalKey.append(listofBits[i])
                # print("key len",len(finalKey))
        self.ui.keyPlainTextEdit.setPlainText(qkd.listtoString(qkd.listofBitstoSymbol(finalKey)))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    wm = LoginWin()
    wm.ui.show()
    sys.exit(app.exec_())