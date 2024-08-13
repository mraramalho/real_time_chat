import socket
from config import HOST, PORT
import threading
import customtkinter as ctk
import tkinter
import secrets
from tkinter import messagebox, simpledialog

class Chat(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        
        self.chat_window: ChatWindow | None = None
        
        self.title('Secret Chat')
        self.geometry("200x100")
        
        self.nickname = ctk.CTkInputDialog(text="Escolha seu apelido", title="Nickname").get_input()
        self.chat_name = ctk.CTkInputDialog(text="Digite o nome do chat que deseja criar", title="Chat Name").get_input()
        
        self.new_chat_btn = ctk.CTkButton(self, text="Novo chat", command=self.handle_new_chat)
        self.new_chat_btn.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()
        
        self.grid_columnconfigure(0, weight=1)
        self.mainloop()
        
    def handle_new_chat(self):
        self.chat_window = ChatWindow()
        self.chat_window.title(self.chat_name)
        self.destroy()
        self.chat_window.protocol("VW_DELETE_WINDOW", self.handle_close_conn)
        self.chat_window.mainloop()
              
    def handle_close_conn(self):
        if self.chat_window:
            self.chat_window.destroy()
            self.client.close()
        
    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode()
                if message == 'NICK':
                    self.client.send(str(self.nickname).encode('utf-8'))
                elif message == 'CHAT_NAME':
                    self.client.send(str(self.chat_name).encode('utf-8'))
                else:
                    if message not in ('NICK', 'CHAT_NAME', '') and self.chat_window:
                        self.chat_window.handle_receive_msg(message)
            except Exception as e:
                print('Ocorreu um erro: ', e)
                self.client.close()
                break
                    
    def write(self):
        while True:
            if self.chat_window:
                msg = self.chat_window.msg
                if msg == '':
                    continue
                message = f'{self.nickname}: {msg}'
                self.client.send(message.encode('utf-8'))
                self.chat_window.msg = ''

class ChatWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.msg = ''
        
        self.title('Chat')
        self.geometry('500x670')
        
        self.txt_log = tkinter.Text(
            master=self,
            wrap=tkinter.WORD,
            bg="#343638",
            fg="#ffffff",
            padx=20,
            pady=5,
            spacing1=4,  # spacing before a line
            spacing3=4,  # spacing after a line / wrapped line
            cursor="arrow",
        )
        self.txt_log.grid(row=1, column=0, padx=(15, 0), pady=(15, 15), sticky="nsew", columnspan = 2)
        self.txt_log.configure(state=tkinter.DISABLED)

        # Scrollbar
        self.scrollbar = ctk.CTkScrollbar(master=self, command=self.txt_log.yview)
        self.scrollbar.grid(row=1, column=2, padx=(0, 15), pady=(15, 15), sticky="ns")

        # Connect textbox scroll event to scrollbar
        self.txt_log.configure(yscrollcommand=self.scrollbar.set)
        
        self.entry = ctk.CTkEntry(self, placeholder_text="Digite uma mensagem")
        self.entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        self.send_btn = ctk.CTkButton(self, text="enviar", command=self.handle_send_msg)
        self.send_btn.grid(row=2, column=1, padx=10, pady=10, columnspan=2)
        
        self.grid_columnconfigure(0, weight=1)
        
    
    def handle_send_msg(self):
        msg = self.entry.get()
        self.txt_log.configure(state=tkinter.NORMAL)
        self.txt_log.configure(state=tkinter.DISABLED)
        self.txt_log.see(tkinter.END)
        self.entry.delete(0, tkinter.END)
        self.msg = msg
        
    def handle_receive_msg(self, msg):
        self.txt_log.configure(state=tkinter.NORMAL)
        self.txt_log.insert(tkinter.END, "\n" + msg)
        self.txt_log.configure(state=tkinter.DISABLED)
        self.txt_log.see(tkinter.END)   
            
# Start threads for receiving and sending messages
if __name__ == '__main__':
    chat = Chat()