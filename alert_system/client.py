import socket

HOST = 'skaikru.cz'
PORT = 1111


def run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(1024)
        if data:
            print("Received alert...")


if __name__ == '__main__':
    run()
