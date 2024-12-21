import socket

main_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # выбираем семейство адресов IPv4,тип сокета TCP
main_socket.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1) # откл. пакетирование,чтобы не портить фпс
main_socket.bind(("localhost",10000)) # привязываем айпи адрес и порт
main_socket.setblocking(False) # непрерывность, сервер не ждет ответ от клиента
main_socket.listen(5) # прослушка 5 одновременных соединений
print('cокет подключен')
players = []

while True:
    try:
        new_sock,addr = main_socket.accept()
        print(new_sock,addr)
        new_sock.setblocking(False)
        players.append(new_sock)
    except BlockingIOError:
        pass
    for id in players:
        try:
            data = id.recv(1024).decode()
            print(data)
        except:
            pass
    for id in players:
        try:
            id.send('no ok'.encode())
        except:
            pass