import socket
from threading import Thread
import socketserver
import config


class ClientThread(Thread):

    def __init__(self,client_sock,backend_ip):
        Thread.__init__(self)
        self.client_sock = client_sock
        self.backend_ip = backend_ip


        def run(self):
            backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            backend_socket.connect((backend_ip,config.TCP_PORT))
            data = self.client_sock.recv(config.DATA_SIZE)
            while True:
                if not data:
                    self.backend_socket.close()
                    break
                self.backend_socket.send(data)
                data = self.client_sock.recv(config.DATA_SIZE)
