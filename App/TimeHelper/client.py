from socket import *
import json

class p2pnet():

    serverip = '192.168.56.1'

    def __init__(self,name = "unnamed_connection"):

        self.name = name
        self.client_sock = socket(AF_INET, SOCK_STREAM)
        self.my_msg = f"{self.name}"
        self.connect_list = self.connect_to_subserver()
        print(self.connect_list)


    def connect_to_subserver(self):
        #self.client_sock.connect(('localhost',9090))
        #self.client_sock.send(self.my_msg.encode())
        try:
            self.client_sock.connect((self.serverip, 9090))
            self.client_sock.send(self.my_msg.encode())
            data = self.client_sock.recv(1024)
            data = data.decode('utf-8')
            print(data)
            print("connection to subserver complited")
        except Exception as e:
            print(e)
            return None
        # while True:
        #     for _ in range(10):
        #         self.client_sock.sendto(self.my_msg.encode(), (self.serverip, 9090))
        #         try:
        #             data = self.server_sock.recv(4096)#уточнить про размер!!!
        #             print(data.decode('utf-8'))
        #             #data = self.server_sock.recvfrom(4096)#возвращает пару (данные,(ip,port))
        #             print("connection to subserver complited")
        #             return json.loads(data.decode('utf-8'))
        #         except Exception as e:
        #             print(f"wait: error: {e}")
        #             continue

    #todo переписать на нор отправку
    def send(self, data):
        try:
            message = json.dumps(data)
            self.client_sock.send(message.encode())
            return True
        except Exception as e:
            print(f"Errors: {e}")
            return False

    def __del__(self):
        #for i in self.connect_list.keys():
        #    ip,port = self.connect_list[i]
        #    self.client_sock.sendto(f"destroy-{self.name}".encode(),(ip,int(port)))
        #self.client_sock.sendto(f"destroy-{self.name}".encode(), (self.serverip, 9090))
        self.client_sock.close()