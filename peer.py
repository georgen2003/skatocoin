import socket
from _thread import *
import os
import hashlib
import threading
import re

'''
1. append to string
2. connect to peers
3. broadcast append operation (update object on all other peers)
'''

class Peer():
    
    def __init__(self):
        
        self.peers = {}
        # self.init_client() maybe not needed in __init__()
        self.thread_server = threading.Thread(target = self.init_server)
        self.thread_server.start()
        
        # the "blockchain"
        self.chain = ""
        return
        
    def init_client(self):
        self.client = socket.socket()
        self.client.settimeout(.5)
        return
        
    def init_server(self):
        
        self.server = socket.socket()
        # gets local IP of machine
        hostname = socket.gethostname()
        self.ip = SERVER_HOST = socket.gethostbyname(hostname)
        SERVER_PORT = 5001
        self.server.bind((SERVER_HOST, SERVER_PORT))
        self.server.listen(10)
        self.id = self.gen_id(self.ip)
        self.peers.update({self.id:self.ip})
        print("Node ID: " + self.id)
        print(f"Listening at {SERVER_HOST}:{SERVER_PORT}...\n")
        
        while True:
            client_socket, client_address = self.server.accept()
            thread = threading.Thread(target = self.new_client, args = (client_socket, client_address))
            thread.start()
            
    def new_client(self, socket: socket, address):
        
        self.peers.update({self.gen_id(address[0]):address[0]})
        
        # size of incoming message (2**size)
        # size up to 2**9 --> 512 bytes
        size = socket.recv(1).decode('utf-8')
        
        if size and address[0] != self.ip:
            message = socket.recv(2**int(size)).decode('utf-8')
            self.chain += message
        
        print(self.chain)
        
        return
    
    def gen_id(self, ip):
        id = hashlib.sha256(ip.encode('utf-8')).hexdigest()
        return id
    
    def connect(self, address):
        
        # opens but does not close socket
        self.init_client()
        
        rgx = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
       
        if(not re.search(rgx, address)):
            print("Invalid address")
            return
        
        id = self.gen_id(address)
        try:
            self.client.connect((address, 5001))
            
        except socket.timeout:
            print("Error: Connection to node " + address + " could not be established")
            if id in self.peers:
                del self.peers[id]
            
        else:
            if id not in self.peers:
                self.peers.update({id:address})
                
        return
    
    def add_block(self, block):
        
        self.chain += block
        
        size = self.get_size(len(block.encode('utf-8')))
        
        for p in self.peers:
            self.connect(self.peers[p])
            self.client.send(str(size).encode())
            self.client.send(block.encode("utf-8"))
            self.client.close()
        return

    def get_size(self, n):
        
        x = 1
        while (x < n):
            x = x << 1
            
        return x