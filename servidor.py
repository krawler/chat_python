import socket
import threading
import sqlite3

HOST = '127.0.0.1'
PORT = 55556

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()
print('Server listening on: ' + str(PORT))

salas = {}

def broadcast(sala,mensagem):
    for i in salas[sala]:
        if isinstance(mensagem, str):
            mensagem = mensagem.encode()

        i.send(mensagem)

def enviar_mensagem(nome,sala,client):
    while True:
        mensagem = client.recv(1024)
        mensagem = f'{nome}: {mensagem.decode()}\n'
        broadcast(sala, mensagem)
        gravar_mensagem(sala, nome, mensagem)


def gravar_mensagem(sala, nome, mensagem):
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    row_log = 'SALA: ' + sala + ' NOME: ' + nome + ' MENSAGEM: ' + mensagem
    cursor.execute('insert into chat_log(log_content) values(?)', (row_log,))
    conn.commit()

while True:
    client, addr = server.accept()
    client.send(b'SALA')
    sala = client.recv(1024).decode()
    client.send(b'NOME')
    nome = client.recv(1024).decode()
    if sala not in salas.keys():
        salas[sala] = []

    salas[sala].append(client)
    print(f'{nome} se conectou na sala {sala}! INFO {addr}')
    broadcast(sala, f'{nome}: Entrou na sala!\n')
    thread_enviar = threading.Thread(target=enviar_mensagem,args=(nome,sala,client))
    thread_enviar.start()