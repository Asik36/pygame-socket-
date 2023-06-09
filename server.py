import socket 
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
client_list = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    username = recv(conn)
    client_list.append((conn, addr, username))

    while connected:
        msg = recv(conn)
        resend(msg, addr)

        print(f"[{username}] {msg}")
        if msg == DISCONNECT_MESSAGE:
            connected = False            
    conn.close()

def send(msg,conn):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))  
    conn.send(send_length)
    conn.send(message)
    
def resend(msg, addr):
    for i in client_list:
        if i[1] != addr:
            send(msg,i[0])

def recv(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        
        return msg

def accept_loop():
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    accept_loop()
    

print("[STARTING] server is starting...")
start()
