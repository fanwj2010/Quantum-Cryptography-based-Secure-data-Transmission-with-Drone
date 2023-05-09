b=b'\x00'
print(b)
b+=b'\x00'
print(b)
print(b[1]==0)
print(len(b))
# 为tcpServer端写一个测试的client程序
# coding:utf-8
import os
import socket
# 第一步：创建一个socket
import time

import protocol

sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 第二步：建立连接
sc.connect(('127.0.0.1', 20001))
# 第三步：发送数据
# sc.send(b'hello World!')
# 第三步：接收数据
date = sc.recv(1024)  # b'had connected'
print(date.decode('utf-8'))

num_of_qubits = 1000

sc.send(protocol.make_generate_qubits_request(num_of_qubits))
qubitsbytes = sc.recv(3 * num_of_qubits + 256)
print(qubitsbytes)
print(len(qubitsbytes))

sc.send(b'Qubits received')

# receive ip
sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sc.connect(('127.0.0.1', 20001))
date = sc.recv(1024)
print(date.decode('utf-8'))
sc.send(protocol.make_recvip_info("127.0.0.1", 20002))

# exchange basis
sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sc.connect(('127.0.0.1', 20001))
date = sc.recv(1024)  # b'had connected'
print(date.decode('utf-8'))
sc.send(protocol.make_send_qubits_request())
print(sc.recv(1024).decode())
