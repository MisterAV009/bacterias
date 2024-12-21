import socket

sockets = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # выбираем семейство адресов IPv4,тип сокета TCP
sockets.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1) # откл. пакетирование,чтобы не портить фпс
sockets.connect(("localhost",10000)) # привязываем айпи адрес и порт
while True:
    sockets.send('ok'.encode())
    data = sockets.recv(1024).decode()
    print(data)