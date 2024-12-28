import socket
import pygame

pygame.init()

sockets = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # выбираем семейство адресов IPv4,тип сокета TCP
sockets.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1) # откл. пакетирование,чтобы не портить фпс
sockets.connect(("localhost",10000)) # привязываем айпи адрес и порт


WIDTH = 800
HEIGHT = 600
CC = (WIDTH // 2,HEIGHT // 2)
radius = 100
old = (0,0)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Бактерии')

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if pygame.mouse.get_focused():
            pos = pygame.mouse.get_pos()

            vector = pos[0] - CC[0],pos[1] - CC[1]
            if vector != old:
                old = vector
                msg = f'<{vector[0]},{vector[1]}>'
                sockets.send(msg.encode())
    data = sockets.recv(1024).decode()
    print(data)
    screen.fill("gray")
    pygame.draw.circle(screen, (255, 0, 0), CC, radius)
    pygame.display.update()

pygame.quit()