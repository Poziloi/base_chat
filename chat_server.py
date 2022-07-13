import socket
from threading import Thread

# IP сервера
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002 # порт, который будет использоваться
separator_token = "<SEP>" # разграничитель между именем и сообщением от клиента

# создание set'а для подключенных пользователь
client_sockets = set()
# создание TCP сокета
s = socket.socket()
# создание порта, который можно переиспользовать
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# связка сокета с адресом
s.bind((SERVER_HOST, SERVER_PORT))
# прослушивание входящих подключений (поскольку диалог, то 2)
s.listen(2)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(cs):
    """
    Эта функция продолжает слушать сообщение из 'cs' сокета
    Однако, когда сообщение получено, оно рассылается всем подключенным пользователям
    """
    while True:
        try:
            # продолжаем прослушивать сообщения из `cs` сокета
            msg = cs.recv(1024).decode()
            print(msg)
        except Exception as e:
            # клиент больше не подключен
            # удаления из set'а
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            # если было полученно сообщение, то заменается на <SEP> 
            # ": " для красивой печати
            msg = msg.replace(separator_token, ": ")
        # итерируем все подключенные сокеты
        for client_socket in client_sockets:
            # и отправляем сообщения
            client_socket.send(msg.encode())


while True:
    # постоянное прослушивание новых подключений
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    # добавление нового подклбченного клиента к сокету
    client_sockets.add(client_socket)
    # запуск потока, который слушает каждого клиентское сообщение
    t = Thread(target=listen_for_client, args=(client_socket,))
    # создание потокового 'демона', который выключается тогда, когда выключается основной демон
    # запуск потоков
    t.start()

# закрытие клиентского сокета
for cs in client_sockets:
    cs.close()
# закрытие серверного сокета
s.close()