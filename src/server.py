import socket
from config import HOST, PORT
import threading
    
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

chats = dict()

def broadcast(msg, chat_name):
    chat = chats.get(chat_name)
    if not chat:
        return
    for client, _ in chat.items():
        if isinstance(client, socket.SocketType):
            client.send(msg)

   
def handle_clients(client, chat_name):
    while True:
        chat = chats.get(chat_name)
        if chat:
            try:
                msg = client.recv(1024)
                broadcast(msg, chat_name=chat_name)
            except:
                nickname = chat.get(client)
                broadcast(f'{nickname} saiu da conversa!'.encode('utf-8'), 
                            chat_name=chat_name)
                del chats[chat_name][client]                
                client.close()
                break
  
def receive():
    while True:
        client, address = server.accept()
        print(f'Conectado com {str(address)}')
        
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        
        client.send('CHAT_NAME'.encode('utf-8'))
        chat_name = client.recv(1024).decode('utf-8')
        
        chat = chats.get(chat_name)
        if chat:
            chat.update({client: nickname})
        else:
            chats[chat_name] = {client: nickname}
        
        print(f'Nome do cliente é {nickname}')
        broadcast(f'{nickname} acabou de entrar no chat'.encode('utf-8'), chat_name)
        client.send('Conectado com o servidor!'.encode('utf-8'))
        
        thread = threading.Thread(target=handle_clients, args=(client, chat_name))
        thread.start()
        
        
if __name__ == "__main__":
    print('Servidor escutando...')
    receive()