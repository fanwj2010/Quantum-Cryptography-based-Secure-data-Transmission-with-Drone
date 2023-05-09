#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：qkd-project 
@File    ：test_recv.py
@Author  ：orionplan
@Date    ：2021/5/1 21:40 
'''
import threading
from socket import *
import protocol
import qkd


port = 20002
receiveer_ip = ''
receiver_port = -1

num_of_qubits = 100
listofBasis = list()
listofBits = list()
listofQubits = list()


def tcplink(sock, addr):
    global receiveer_ip
    global receiver_port
    global num_of_qubits
    global listofBits
    global listofBasis
    global listofQubits
    print('received from %s:%s' % addr)
    while True:
        date = sock.recv(2048)
        if not date or date.decode('utf-8') == 'exit':
            break
        operaCode = protocol.parse_request_operaCode(date)
        if operaCode == 4:
            _, receiveer_ip, receiver_port = protocol.parse_recvip_info(date)

        if operaCode == 0:
            pass
        if operaCode == 1:
            pass
        if operaCode == 2:
            _, num_of_qubits = protocol.parse_generate_qubits_request(date)
            listofBasis = qkd.generateRandomBasis(num_of_qubits)
            basisBytes=qkd.listtobytes(listofBasis)

            sock.send(b'length recv')
            qubitsbytes = sock.recv(3 * num_of_qubits + 256)
            print(qubitsbytes)
            print(len(qubitsbytes))



            sock.send(basisBytes)

            recvBasisB = sock.recv(num_of_qubits + 256)

            print(b"recvBasisB "+recvBasisB)

            # print(sock.recv(1024).decode())
            sock.send(b'Exchange successful')


        if operaCode == 3:
            pass

    sock.close()
    print(' %s:%s connection closed。。。。' % addr)


if __name__ == '__main__':
    # create a socket
    ss = socket(AF_INET, SOCK_STREAM)
    # bind port
    ss.bind(('', port))
    # listen port
    ss.listen(5)
    while True:
        sock, addr = ss.accept()
        # start a new thread to deal with TCP connect
        threading.Thread(target=tcplink, args=(sock, addr)).start()