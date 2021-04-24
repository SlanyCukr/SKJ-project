import socket

HOST = '0.0.0.0'
PORT = 1111
ALERT = False


def run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)

            global ALERT
            if ALERT:
                conn.sendall(b'1')
                ALERT = False


if __name__ == '__main__':
    run()
