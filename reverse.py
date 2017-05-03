import random
import socket
import sys
import threading

class ReverseServerTCP:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', 80))
        self.listen(10)
        self.listenRequest()


    def listenRequest(self):
        while True:
            client_connection, client_address = self.socket.accept()

# escolher para onde enviar
# devolve endereco do backend server a quem ligar
# backend_address = best()
            

            cliente = TcpConnector(backend_address,client_connection)
            cliente.start()
            cliente.join()




def main():
    ReverseServerTCP()


if __name__ == "__main__":
    main()
