from pydoc import cli
import socket
from time import sleep
import KVClient

def kvclient_test():
    client = KVClient(host="127.0.0.1", port=9900)
    command = ''
    print('''WELCOME TO A FUCKING KEY VALUE STORE!
SINCE YOU CANT DO THIS USING REDIS OR A PEN AND PAPER, I MADE THIS CODE TO HELP YOU STORE VALUES!
Here's what you can do:
        GET <key>
        PUT <key> <value>
        SCAN
        EXIT
    ''')
    while command != "EXIT":
        
        command = input("Enter a command:   ").split()
        match command[0]:
                case "PUT": 
                    client.put(command[1], command[2])
                    flag = 1
                case "GET": 
                    print(client.get(command[1]))
                case "SCAN": 
                    print(client.scan())
                case "EXIT":
                    break
    client.exit()

class KVClient():
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = socket.socket()
        self.socket.connect((self.host, self.port))

    def get(self, key: str):
        command = "GET " + key 
        self.socket.send(command.encode())
        result =  self.socket.recv(1024).decode()
        return result
        
    def put(self, key: str, value: str):
        """calls the server and returns the value of `key`"""
        command = "PUT " + key +" " + value
        self.socket.send(command.encode())
        sleep(1)
        print("Addition complete: "+key + ": " +value)
        sleep(1)
        result =  self.socket.recv(1024).decode()
        return result

    def scan(self):
        """
        implement an iterator that lists the entire contents of the
        remote kvstore
        """
        command = "SCAN"
        self.socket.send(command.encode())
        result = self.socket.recv(1024).decode()
        return result
        
    def exit(self):
        command = "EXIT"
        print("Exiting application")
        self.socket.send(command.encode())    

if __name__ == "__main__":
    kvclient_test()