import os
import struct
import sys
from socket import *


def socket_service():
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
#     问题： 树莓派无法和电脑建立TCP通信连接
#     解决方法： 新建测试文件
# 树莓派 客户端 向 电脑发送图片
    while True:
        sock, addr = s.accept()
        deal_data(sock, addr)
        break
    s.close()
    print("photo is well received")


def deal_data(sock, addr):
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
    socket_service()
