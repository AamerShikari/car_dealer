import socket
import select
import hashlib
import json
from urllib.parse import urlparse


class Blockchain:
    def __init__(self):
        self.chain = []  # blockchain
        self.transaction = []  # transaction to add to block
        self.users = []  # list of users
        #self.request = []
        self.car = []
        #self.money = []
        self.new_block("Tom", "tom123", "Ferrari", '0')
        self.add_user("Tom", "tom123", 10000)
        self.add_user("Jery", "jery456", 10000)

    def new_transaction(self, owner, car):
        self.transaction.append({
            'owner': owner,
            'car': car
        })
        return self.last_block['index'] + 1

    def new_block(self, username, password, car_value, previous_hash):
        block = {
            # 'index': len(self.chain) + 1,
            "user": username,
            "pword": password,
            'car': car_value,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        # add money or additional features
        self.transaction.append([username, car_value])

        #self.request = []
        #self.car = []
        self.chain.append(block)
        return block


    def add_user(self, username, password, money):
        self.users.append([username, password, money])

    def add_money(self, username, money):
        # money = receive_message(notified_socket)
        # money = int(money['data'].decode('utf-8'))

        for x in self.users:
            if username == x[0]:
                x[2] += money
        
        print(f"Added {money} to account")
        
    def remove_money(self, username, money):
        for x in self.users:
            if username == x[0]:
                x[2] -= money
        
        print(f"Added {money} to account")

    def add_car(self, car_value):
        self.car.append(car_value)

    def get_money(self, username):
        for x in self.users: 
            if x[0] == username:
                return x[2]
        print("User Not found")
        return 0;

    # validate chain by checking previous hashes
    def validate(self):
        previous_block = self.chain[0]
        counter = 1

        password = receive_message(notified_socket)
        password = password['data'].decode('utf-8')

        while counter < len(self.chain):
            current_block = self.chain[counter]
            previous_hash = self.hash(previous_block)
            if current_block['previous_hash'] != previous_hash:
                print(f"Incorrect previous_hash")
                # return False
            previous_block = current_block
            counter += 1

        if self.buyer_password() != password:
            print(f"Incorrect password")
            return False

        print(f"Purchase validated")
        return True

    def user_login(self, user, pword):
        username = user['data'].decode('utf-8')
        password = pword['data'].decode('utf-8')

        counter = 0
        new_user = True

        while counter < len(self.users):
            current_block = self.users[counter]
            if current_block[0] == username:
                new_user = False
                if current_block[1] != password:
                    print(f"Incorrect password")
                    return False
            counter += 1

        if new_user == True:
            self.add_user(username, password, 0)

        return True

    def remove_transaction(self):
        self.transaction.pop()
        self.chain.pop()

    @staticmethod
    def hash(block):
        block_hash = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_hash).hexdigest()

    def new_hash(self):
        last_block = self.last_block
        previous_hash = self.hash(last_block)
        return previous_hash
        
    @property
    def last_block(self):
        return self.chain[-1]

    def last_buyer(self):
        return self.chain[len(self.chain) - 1]['user']

    def buyer_password(self):
        print(f"{self.chain[len(self.chain) - 1]['pword']}")
        return self.chain[len(self.chain) - 1]['pword']

    def get_password(self, user):
        for x in self.users:
            if x[0] == user:
                return x[1]

    def print_blockchain(self):
        for x in self.chain:
            print(f"{x}")

    def print_users(self):
        for x in self.users:
            print(f"{x}")

    def users_string(self):
        us = ""
        counter = 1
        for x in self.users:
            us += f"{counter}: " + f"{x[0]} \n"
            counter+=1 
        return us

    def view_string(self):
        view = ""
        counter = 1
        for x in self.chain:
            view += f"{counter}: {x['user']}, {x['car']} \n"
            counter += 1
        return view

    def print_last(self):
        print(f"{self.chain[len(self.chain) - 1]}")



HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

# list of all sockets server interacts with (including server)
socket_list = [server_socket]


clients = {}  # individual client identifiers


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}

    except:
        return False


