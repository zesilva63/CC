import socket
import json
import config


def response(msg):
    return {''}


class BackendUDP:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET,
                                    socket.SOCK_DGRAM)
        self.socket.bind(('', config.udp_port))

        self.indicacao()
        self.listenProbes()

    def indicacao(self):
        msg = {'type': 'register'}
        self.socket.sendto(json.dumps(msg.encode("utf-8")),
                           (config.rproxy_ip, config.udp_port))

    def listenProbes(self):
        while True:
            msg, address = self.socket.recvfrom(1024)
            if msg['type'] == 'probe_request':
                r = response(msg)
                self.socket.sendto(json.dumps(r.encode("utf-8")),
                                   address)


def main():
    BackendUDP()


if __name__ == "__main__":
    main()
