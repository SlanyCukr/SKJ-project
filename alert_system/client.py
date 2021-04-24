import socket

HOST = 'localhost'
PORT = 1111


def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        print(f'Connected to {HOST}:{PORT}. Waiting for alerts...')

        while True:
            data = s.recv(1024)
            if data:
                print("Received alert...")


if __name__ == '__main__':
    run_client()
