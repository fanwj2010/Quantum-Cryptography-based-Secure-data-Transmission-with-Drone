import socket

address = ('127.0.0.1', 31500)

def receiving():
    drone_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # s = socket.socket()
    drone_s.bind(address)
    drone_s.listen(5)
    ss, addr = drone_s.accept()

    command = ss.recv(512)
    if command == "0":
        print(0)
    if command == "1":
        print(1)

    ss.send("0".encode())

