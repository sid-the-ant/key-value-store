from cgitb import reset
import socket
import threading

def kv_server(file:str, port: int):
    serverObject = KVServer("store.txt", 9900)
    serverObject.server()
    
class KVServer:
    def __init__(self, path: str, port: str):
        self.port = port
        self.path = path
        self.store = open(path,  "r")
        self.dict = dict()
        self.read()
    def read(self):
        for line in self.store:
            a, b = line.split();
            self.dict[a] = b;
    
    def write(self):
        write_file = open(self.path, "w")
        for i,j in self.dict.items():
            write_file.write(i + " " + j +"\n")

    def put(self, key: str, val: str):
        self.dict[key] = val
        self.write()
        return key + " " + val
    

    def get(self, key:str):
        return self.dict[key]

    def scan(self):
        result = ''
        for i, j in self.dict.items():
            result += (i+ ": " + j + '\n')
        return result.strip()

    def threader(self, con: socket):
        command = con.recv(1024).decode().split()
        print(command)
        result = ''
        flag = 0
        match command[0]:
            case "PUT": 
                result =  self.put(command[1], command[2])
                flag = 1
            case "GET": 
                result = self.get(command[1])
            case "SCAN": 
                result = self.scan()
            case "EXIT":
                flag = -1
                return
        print(result)
        con.send(result.encode())
            

    def server(self):
        s= socket.socket()
        s.bind(('', self.port))
        s.listen()
        while True:
            con, addr = s.accept()
            t= threading.Thread(target=self.threader , args=[con,], daemon=True)
            t.start()
            # command = con.recv(1024).decode().split()
            # print(command)
            # result = ''
            # flag = 0
            # match command[0]:
            #     case "PUT": 
            #         result =  self.put(command[1], command[2])
            #         flag = 1
            #     case "GET": 
            #         result = self.get(command[1])
            #     case "SCAN": 
            #         result = self.scan()
            #     case "EXIT":
            #         flag = -1
            #         return
            # print(result)
            # con.send(result.encode())
            # if flag == 1:
            #     self.write()
            
            


if __name__ == "__main__":

    kv_server("store.txt", 9900)