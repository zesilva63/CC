import socket
import time
import json
from threading import Thread
import config


class Server:
    def __init__(self):
        pass

    def add_probe_response(server, response):
        pass


def server_score(probe_response):
    assert(probe_response['type'] == 'probe_response')
    if probe_response['critical']:
        return -1
    if probe_response['']:
        pass


class ProxyServerMonitor:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET,
                                    socket.SOCK_DGRAM)
        self.socket.bind(('', config.udp_port))
        self.servers = set()

        t1 = Thread(target=self.listen)
        t1.start()

        self.shout()

    def listen(self):
        while True:
            msg, address = self.socket.recvfrom(1024)

            msg = json.loads(msg.decode())

            if msg['type'] == 'register':
                self.servers.add(address)
                print("Register", address)

    def shout(self):
        def shout_msg(seq):
            return {'type': 'probe_request',
                    'seq': seq}

        sequence = 0
        while True:
            for server in self.servers:

                msg = json.dumps(shout_msg(sequence)).encode()
                self.socket.sendto(msg, server)

            time.sleep(10)
            sequence += 1


def main():
    ProxyServerMonitor()


if __name__ == "__main__":
    main()
