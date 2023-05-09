import socket
import os
import tqdm


IP = '127.0.0.1'
port = 5300
buf = 4000

# 文件的基本信息
separator = "<separator>"
file = "test.txt"
fileSize = os.path.getsize(file)

# listen_socket = socket(AF_INET, SOCK_STREAM)
# communication = socket.socket()
s = socket.socket()
print(f'服务器在{port}等待连接')
s.connect((IP, port))
print("服务器连接成功")
# 将需要发送的信息进行解码
s.send(f"{file}{separator}{fileSize}".encode())
progress = tqdm.tqdm(range(fileSize), unit="B", unit_divisor=1024)

with open(file, 'rb') as f:
    for _ in progress:
        bytes_read = f.read(buf)
        if not bytes_read:
            break
        s.sendall(bytes_read)
        progress.update(len(bytes_read))
s.close()