block = Blockchain()
seller = ""
buyer = ""
temp = ""
seller_id = 0
buyer_id = 0
temp_id = 0

while True:
    read_sockets, _, exception_sockets = select.select(
        socket_list, [], socket_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)
            if user is False:
                continue
            socket_list.append(client_socket)
            clients[client_socket] = user

            password = receive_message(client_socket)

            if block.user_login(user, password) == False:
                message = f""
                message = message.encode("utf-8")
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode(
                    "utf-8")
                client_socket.send(message_header + message)

                user = receive_message(client_socket)
                password = receive_message(client_socket)
            
            if user['data'].decode('utf-8') != block.last_buyer():
                buyer = user['data'].decode('utf-8')
                buyer_id = client_socket
            else:
                seller = user['data'].decode('utf-8')
                seller_id = client_socket

            message = f"Connection confirmed with user: {user['data'].decode('utf-8')}"
            message = message.encode("utf-8")
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}, password: {password['data'].decode('utf-8')}")
            client_socket.send(message_header + message)

            if seller == user['data'].decode('utf-8'):
                message = f"SELLER"
                message = message.encode("utf-8")
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
                client_socket.send(message_header + message)
            else:
                message = f"BUYER"
                message = message.encode("utf-8")
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
                client_socket.send(message_header + message)

        else:
            message = receive_message(notified_socket)

            if notified_socket == buyer_id:
                user = buyer
            elif notified_socket == seller_id:
                user = seller

            if message is False:
                print(
                    f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                socket_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            print(f"Received message from {user}: {message['data'].decode('utf-8')}")

            # if message['data'].decode('utf-8') == "PURCHASE":
            #     # if (block.last_block().decode('utf-8') != user['data'].decode('utf-8')):
            #     if block.last_buyer() != user['data'].decode('utf-8'):
            #         block.new_block(f"{user['data'].decode('utf-8')}",
            #                         f"{password['data'].decode('utf-8')}", "Ferarri", '0')
            #         if block.validate() == False:
            #             print(f"Invalid purchase")
            #             block.remove_transaction()
            #     else:
            #         print(f"You already own the Vehicle!")

            #     block.print_last()
            if message['data'].decode('utf-8') == "PURCHASE":
                #Buyer Insufficient Funds
                if block.get_money(buyer) <= 10000:
                    #send response to BUYER
                    request = f"Insufficient Funds."
                    request = request.encode("utf-8")
                    request_header = f"{len(request):<{HEADER_LENGTH}}".encode("utf-8")
                    buyer_id.send(request_header + request)
                    continue
                else:
                    #send response to BUYER
                    request = f"Sufficient Funds."
                    request = request.encode("utf-8")
                    request_header = f"{len(request):<{HEADER_LENGTH}}".encode("utf-8")
                    buyer_id.send(request_header + request)

                #send purchase to SELLER
                request = f"{buyer} would like to buy your car. Sell?"
                request = request.encode("utf-8")
                request_header = f"{len(request):<{HEADER_LENGTH}}".encode("utf-8")
                seller_id.send(request_header + request)

                #send purchase to BUYER
                request = f"Purchase request sent to {seller}"
                request = request.encode("utf-8")
                request_header = f"{len(request):<{HEADER_LENGTH}}".encode("utf-8")
                buyer_id.send(request_header + request)

                #receive SELLER response
                response = receive_message(seller_id)
                if response['data'].decode('utf-8') == "Y":
                    #send response to BUYER
                    request = f"Request approved. Please input password:"
                    request = request.encode("utf-8")
                    request_header = f"{len(request):<{HEADER_LENGTH}}".encode("utf-8")
                    buyer_id.send(request_header + request)

                    #send response to SELLER
                    request = f"Accepted request. Waiting for payment."
                    request = request.encode("utf-8")
                    request_header = f"{len(request):<{HEADER_LENGTH}}".encode("utf-8")
                    seller_id.send(request_header + request)

                    #receive payment from BUYER
                    response = receive_message(buyer_id)
                    print(f"{block.get_password(buyer)}")
                    if response['data'].decode('utf-8') == block.get_password(buyer):
                        previous_hash=block.new_hash()
                        block.new_block(f"{buyer}", f"{block.get_password(buyer)}", "Ferarri", previous_hash)
                        block.add_money(seller, 10000)
                        block.remove_money(buyer, 10000)

                        #send response to BUYER
                        request = f"Payment sent. You now own the car."
                        request = request.encode("utf-8")
                        request_header = f"{len(request):<{HEADER_LENGTH}}".encode("utf-8")
                        buyer_id.send(request_header + request)

                        #send response to SELLER
                        request = f"Payment received. The car has been sold."
                        request = request.encode("utf-8")
                        request_header = f"{len(request):<{HEADER_LENGTH}}".encode("utf-8")
                        seller_id.send(request_header + request)

                        temp = buyer
                        buyer = seller
                        seller = temp
                        temp = ""

                        temp_id = buyer_id
                        buyer_id = seller_id
                        seller_id = temp_id 
                        temp_id  = 0
                    else:
                        #send response to BUYER
                        request = f"Password incorrect. Purchase invalid."
                        request = request.encode("utf-8")
                        request_header = f"{len(request):<{HEADER_LENGTH}}".encode("utf-8")
                        buyer_id.send(request_header + request)

                        #send response to SELLER
                        request = f"Buyer invalid. Purchase incomplete."
                        request = request.encode("utf-8")
                        request_header = f"{len(request):<{HEADER_LENGTH}}".encode("utf-8")
                        seller_id.send(request_header + request)

                else:
                    #send response to BUYER
                    request = f"Request denied."
                    request = request.encode("utf-8")
                    request_header = f"{len(request):<{HEADER_LENGTH}}".encode("utf-8")
                    buyer_id.send(request_header + request)

                    #send response to SELLER
                    request = f"Rejected request. Car will not be sold."
                    request = request.encode("utf-8")
                    request_header = f"{len(request):<{HEADER_LENGTH}}".encode("utf-8")
                    seller_id.send(request_header + request)

            if message['data'].decode('utf-8') == "VIEW":
                uss = block.view_string()
                msg = uss.encode("utf-8")
                msg_header = f"{len(msg):<{HEADER_LENGTH}}".encode("utf-8")
                notified_socket.send(msg_header + msg)

                block.print_blockchain()

            if message['data'].decode('utf-8') == "USERS":
                uss = block.users_string()
                msg = uss.encode("utf-8")
                msg_header = f"{len(msg):<{HEADER_LENGTH}}".encode("utf-8")
                notified_socket.send(msg_header + msg)

                block.print_users()

            if message['data'].decode('utf-8') == "BALANCE":
                uss = f"Current Balance = {str(block.get_money(user))} \n"
                print (uss)
                msg = uss.encode("utf-8")
                msg_header = f"{len(msg):<{HEADER_LENGTH}}".encode("utf-8")
                notified_socket.send(msg_header + msg)
                

            if message['data'].decode('utf-8') == "ADD":
                money = receive_message(notified_socket)
                money = int(money['data'].decode('utf-8'))

                block.add_money(user, money)

            if message['data'].decode('utf-8') == "Q":
                print(
                    f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")

                socket_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            # Currently shows all clients messages that one has sent
            # for client_socket in clients:
            #     if client_socket != notified_socket:
            #         client_socket.send(
            #             user['header'] + user['data'] + message['header'] + message['data'])

        for notified_socket in exception_sockets:
            socket_list.remove(notified_socket)
            del clients[notified_socket]

'''
class users: 
    def __init__(self, name, hasCar):
        self.name = name
        self.hasCar = hasCar

list = []

list.append( users('Tom', False) )
list.append( users('John', True) )


for obj in list: 
    print (obj.name, obj.hasCar, sep=' ' )

class blockchain: 
    def __init__(self, name): 
        self.name = name

list.append(users[1].__name__)
list.append(users[0].__name__)

'''
