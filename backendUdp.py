import socket
import os
import json
import config
from subprocess import check_output
import random

def response(msg):
    normalized_tcp = int(check_output("netstat | grep tcp | wc -l", shell=True)) /  \
                     int(check_output("ulimit -n", shell=True))
    return {'seq': msg['seq'],
            'load': os.getloadavg()[0],
            'tcp': normalized_tcp
            }


class BackendUDP:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET,
                                    socket.SOCK_DGRAM)
        self.socket.bind(('', random.randint(5000, 10000)))

        self.indicacao()
        self.listenProbes()

    def indicacao(self):
        msg = {'type': 'register'}
        self.socket.sendto(json.dumps(msg).encode("utf-8"),
                           (config.rproxy_ip, config.udp_port))

    def listenProbes(self):
        while True:
            msg, address = self.socket.recvfrom(1024)
            msg = json.loads(msg)
            if msg['type'] == 'probe_request':
                r = response(msg)
                self.socket.sendto(json.dumps(r).encode("utf-8"),
                                   address)


def main():
    # print(response({'seq': 0}))
    BackendUDP()


if __name__ == "__main__":
    main()
