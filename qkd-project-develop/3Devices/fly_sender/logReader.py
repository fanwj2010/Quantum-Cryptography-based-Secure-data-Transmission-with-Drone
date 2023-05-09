import datetime
import sys
import os

import qkd


class Item:
    time = ''
    QBER = ''
    length = ''
    qubits = ''
    bits = ''
    basis = ''
    recvbasis = ''
    compareBits = ''
    compareBasis = ''
    finalKey = ''

    def info(self):
        return "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}".format(self.time, self.QBER, self.length, self.qubits, self.bits,
                                                       self.basis, self.recvbasis, self.compareBits, self.compareBasis,
                                                       self.finalKey)



def readLog(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as filelog:
            line = filelog.readline()

            while line:
                item = Item()
                item.time = line
                line = filelog.readline()
                item.QBER = line
                line = filelog.readline()
                item.length = line
                line = filelog.readline()
                item.qubits = line
                line = filelog.readline()
                item.bits = line
                line = filelog.readline()
                item.basis = line
                line = filelog.readline()
                item.recvbasis = line
                line = filelog.readline()
                item.compareBits = line
                line = filelog.readline()
                item.compareBasis = line
                line = filelog.readline()
                item.finalKey = line
                line = filelog.readline()
                line = filelog.readline()
                line = filelog.readline()
                line = filelog.readline()
                dataList.append(item)


filename = 'data/asdfg.txt'
dataList = []
readLog(filename)
for item in dataList:
    print(item.info())
