import socket
from config import HOST, PORT
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

chats = dict()

def broadcast(msg, chat_name):
    for client, info in chats.items():
        if info['chat_name'] == chat_name:
            client.send(msg)

   
def handle_clients(client):
    while True:
        client_info = chats.get(client)
        try:
            msg = client.recv(1024)
            if client_info:
                chat_name = client_info.get('chat_name')
                broadcast(msg, chat_name=chat_name)
        except:
            client.close()
            if client_info:
                nickname = client_info.get('nickname')
                chat_name = client_info.get('chat_name')
                del chats[client]
                broadcast(f'{nickname} saiu da conversa!'.encode('utf-8'), 
                          chat_name=chat_name)
                break
  
def receive():
    while True:
        client, address = server.accept()
        print(f'Conectado com {str(address)}')
        
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        
        client.send('CHAT_NAME'.encode('utf-8'))
        chat_name = client.recv(1024).decode('utf-8')
        
        chats[client] = dict(
            chat_name = chat_name,
            nickname = nickname
        )
        
        print(f'Nome do cliente é {nickname}')
        broadcast(f'{nickname} acabou de entrar no chat'.encode('utf-8'), chat_name)
        client.send('Conectado com o servidor!'.encode('utf-8'))
        
        thread = threading.Thread(target=handle_clients, args=(client,))
        thread.start()
        
if __name__ == "__main__":
    print('Servidor escutando...')
    receive()