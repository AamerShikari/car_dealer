import socket 
import select 
import hashlib
import json
from urllib.parse import urlparse

class Blockchain:
    def __init__(self):
        self.chain = []  # blockchain
        self.transaction = []  # transaction to add to block
        self.users = [] #list of users
        #self.request = []
        self.car = []
        #self.money = []
        self.new_block("Tony", "tony123", "Ferrari", '0')
        self.new_user("Tony", "tony123")

    def new_block(self, username, password, car_value, previous_hash):
        block = {
            #'index': len(self.chain) + 1,
            "user": username,
            "pwrd": password,
            'car': car_value,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        self.transaction.append([username, car_value]) #add money or additional features 

        #self.request = []
        #self.car = []
        self.chain.append(block)
        return block

    def new_user(self, username, password):
        self.users.append([username, password])

    def add_car(self, car_value):
        self.car.append(car_value)

    # validate chain by checking previous hashes
    def validate(self):
        previous_block = self.chain[0]
        counter = 1

        while counter < len(self.chain):
            current_block = self.chain[counter]
            previous_hash = self.hash(previous_block)
            if current_block['previous_hash'] != previous_hash:
                return False
            previous_block = current_block
            counter += 1
        return True

    def check_user(self, user, pword):
        username = user['data'].decode('utf-8')
        password = pword['data'].decode('utf-8')

        found = False

        for x in self.users:
            if x[0] == username:
                found = True
                if x[1] == password:
                    return True
                else:
                    print(f"Incorrect password.")
                    return False

        if found == False:
            self.users.append([username, password])
            return True

    def valid_buyer(self, user):
        username = user['data'].decode('utf-8')
        print(f"Current user: {username}")

        password = receive_message(notified_socket)

        print(f"{self.chain[len(self.chain)-1]['user']}")
        if self.chain[len(self.chain)-1]['user'] == username:
            print(f"You already own the vehicle!")
            return False

        for x in self.chain:
            if x['user'] == username:
                pwrd = password['data'].decode('utf-8')
                if x['pwrd'] != pwrd:
                    print(f"Incorrect password.")
                    print(f"Purchase invalid.")
                    return False
        
        if self.check_user(user, password) is False:
            print(f"Purchase invalid.")
            return False


        print(f"Purchase valid. You now own the vehicle.")
        return True

    def new_transaction(self, owner, car):
        self.transaction.append({
            'owner': owner,
            'car': car
        })
        return self.last_block['index'] + 1

    def remove_transaction(self):
        self.transaction.pop()
        self.chain.pop()


	
    @staticmethod
    def hash(block):
        block_hash = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_hash).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def print_blockchain(self):
        for x in self.chain: 
            print (f"{x}")

    def print_users(self):
        for x in self.users:
            print (f"{x}")

    def print_last(self):
        print (f"{self.chain[len(self.chain) - 1]}")




HEADER_LENGTH = 10 
IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

socket_list = [server_socket] #list of all sockets server interacts with (including server) 


clients = {} #individual client identifiers 


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

while True: 
    read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list)  

    for notified_socket in read_sockets: 
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)
            if user is False:
                continue
            socket_list.append(client_socket)

            password = receive_message(client_socket)
            clients[client_socket] = user

            if block.check_user(user, password) is True:
                message = f"Connection confirmed with user: {user['data'].decode('utf-8')}"
                message = message.encode("utf-8")
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
                print (f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}, password: {password['data'].decode('utf-8')}")
                client_socket.send(message_header + message)

        else: 
            message = receive_message(notified_socket)

            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                socket_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]

            print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            if message['data'].decode('utf-8') == "PURCHASE":
                #if (block.last_block().decode('utf-8') != user['data'].decode('utf-8')):
                if block.valid_buyer(user) == True:
                    block.new_block(f"{user['data'].decode('utf-8')}", f"{password['data'].decode('utf-8')}", "Ferarri", '0')
                
                block.validate()
                #print(f"You already own the Vehicle!")
                block.print_last()

            if message['data'].decode('utf-8') == "VIEW":
                block.print_blockchain() 

            if message['data'].decode('utf-8') == "USERS":
                block.print_users() 
            

            #Currently shows all clients messages that one has sent 
            for client_socket in clients: 
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

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