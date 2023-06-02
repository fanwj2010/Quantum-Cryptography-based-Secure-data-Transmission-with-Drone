# -*- coding: utf-8 -*-
import datetime
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
recvListofBasis = list()
listofFinalkeyStr = list()
qber=0.0


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
        self.ui.sendPushButton.clicked.connect(self.tests)

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
        global recvListofBasis
        global listofFinalkeyStr
        global qber
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
        self.send_qubits()
        self.ui.recvBasePlainTextEdit.setPlainText(qkd.listtoString(qkd.listofBasistoSymbol(recvListofBasis)))
        self.ui.qberEdit.setText(str(round(qber * 100.0, 2)) + '%')
        self.ui.finalKeyTextEdit.setPlainText(qkd.listtoString(listofFinalkeyStr))

    def send_qubits(self):
        global listofBasis
        global num_of_qubits
        global listofBits
        global listofQubits
        global recvListofBasis
        global listofFinalkeyStr
        global qber
        sc = socket(AF_INET, SOCK_STREAM)
        sc.connect((self.ui.droneIPEdit.displayText(), int(self.ui.piPortEdit.displayText())))

        date = sc.recv(1024)  # b'had connected'
        print(date.decode('utf-8'))
        sc.send(protocol.make_send_qubits_request())

        recvBasisB = sc.recv(num_of_qubits + 256)
        recvListofBasis = qkd.bytestolist(recvBasisB)
        print(b"recvBasisB " + recvBasisB)
        # self.ui.recvBasePlainTextEdit.setPlainText(qkd.listtoString(qkd.listofBasistoSymbol(recvListofBasis)))

        basisCompare, qber = qkd.compareBasis(listofBasis, recvListofBasis)
        print("QBER: ", round(qber * 100.0,2), "%")
        # self.ui.qberEdit.setText(str(round(qber * 100.0,2)) + '%')

        listofFinalkeyStr = qkd.showFinalkeys(listofBits, basisCompare)
        self.ui.finalKeyTextEdit.setPlainText(qkd.listtoString(listofFinalkeyStr))

    def open_new_window(self):
        self.dlg = MyDialog()
        self.dlg.exec_()

    def test_qubits(self,num):
        global listofBasis
        global num_of_qubits
        global listofBits
        global listofQubits
        global recvListofBasis
        global listofFinalkeyStr
        global qber

        num_of_qubits = num

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

        # self.ui.BasePlainTextEdit.setPlainText(qkd.listtoString(qkd.listofBasistoSymbol(listofBasis)))
        # self.ui.BitPlainTextEdit.setPlainText(qkd.listtoString(qkd.listofBitstoSymbol(listofBits)))
        # self.ui.QubitPlainTextEdit.setPlainText(qkd.listtoString(qkd.listofQubitstoSymbol(listofQubits)))
        self.send_qubits()

    def tests(self):
        global listofBasis
        global num_of_qubits
        global listofBits
        global listofQubits
        global recvListofBasis
        global listofFinalkeyStr
        global qber
        dateTime_p = datetime.datetime.now()
        str_p = datetime.datetime.strftime(dateTime_p, '%Y-%m-%d_%H-%M-%S')
        testfilename = './data/' + 'test_' + str_p + '.txt'
        open(testfilename, 'w+').close()
        for i in range(10):
            for j in range(3):
                lenth=(i+1)*100
                self.test_qubits(lenth)
                saveLog(testfilename,lenth,listofBasis,listofBits,listofQubits,recvListofBasis)
        self.ui.BasePlainTextEdit.setPlainText(qkd.listtoString(qkd.listofBasistoSymbol(listofBasis)))
        self.ui.BitPlainTextEdit.setPlainText(qkd.listtoString(qkd.listofBitstoSymbol(listofBits)))
        self.ui.QubitPlainTextEdit.setPlainText(qkd.listtoString(qkd.listofQubitstoSymbol(listofQubits)))
        self.ui.recvBasePlainTextEdit.setPlainText(qkd.listtoString(qkd.listofBasistoSymbol(recvListofBasis)))
        self.ui.qberEdit.setText(str(round(qber * 100.0, 2)) + '%')
        self.ui.finalKeyTextEdit.setPlainText(qkd.listtoString(listofFinalkeyStr))


def saveLog(filename, length, listofBasis, listofBits, listofQubits, recvListofBasis):
    if os.path.exists(filename):
        dateTime_p = datetime.datetime.now()
        str_p = datetime.datetime.strftime(dateTime_p, '%Y-%m-%d_%H-%M-%S')
        qubitsStr = qkd.listtoLineStr(qkd.listofQubitstoSymbol(listofQubits))
        bitsStr = qkd.listtoLineStr(qkd.listofBitstoSymbol(listofBits))
        baseStr = qkd.listtoLineStr(qkd.listofBasistoSymbol(listofBasis))
        recvbaseStr = qkd.listtoLineStr(qkd.listofBasistoSymbol(recvListofBasis))
        basisCompare, qber = qkd.compareBasis(listofBasis, recvListofBasis)
        compareBits = qkd.listtoLineStr(qkd.showFinalkeys(listofBits, basisCompare))
        compareBasis = qkd.listtoLineStr(qkd.showSameBasis(listofBits, basisCompare))
        finalKeys = qkd.listtoLineStr(qkd.finalKeys(listofBits, basisCompare))
        with open(filename, 'a+') as filelog:
            filelog.write(str_p + ': \n')
            filelog.write("QBER: " + str(round(qber * 100.0,2)) + "% \n")
            filelog.write("Length: " + str(length) + "\n")
            filelog.write("Qubits:\t" + qubitsStr + "\n")
            filelog.write("Bits:\t" + bitsStr + " \n")
            filelog.write("basis:\t" + baseStr + " \n")
            filelog.write("recvbasis:\t" + recvbaseStr + " \n")
            filelog.write("compareBits:\t" + compareBits + " \n")
            filelog.write("compareBasis:\t" + compareBasis + " \n")
            filelog.write("final keys:" +str(len(finalKeys))+'\t'+ finalKeys + " \n")
            filelog.write("\n\n\n")

    else:
        print('filename not found')
        return

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
    print(datetime.datetime)
    if not os.path.exists('./data'):
        os.mkdir('./data')
    app = QtWidgets.QApplication(sys.argv)
    wm = LoginWin()
    wm.ui.show()
    sys.exit(app.exec_())
