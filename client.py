import socket
import threading
from tkinter import *
import tkinter
from tkinter import simpledialog

class Chat:

    def __init__(self):
        HOST = '127.0.0.1'
        PORT = 55556
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        login = Tk()
        login.withdraw()

        self.janela_carregada = False
        self.ativo = True

        self.sala = simpledialog.askstring('Nome','Digite a sala que deseja entrar:', parent=login)
        self.nome = simpledialog.askstring('Nome', 'Digite seu nome:', parent=login)

        thread = threading.Thread(target=self.conecta)
        thread.start()

        self.janela()

    def janela(self):
        self.root = Tk()
        self.root.geometry('800x800')
        self.root.title('Chat')

        self.label_sala = Label(self.root, text='Sala: ' + self.sala, font=('Arial', 20))
        self.label_sala.place(relx=0.02, rely=0.03, width=200, height=30)

        self.caixa_texto = Text(self.root)
        self.caixa_texto.place(relx=0.05, rely=0.1, width=700, height=500)

        self.mensagem_enviar = Entry(self.root)
        self.mensagem_enviar.place(relx=0.05, rely=0.8, width=500, height=20)

        self.btn_enviar = Button(self.root, text='Enviar', command=self.enviar_mensagem)
        self.btn_enviar.place(relx=0.7, rely=0.8, width=100, height=20)
        self.root.protocol('WM_DELETE_WINDOW', self.fechar)

        self.root.mainloop()
        exit(self.root)

    def fechar(self):
        self.root.destroy()
        self.client.close()

    def conecta(self):
        while True:
            recebido = self.client.recv(1024)
            if recebido == b'SALA':
                self.client.send(self.sala.encode())
            elif recebido == b'NOME':
                self.client.send(self.nome.encode())
            else:
                try:
                    self.caixa_texto.insert('end', recebido.decode())
                except:
                    pass

    def enviar_mensagem(self):
        mensagem = self.mensagem_enviar.get()
        self.client.send(mensagem.encode())
        self.mensagem_enviar.delete(0, END)
        self.mensagem_enviar.focus()

chat = Chat()

