import socket
import threading

HEADER = 64
# The first message is going to be always 64 bytes of length
# so we first receive a message with: "(num of bytes the msg) + padding to be 64"
# After that, we prepare the server for that num of bytes.
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Anything that hits ADDR will face a socket (due to the bind)
server.bind(ADDR)

# New thread to handle communication between all client and server


def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        #This is a blocking line - We wont pass it until we receive a message from
        # the client, main reason why we thread
        msg_length = conn.recv(HEADER).decode(FORMAT) #first message is the length. decode from byte format to utf8
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

    connected.close()

def start():
    # Our server starts to listen new connections
    server.listen()
    print(f"[LISTENING] Server is litening on {SERVER}")
    while True:
        #This line will wait for a new connection. When that occurs,
        # we will store the addr (IP and port) and conn (object to send back info to the connection)
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")


print("[STARTING] Server is starting...")
start()