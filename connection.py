from socket import *
import os, _thread as thread, time
from checker import checkerf

class Client:
    def __init__(self, ip = 'localhost', port = 50007):
        self.server_ip = ip
        self.port = port
        self.sockobj = socket(AF_INET, SOCK_STREAM)
        self.sockobj.connect((self.server_ip, self.port))

    def send_file(self, fpath, pid):
        f = open(fpath)
        self.sockobj.send(str(os.path.getsize(fpath)).encode())
        time.sleep(0.1)
        self.sockobj.send(str(pid).encode())
        time.sleep(0.1)
        while True:
            msg = f.read(1024)
            if not msg:
                break
            else:
                self.sockobj.send(msg.encode())
                time.sleep(0.1)

class Server:
    def __init__(self):
        self.ip = ''
        self.port = 50007
        self.sockobj = socket(AF_INET, SOCK_STREAM)
        self.sockobj.bind((self.ip, self.port))
        self.sockobj.listen(5)

    def loop(self):
        while True:
            connection, address = self.sockobj.accept()
            print('%s at %s'%(address, time.ctime()))
            #logfile = open('log/conn.log', 'w')
            #logfile.write('%s at %s'%(address, time.ctime()))
            self.conn = Connection(connection, address)

class Connection:
    def __init__(self, connection, address):
        self.address = address
        self.connection = connection
        thread.start_new_thread(self.receive_file, (5,))

    def receive_file(self, aiweyi):
        self.fsize = int(self.connection.recv(1024).decode())
        self.pid = int(self.connection.recv(1024).decode())
        self.l = []
        #print(self.fsize)
        while True:
            self.msg = self.connection.recv(1024)
            self.fsize -= len(self.msg)
            if not self.msg:
                break
            else:
                self.l.append(self.msg)
                #print(self.msg)
            if self.fsize == 0:
                break
        self.create_file()
        self.execute_file()
        self.connection.send(self.result.encode())
        os.remove(self.fname)

    def create_file(self):
        self.fname = 'tmp/%s.py'%(time.time())
        f = open(self.fname, 'w')
        for chunk in self.l:
            f.write(chunk.decode())

    def execute_file(self):
        self.result = checkerf(self.fname, self.pid)
