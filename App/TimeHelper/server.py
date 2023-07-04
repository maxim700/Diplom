from socket import *
import json

class subserver:
    def __init__(self):
        self.connect_list = {}
        self.sock = socket(AF_INET, SOCK_STREAM)
        #self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(('192.168.56.1', 9090))

        self.sock.listen(1)
        #self.sock.listen(20)
        #print(gethostbyname(gethostname()))

    def listener(self):
        try:
            conn, addr = self.sock.accept()
            #conn.settimeout(2)
            #получаем сообщение о новом подключении
            #data = conn.recv(1024)z
            data = conn.recv(1024)
            data = json.loads(data.decode('utf-8'))
            match data["comand"]:
                case "down":
                    self.download()
                case "up":
                    self.upload()

            print("Новое соединение: ", data)
            return True
        except Exception as e:
            print(f"no new connections error: {e}")
            return False

    def upload(self,conn, fn):
        ##Костыль todo нужно синхронить а как?
        data = conn.recv(1024)
        data = json.loads(data.decode('utf-8'))
        with open(fn, "w") as file:
            json.dump(data, file)
            print("msg saved")
        file.close()

    def download(self, conn, fn):
        with open(fn, "r") as file:
            data = json.load(file).encode()
            conn.send(data)
            print("msg sended")
        file.close()


    def __del__(self):
        self.sock.close()




def main():
    serv = subserver()
    while True:
        serv.listener()



if __name__=='__main__':
    main()