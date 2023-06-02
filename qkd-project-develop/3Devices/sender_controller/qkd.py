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


class Qubit():  # initialization
    def __init__(self, initial_state, initial_basis):
        """
        initial_state, initial_basis, initial__isMeasured = False
        :param initial_state: 0(sBasis0) or 1(sBasis1)
        :param initial_basis: 0(standard) or 1(H_gate)
        """
        if initial_state:
            self.__state = sBasis1
        else:
            self.__state = sBasis0
        if initial_basis:
            self.__basis = H_gate
        else:
            self.__basis = standard
        self.__isMeasured = False

    def measurement(self, base):
        """
        standard measurement
        :param base:0 or 1
        :return: bit measured 0 or 1
        """
        if self.__isMeasured:
            raise Exception("Qubit already measured!")
        M = 10000
        m = np.random.randint(0, M)
        self.__isMeasured = True
        basenp = standard
        if base == 1:
            basenp = H_gate
        if m < round(pow(norm(np.dot(standard_measture, np.dot(basenp, np.dot(self.__basis, self.__state)))), 2),
                     2) * M:
            return 0
        else:
            return 1

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

    def toBytes(self):
        if self.__state is sBasis0:
            bytes = b'\x00'
        else:
            bytes = b'\x01'
        if self.__basis is standard:
            bytes += b'\x00'
        else:
            bytes += b'\x01'
        return bytes


def generateRandomBits(no_of_qubits):
    """
    static method for the generation of list of random bits i.e. 0 & 1
    :param no_of_qubits: number of qubits
    :return: list of bits
    """
    var = list()
    for i in range(no_of_qubits):
        rnd = np.random.randint(0, 2)
        var.append(rnd)
    return var


def generateRandomBasis(no_of_qubits):
    """
    static method for the generation of list of random basis i.e. 0:standard & 1:Had
    :param no_of_qubits:  number of qubits
    :return: list of basis(0 or 1)
    """
    var = list()
    for i in range(no_of_qubits):
        rnd = np.random.randint(0, 2)
        var.append(rnd)
    return var


def generateQubits(listOfBasis, listOfBits):
    """
    static method for the generation of list of qubits according to the random generated bits and basis
    :param listOfBasis: list of 0 or 1
    :param listOfBits: list of 0 or 1
    :return: list of qubits
    """
    assert len(listOfBits) == len(listOfBasis), "Basis and Bits must be the same length!"
    var = list()
    for i in range(len(listOfBits)):
        qubit = Qubit(listOfBits[i], listOfBasis[i])
        var.append(qubit)
    return var


def measureQubits(listofQubits, listofBasis):
    """
    measure the qubits by the bases
    :param listofQubits: list of qubit
    :param listofBasis: list of 0 or 1
    :return: list of bits (0 or 1)
    """
    var = list()
    for i in range(len(listofQubits)):
        bitMeasured = listofQubits[i].measurement(listofBasis[i])
        var.append(bitMeasured)
    return var


def qubittoSymbol(qubit):
    """
    from object qubit to Symbol
    :param qubit: object qubit
    :return: "━“ or "|" or "╲" or "╱"
    """
    qubitStr = qubit.toString()
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
    """
    list of Basis to symbols
    :param listofBasis:
    :return: list of "+" or "X"
    """
    var = list()
    for i in listofBasis:
        if i == 0:
            basisSym = "+"
        else:
            basisSym = "X"
        var.append(basisSym)
    return var


def listofQubitstoSymbol(listofQubits):
    """
    from list of object qubits to list of Symbol
    :param listofQubits: list of object qubit
    :return: list of  "━“ or "|" or "╲" or "╱"
    """
    var = list()
    for i in listofQubits:
        qubitSym = qubittoSymbol(i)
        var.append(qubitSym)
    return var


def listofBitstoSymbol(listofBits):
    """
    list of bits to symbols
    :param listofBits:
    :return: list of "0" or "1"
    """
    var = list()
    for i in listofBits:
        if i == 0:
            var.append("0")
        else:
            var.append("1")
    return var


def listtobytes(listofBits):
    """
    list of bits or basis (0 or 1) to bytes
    :param listofBits: list of 0 or 1
    :return: bytes in \x00 or \x01
    """
    var = b''
    for i in listofBits:
        if i == 0:
            var += b'\x00'
        else:
            var += b'\x01'
    return var


def bytestolist(bytes):
    """
    bytes to list of bits or basis
    :param bytes:
    :return:
    """
    var = list()
    for i in range(len(bytes)):
        var.append(bytes[i])
    return var


def bytestoListofQubits(bytes):
    var = list()
    for i in range(int(len(bytes) / 3)):
        qubit = Qubit(bytes[3 * i], bytes[3 * i + 1])
        var.append(qubit)
    return var


def listofQubitstoBytes(listofQubits):
    """
    from object qubit to Symbol
    :param listofQubits: list of object qubit
    :return: bytes b'\x00\x01'
    """
    var = b''
    for i in listofQubits:
        var += i.toBytes()
        var += b'\xff'
    return var


def listtoString(list):
    """
    list of string to string
    :param list: list of string
    :return: string with '\n'
    """
    lineNum = 10  # set the line length
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
    """
    compare two bases
    :param basis: list of 0 or 1
    :param recvBasis:
    :return: list of 1(same) or 0(different)
    """
    assert len(basis) == len(recvBasis), "Basis must be the same length!"
    qber = 0
    var = list()
    for i in range(len(basis)):
        if basis[i] == recvBasis[i]:
            var.append(1)
            qber = qber+1
        else:
            var.append(0)
    qber = qber/len(basis)
    return var, qber


def showSameBasis(basis, basisCompare):
    """
    show same basis in list of str after comparing two basis
    :param basis: list of 0 or 1
    :param basisCompare: list of 1(same) or 0(different)
    :return: list of string "+" or "X" or "*"
    """
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


def showFinalkeys(bits, basisCompare):
    """
    show final keys in list of str after comparing two basis
    :param bits: list of 0 or 1
    :param basisCompare: list of 1(same) or 0(different)
    :return: list of string "1" or "0" or "*"
    """
    var = list()
    for i in range(len(bits)):
        if basisCompare[i] == 1:
            if bits[i] == 1:
                var.append("1")
            else:
                var.append("0")
        else:
            var.append("*")
    return var
