import socket
from threading import Thread
from SocketServer import ThreadingMixIn

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



TCP_IP = 'localhost'
TCP_PORT = 80
BUFFER_SIZE = 4086

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpServer.listen(20)
    print("Multithreaded Python server : Waiting for connections from TCP clients...")
    (client_socket, (ip,port)) = tcpServer.accept()
    #backend_socket = chooseBest()
    thread = ClientThread(client_socket,backend_socket)
    thread.start()
    threads.append(thread)


for t in threads:
    t.join()
