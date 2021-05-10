import socket 
import select 
import errno 
import sys
import time


HEADER_LENGTH = 10 

IP = "127.0.0.1"
PORT = 1234

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False) #sets receive blocking to false -> can receive 

message = ""

while message == "":
    my_username = input("Username: ") 
    username = my_username.encode("utf-8")
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
    client_socket.send(username_header + username)

    my_password = input("Password: ") 
    password = my_password.encode("utf-8")
    password_header = f"{len(password):<{HEADER_LENGTH}}".encode("utf-8")
    client_socket.send(password_header + password)

    time.sleep(1)

    message_header = client_socket.recv(HEADER_LENGTH)
    message_length = int(message_header.decode("utf-8").strip())
    message = client_socket.recv(message_length).decode("utf-8")
    if message == "":
        print(f"Server > Incorrect password")
print(f"Server > {message}")

while True: 
    message = input(f"{my_username} > ")

    if message: 
        if message == "PURCHASE":
            print(f"Server > Please enter your password:")
        if message == "Q":
            print(f"Quit")
            sys.exit()
        message = message.encode("utf-8")
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)
        
    try:
        while True: 
            #receive things 
            #Setup the username length and data
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("connection closed by the server")
                sys.exit()
            username_length = int(username_header.decode("utf-8").strip())
            username = client_socket.recv(username_length).decode("utf-8")

            #Setup the message length and header 
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length).decode("utf-8")

            print(f"{username} > {message}")
    
    except IOError as e: 
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue 

    except Exception as e: 
        print('General error', str(e))
        sys.exit()