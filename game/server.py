import socket
import time
import psycopg2
from sqlalchemy import create_engine,Column,String,Integer
from sqlalchemy.orm import declarative_base,sessionmaker


engine = create_engine('postgresql+psycopg2://postgres:1@localhost/bacterias')
Base = declarative_base()
Session = sessionmaker(bind=engine)
s = Session()


main_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # выбираем семейство адресов IPv4,тип сокета TCP
main_socket.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1) # откл. пакетирование,чтобы не портить фпс
main_socket.bind(("localhost",10000)) # привязываем айпи адрес и порт
main_socket.setblocking(False) # непрерывность, сервер не ждет ответ от клиента
main_socket.listen(5) # прослушка 5 одновременных соединений
print('cокет подключен')


class Player(Base):
    __tablename__ = "gamers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250))
    address = Column(String)
    x = Column(Integer, default=500)
    y = Column(Integer, default=500)
    site = Column(Integer, default=50)
    errors = Column(Integer, default=0)
    abs_speed = Column(Integer, default=1)
    speed_x = Column(Integer, default=0)
    speed_y = Column(Integer, default=0)
    color = Column(String(250), default='red')
    w_vision = Column(Integer, default=800)
    h_vision = Column(Integer, default=600)

    def __init__(self, name, address):
        self.name = name
        self.address = address


class LocalPlayer:
    def __init__(self, id, name, sock, addr):
        self.id = id
        self.db: Player = s.get(Player, self.id)
        self.sock = sock
        self.name = name
        self.address = addr
        self.x = 500
        self.y = 500
        self.size = 50
        self.errors = 0
        self.abs_speed = 1
        self.speed_x = 0
        self.speed_y = 0
        self.color = "red"
        self.w_vision = 800
        self.h_vision = 600



Base.metadata.create_all(engine)
players = {}

while True:
    try:
        new_sock,addr = main_socket.accept()
        print(new_sock,addr)
        new_sock.setblocking(False)
        player = Player('bob',addr)
        s.merge(player)
        s.commit()
        addr = f'({addr[0]},{addr[1]})'
        data = s.query(Player).filter(Player.address == addr)
        for user in data:
            player = LocalPlayer(user.id,'bob',new_sock,addr)
            players[user.id] = player
    except BlockingIOError:
        pass
    for id in list(players):
        try:
            data = players[id].sock.recv(1024).decode()
            print(data)
        except:
            pass
    for id in list(players):
        try:
            players[id].sock.send('g'.encode())
        except:
            del players[id]
            players[id].sock.close()
            print('сокет закрыт')


    time.sleep(1)