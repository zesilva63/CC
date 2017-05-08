import socket
from threading import Thread
import socketserver

class ClientThread(Thread):

    def __init__(self,client_sock,backend_sock):
        Thread.__init__(self)
        self.client_sock = client_sock
        self.backend_sock = backend_sock


        def run(self):
            data = self.client_sock.recv(BUFFER_SIZE)
            while True:
                if not data:
                    self.backend_sock.close()
                    break
                self.backend_sock.send(data)
                data = self.client_sock.recv(BUFFER_SIZE)
