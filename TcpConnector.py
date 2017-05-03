import threading

class TcpConnector(Thread):

    def __init__(self,end,sock):
        Thread.__init__(self)
        self.endereco = end
        self.client = sock
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.endereco, 80))







