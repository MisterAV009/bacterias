import socket
import pygame
import math
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

name = ''
color = ''


def login():
    global name
    name = row.get()
    if name and color:
        root.destroy()
        root.quit()
    else:
        tk.messagebox.showerror('ОШИБКА', 'ты не ввел имя или не выбрал цвет')


def scroll(event):
    global color
    color = combo.get()
    style.configure('TCombobox', fieldbackground=color, background='white')


root = tk.Tk()
root.title("Логин")
root.geometry("300x200")

style = ttk.Style()
style.theme_use('clam')

name_label = tk.Label(root, text="Введи свой никнейм:")
name_label.pack()

row = tk.Entry(root, width=30, justify="center")
row.pack()

color_label = tk.Label(root, text="Выбери цвет:")
color_label.pack()
colors = ['Maroon', 'DarkRed', 'FireBrick', 'Red', 'Salmon', 'Tomato', 'Coral', 'OrangeRed', 'Chocolate', 'SandyBrown',
          'DarkOrange', 'Orange', 'DarkGoldenrod', 'Goldenrod', 'Gold', 'Olive', 'Yellow', 'YellowGreen', 'GreenYellow',
          'Chartreuse', 'LawnGreen', 'Green', 'Lime', 'SpringGreen', 'MediumSpringGreen', 'Turquoise',
          'LightSeaGreen', 'MediumTurquoise', 'Teal', 'DarkCyan', 'Aqua', 'Cyan', 'DeepSkyBlue',
          'DodgerBlue', 'RoyalBlue', 'Navy', 'DarkBlue', 'MediumBlue']

combo = ttk.Combobox(root, values=colors, textvariable=color)
combo.bind("<<ComboboxSelected>>", scroll)
combo.pack()

name_btn = tk.Button(root, text="Зайти в игру", command=login)
name_btn.pack()

root.mainloop()

pygame.init()

sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # выбираем семейство адресов IPv4,тип сокета TCP
sockets.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # откл. пакетирование,чтобы не портить фпс
sockets.connect(("localhost", 10000))  # привязываем айпи адрес и порт
sockets.send(f'color:<{name},{color}>'.encode())


def draw_text(x, y, r, text, color):
    font = pygame.font.Font(None, r)
    text = font.render(text, True, color)
    rect = text.get_rect(center=(x, y))
    screen.blit(text, rect)


WIDTH = 800
HEIGHT = 600
CC = (WIDTH // 2, HEIGHT // 2)
radius = 100
old = (0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Бактерии')

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if pygame.mouse.get_focused():
            pos = pygame.mouse.get_pos()

            vector = pos[0] - CC[0], pos[1] - CC[1]
            lenv = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
            vector = vector[0] / lenv, vector[1] / lenv
            if lenv <= radius:
                vector = (0, 0)
            if vector != old:
                old = vector
                msg = f'<{vector[0]},{vector[1]}>'
                sockets.send(msg.encode())
            print(vector)
    data = sockets.recv(1024).decode()
    print(data)
    screen.fill("gray")
    pygame.draw.circle(screen, color, CC, radius)
    draw_text(CC[0], CC[1], radius // 2, name, 'blue')
    pygame.display.update()
    print('ядерка летит')

pygame.quit()
