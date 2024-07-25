import socket
from config import HOST, PORT
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

chat_name = input('Digite o chat em que quer entrar: '),
nickname = input('Digite o seu apelido')

def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == 'NICK':
                client.send(str(nickname).encode('utf-8'))
            elif message == 'CHAT_NAME':
                client.send(str(chat_name).encode('utf-8'))
            else:
                if message not in ('NICK', 'CHAT_NAME', ''):
                    print('>>> ', message)
        except Exception as e:
            print('Ocorreu um erro: ', e)
            client.close()
            break

                
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))

# Start threads for receiving and sending messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
    