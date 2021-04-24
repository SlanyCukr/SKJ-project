import socket
from time import sleep
import RPi.GPIO as GPIO

from alert_system.led_control import flash

HOST = 'localhost'
PORT = 1111

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
buzzer = 23
GPIO.setup(buzzer, GPIO.OUT)


def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        print(f'Connected to {HOST}:{PORT}. Waiting for alerts...')

        while True:
            data = s.recv(1024)
            if data:
                print("Received alert...")
                flash()
                for i in range(10):
                    GPIO.output(buzzer, GPIO.HIGH)
                    sleep(0.25)
                    GPIO.output(buzzer, GPIO.LOW)
                    sleep(0.25)


if __name__ == '__main__':
    run_client()
