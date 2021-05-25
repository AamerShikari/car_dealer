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
#client_socket.setblocking(False) #sets receive blocking to false -> can receive 

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

status = ""
message_header = client_socket.recv(HEADER_LENGTH)
message_length = int(message_header.decode("utf-8").strip())
message = client_socket.recv(message_length).decode("utf-8")
print(f"Server > Welcome {message}")
status = message

while True:

    message = input(f"{my_username} > ")

    if message == "USERS" or message == "BALANCE" or message == "HISTORY" or message == "VIEW" or message == "AVAILABLE":

        #sending purchase request
        message = message.encode("utf-8")
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)

        #receive SELLER response
        message_header = client_socket.recv(HEADER_LENGTH)
        message_length = int(message_header.decode("utf-8").strip())
        message = client_socket.recv(message_length).decode("utf-8")
        print(f"{message}")


    elif message == "PURCHASE" and status == "BUYER":
        #sending purchase request
        message = message.encode("utf-8")
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)

        #receive request confirmation
        message_header = client_socket.recv(HEADER_LENGTH)
        message_length = int(message_header.decode("utf-8").strip())
        message = client_socket.recv(message_length).decode("utf-8")
        print(f"Server > {message}")
        if message == "Insufficient Funds.":
            continue

        #receive request confirmation
        message_header = client_socket.recv(HEADER_LENGTH)
        message_length = int(message_header.decode("utf-8").strip())
        message = client_socket.recv(message_length).decode("utf-8")
        print(f"Server > {message}")

        #receive SELLER response
        message_header = client_socket.recv(HEADER_LENGTH)
        message_length = int(message_header.decode("utf-8").strip())
        message = client_socket.recv(message_length).decode("utf-8")
        print(f"Server > {message}")

        if message != "Request denied.":
            #input password to pay
            message = input(f"{my_username} > ")
            message = message.encode("utf-8")
            message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
            client_socket.send(message_header + message)

            #receive purchase confirmation or error
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length).decode("utf-8")
            print(f"Server > {message}")

            if message != "Password incorrect. Purchase invalid.":
                status = "SELLER"
                print(f"You are now a seller.")

    elif message == "PURCHASE" and status == "SELLER":
        print(f"Server > You already own the car.")
    elif message == "SELL" and status == "SELLER":
        print(f"Waiting for a buyer...")

        #receive BUYER request
        message_header = client_socket.recv(HEADER_LENGTH)
        message_length = int(message_header.decode("utf-8").strip())
        message = client_socket.recv(message_length).decode("utf-8")
        print(f"Server > {message}")

        #send decision 
        message = input(f"{my_username} > ")
        message = message.encode("utf-8")
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)

        #receive decision confirmation
        message_header = client_socket.recv(HEADER_LENGTH)
        message_length = int(message_header.decode("utf-8").strip())
        message = client_socket.recv(message_length).decode("utf-8")
        print(f"Server > {message}")

        #receive purchase confirmation or error
        message_header = client_socket.recv(HEADER_LENGTH)
        message_length = int(message_header.decode("utf-8").strip())
        message = client_socket.recv(message_length).decode("utf-8")
        print(f"Server > {message}")

        if message != "Buyer invalid. Purchase incomplete.":
            status = "BUYER"
            print(f"You are now a buyer.")
    elif message == "SELL" and status == "BUYER":
        print(f"You have no cars to sell.")
    elif message == "ADD":
        #sending deposit request
        message = message.encode("utf-8")
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)

        #enter amount to deposit
        print(f"Server > Enter amount:")
        message = input(f"{my_username} > ")
        message = message.encode("utf-8")
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)
    elif message == "Q":
        print(f"Quit")
        sys.exit()
    else:
        message = message.encode("utf-8")
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)

        
        

# while True: 
#     message = input(f"{my_username} > ")

#     if message: 
#         if message == "PURCHASE":
#             print(f"Server > Please enter your password:")
#         if message == "Q":
#            
#         message = message.encode("utf-8")
#         message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
#         client_socket.send(message_header + message)
        
#     try:
#         while True: 
#             #receive things 
#             #Setup the username length and data
#             username_header = client_socket.recv(HEADER_LENGTH)
#             if not len(username_header):
#                 print("connection closed by the server")
#                 sys.exit()
#             username_length = int(username_header.decode("utf-8").strip())
#             username = client_socket.recv(username_length).decode("utf-8")

#             #Setup the message length and header 
#             message_header = client_socket.recv(HEADER_LENGTH)
#             message_length = int(message_header.decode("utf-8").strip())
#             message = client_socket.recv(message_length).decode("utf-8")

#             print(f"{username} > {message}")
    
#     except IOError as e: 
#         if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
#             print('Reading error', str(e))
#             sys.exit()
#         continue 

#     except Exception as e: 
#         print('General error', str(e))
#         sys.exit()