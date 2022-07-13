import socket
from threading import Thread
from datetime import datetime

key = 8194 #ключ шифрование (лучше сделать, чтобы он равндомно генерировался, но я до конца не знаю как это работает)

# IP адресс сервера
# если сервер не на этйо машине, то 
# вписать приватный IP (напр. 192.168.1.2)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 # порт сервера
separator_token = "<SEP>" # разграничитель между именем и сообщением от клиента

# инициализация TCP сокета
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# подключение к серверу
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")
# просьба ввести клиента имени
name = input("Enter your name: ")

def listen_for_messages():
    while True:
        global key
        message = s.recv(1024).decode()
        decript_str = ""
        for letter in message:
            decript_str += chr(ord(letter) ^ key)
        print(decript_str)

# создание потока, который слушает сообщения и выводит их
t = Thread(target=listen_for_messages)
# создание потокового 'демона', который выключается тогда, когда выключается основной демон
t.daemon = True
# запуск потока
t.start()

while True:
    # ввод сообщения, которое мы хотим отправить
    to_send = input()
    # выход из программы
    if to_send.lower() == 'q':
        break
    # добавление даты и времени отправки сообщения
    date_now = datetime.now().strftime('%Y.%m.%d. %H:%M:%S') 
    to_send = f"[{date_now}] {name}{separator_token}{to_send}"
    encript_str = ""
    for letter in to_send:
        encript_str += chr( ord(letter) ^ key )
    #  отправка сообщения
    s.send(encript_str.encode())

# закрытие сокета
s.close()