import os
import socket
import tqdm

IP = '0.0.0.0'
port = 5300
IP_port = (IP, port)
buf = 4000

separator = "<separator>"
s = socket.socket()
s.bind(IP_port)
s.listen(2)

print(f'等待连接,在{port}监听')
client_socket, address = s.accept()
print("客户端连接：", address)

receive = client_socket.recv(buf).decode()
filename, fileSize = receive.split(separator)
filename = os.path.basename(filename)
fileSize = int(fileSize)
progress = tqdm.tqdm(range(fileSize), f'接受{filename}', unit="B", unit_divisor=1024)

with open(filename, 'wb') as f:
    for _ in progress:
        bytes_read = client_socket.recv(buf)
        if not bytes_read:
            break
        f.write(bytes_read)
        progress.update(len(bytes_read))

client_socket.close()
s.close()
