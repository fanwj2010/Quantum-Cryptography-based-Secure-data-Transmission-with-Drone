from socket import *
import os
import sys
import struct
import time


def sock_client():
    time.sleep(8)
    try:
        s = socket(AF_INET, SOCK_STREAM)
        # 改成服务器IP
        s.connect(('192.168.56.1', 6666))
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
        fhead = struct.pack(b'128sl', bytes(os.path.basename(filepath), encoding='utf-8'), os.stat(filepath).st_size)
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


if __name__ == '__main__':

    sock_client()
