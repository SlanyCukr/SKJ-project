import socket
from threading import Thread
from time import sleep

from alert_system.db_utils import get_latest_article_id
from settings import get_settings

SETTINGS = get_settings()
HOST = '0.0.0.0'
PORT = SETTINGS["alert_server_port"]
ALERTS = {}
LATEST_ARTICLE_ID = None


def new_client(clientsocket, addr):
    ALERTS[addr] = False
    while True:
        sleep(5)
        if ALERTS[addr]:
            print(f'Sending alert to {addr}.')
            clientsocket.sendall(b'1')
            ALERTS[addr] = False
    del ALERTS[addr]
    clientsocket.close()


def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()

            print(f'New client {addr}.')

            client_thread = Thread(target=new_client, args=(conn, addr))
            client_thread.start()
        s.close()


def check_alerts():
    global LATEST_ARTICLE_ID

    while True:
        article_id = get_latest_article_id()
        if article_id != LATEST_ARTICLE_ID:
            for key in ALERTS.keys():
                ALERTS[key] = True
            LATEST_ARTICLE_ID = article_id
        sleep(5)


if __name__ == '__main__':
    print(f'Running alert server on {HOST}:{PORT}')

    run_server_thread = Thread(target=run_server)
    run_server_thread.start()

    check_alerts()
