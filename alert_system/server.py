import socket

HOST = '0.0.0.0'
PORT = 11111
ALERT = False

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            if ALERT:
                conn.sendall(b'1')
