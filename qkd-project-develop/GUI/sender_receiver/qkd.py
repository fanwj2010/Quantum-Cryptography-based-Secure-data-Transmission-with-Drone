# -*- coding: utf-8 -*-
import math

import numpy as np
from numpy.linalg import norm

"""
Standard Basis |0> 	   	 & |1>       for the rectilinear basis.
Hadamard Basis |0> + |1> & |0> - |1> for the diagonal basis.
0 0 -> |0>
0 1 -> |1>
1 0 -> |0> + |1>
1 1 -> |0> - |1>
"""
H_gate = np.array([[(1 / math.sqrt(2)), (1 / math.sqrt(2))], [(1 / math.sqrt(2)), (-1 / math.sqrt(2))]])
standard = np.array([[1, 0], [0, 1]])
sBasis0 = np.array([1.0, 0.0]).reshape(-1, 1)
sBasis1 = np.array([0.0, 1.0]).reshape(-1, 1)
standard_measture = sBasis0.reshape(1, -1)
print(standard_measture)

class Qubit():  # initialization
    def __init__(self, initial_state, initial_basis):
        if initial_state:
            self.__state = sBasis1
        else:
            self.__state = sBasis0
        if initial_basis:
            self.__basis = H_gate
        else:
            self.__basis = standard
        self.__isMeasured = False

    # standard measurement
    def measurement(self, base):
        if self.__isMeasured:
            raise Exception("Qubit already measured!")

        M = 10000
        m = np.random.randint(0, M)
        self.__isMeasured = True
        basenp = standard

        if base == 1:
            basenp = H_gate
        # 1.
        if m < round(pow(norm(np.dot(standard_measture, np.dot(basenp, np.dot(self.__basis, self.__state)))), 2),
                     2) * M:
            return 0
        else:
            return 1

    # def getState(self):
    #     return self.__state
    # def getBasis(self):
    #     return self.__basis
    def toString(self):
        if self.__state is sBasis0:
            str = "0"
        else:
            str = "1"
        if self.__basis is standard:
            str += "0"
        else:
            str += "1"
        return str


# static method for the generation of array of random bits i.e. 0 & 1
def generateRandomBits(no_of_qubits):
    var = list()
    for i in range(no_of_qubits):
        rnd = np.random.randint(0, 2)
        var.append(rnd)
    return var


# static method for the generation of array of random basis i.e. 0:standard & 1:Had
def generateRandomBasis(no_of_qubits):
    var = list()
    for i in range(no_of_qubits):
        rnd = np.random.randint(0, 2)
        var.append(rnd)
    return var


def generateQubits(listOfBasis, listOfBits):
    assert len(listOfBits) == len(listOfBasis), "Basis and Bits must be the same length!"
    var = list()
    for i in range(len(listOfBits)):
        qubit = Qubit(listOfBits[i], listOfBasis[i])
        var.append(qubit)
    return var


def measureQubits(listofQubits, listofBasis):

    var = list()
    for i in range(len(listofQubits)):
        bitMeasured = listofQubits[i].measurement(listofBasis[i])
        var.append(bitMeasured)
    return var


def qubittoSymbol(qubit):
    # print(qubit)
    qubitStr = qubit.toString()
    # print(qubitStr)
    # for i in qubitStr:
    #     print(i)
    qubitSym = ""
    if qubitStr[-1:] == "0":
        if qubitStr[:-1] == "0":
            qubitSym = "━"
        else:
            qubitSym = "| "
    else:
        if qubitStr[:-1] == "0":
            qubitSym = "╲"
        else:
            qubitSym = "╱"
    return qubitSym


def listofBasistoSymbol(listofBasis):
    var = list()
    for i in listofBasis:
        if i == 0:
            basisSym = "+"
        else:
            basisSym = "X"
        var.append(basisSym)
    return var


def listofQubitstoSymbol(listofQubits):
    var = list()
    for i in listofQubits:
        qubitSym = qubittoSymbol(i)
        var.append(qubitSym)
    return var


def listofBitstoSymbol(listofBits):
    var = list()
    for i in listofBits:
        if i == 0:
            var.append("0")
        else:
            var.append("1")
    return var


def listtoString(list):
    lineNum = 10
    str = ""
    if len(list) < lineNum:
        for i in range(len(list)):
            str = str + list[i] + ", "
        return str
    str = "1:\t" + list[0] + ", "
    for i in range(lineNum - 1):
        str = str + list[i + 1] + ", "
    str += '\n' + "2:\t"
    row = 3
    for i in range(len(list) - lineNum):
        if i % lineNum == lineNum - 1:
            str = str + list[i + lineNum] + ", " + "\n" + "{}:\t".format(row)
            row = row + 1
        else:
            str = str + list[i + lineNum] + ", "
    return str  # [:-7]


def compareBasis(basis, recvBasis):
    assert len(basis) == len(recvBasis), "Basis must be the same length!"
    var = list()
    for i in range(len(basis)):
        if basis[i] == recvBasis[i]:
            var.append(1)
        else:
            var.append(0)
    return var


def showSameBasis(basis, basisCompare):
    var = list()
    for i in range(len(basis)):
        if basisCompare[i] == 1:
            if basis[i] == 1:
                var.append("+")
            else:
                var.append("X")
        else:
            var.append("* ")
    return var

# print(len("10101111001000010111001100011111000110110101100010110111101111100001111110111111111110110011011001110011010011001101010000000000010001000010110100010100100011110001011100100100101100111011110100100111"))
#
#
# no_of_qubits=100
# print(Qubit(1,1).toString())
# listOfBasis=GenerateRandomBasis(no_of_qubits)
# listOfBits=GenerateRandomBits(no_of_qubits)
# listofQubits=GenerateQubits(listOfBasis,listOfBits)
# # for i in listofQubits:
# #     print(i.toString())
# print(ListofBasistoSymbol(listOfBasis))
# print(ListofQubitstoSymbol(listofQubits))
# print(np.dot(standard_measture, np.dot(H_gate,sBasis0)))
# print(np.dot(standard_measture, sBasis0))
# print(np.dot(standard_measture, np.dot(H_gate,np.dot(H_gate,sBasis0))))
