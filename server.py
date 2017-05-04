import socket
import json

import config


def status(sequence):
    return {"type": 'probe_response',
            "n": sequence,
            "cpu": 10,
            "memory": 30,
            "conn": 30}


class BackendServer:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET,
                                    socket.SOCK_DGRAM)
        self.socket.bind(('localhost', config.port + 1))

        self.indicacao()
        self.listenProbes()


    def indicacao(self):
        register = {'type': 'register'}
        msg = json.dumps(register).encode("utf-8")
        self.socket.sendto(msg, (config.rproxy_ip, config.port))


    def listenProbes(self):
        while True:
            msg, address = self.socket.recvfrom(1024)
            request = json.loads(msg.decode())
            print(address, request)

            if request['type'] == 'probe_request':
                msg = json.dumps(status(request['seq'])).encode()
                self.socket.sendto(msg, address)


def main():
    BackendServer()


if __name__ == "__main__":
    main()
