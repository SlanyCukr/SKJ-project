import socket

HOST = 'skaikru.cz'
PORT = 11111

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = s.recv(1024)

    print("Received alert...")
