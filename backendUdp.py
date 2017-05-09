import random
import socket

import config

class BackendServer:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET,
                                    socket.SOCK_DGRAM)
        self.socket.bind(('', config.udp_port))

        #self.indicacao()
        self.listenProbes()


    def indicacao(self):
        msg = "".encode("utf-8")
        self.socket.sendto(msg, (config.rproxy_ip, config.udp_port))


    def listenProbes(self):
        while True:
            msg, address = self.socket.recvfrom(1024)
            print(address)
            msg = msg.decode()[::-1].encode()
            self.socket.sendto(msg, address)


def main():
    BackendServer()


if __name__ == "__main__":
    main()
