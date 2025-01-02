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
    id = Column(Integer, primari_key=True, autoincrement=True)
    name = Column(String(250))
    address = Column(String)
    x = Column(Integer, defaulnt=500)
    y = Column(Integer, defaulnt=500)
    site = Column(Integer, defaulnt=50)
    errors = Column(Integer, defaulnt=0)
    abs_speed = Column(Integer, defaulnt=1)
    speed_x = Column(Integer, defaulnt=0)
    speed_y = Column(Integer, defaulnt=0)
    color = Column(String(250), default='red')
    w_vision = Column(Integer, defaulnt=800)
    h_vision = Column(Integer, defaulnt=600)

    def __init__(self, name, address):
        self.name = name
        self.address = address


Base.metadata.create_all(engine)
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
            id.send('g'.encode())
        except:
            players.remove(id)
            id.close()
            print('сокет закрыт')


    time.sleep(1)