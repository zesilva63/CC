import socket
import time
import json
from threading import Thread
import config


class MonitorConnection:
    def __init__(self):
        self.recent_seq = []
        self.conversation = {}

    def probe_request(self, msg):
        self.recent_seq.append(msg['seq'])
        if (len(self.recent_seq) > 1000):
            self.recent_seq = self.recent_seq[1:]

        self.conversation[msg['seq']] = ((time.time(), msg), (None, None))

    def probe_response(self, response):
        (req, _) = self.conversation[response['seq']]
        self.conversation[response['seq']] = (req, (time.time(), response))

    def available(self):
        last5 = self.recent_seq[-5:]

        if all(time is None for (_, (time, _)) in last5):
            return False
        if any(msg is not None and msg['critical'] for (_, (_, msg)) in last5):
            return False

        return True

    def __cmp__(self, y):
        pass


class ProxyServerMonitor:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET,
                                    socket.SOCK_DGRAM)
        self.socket.bind(('', config.udp_port))
        self.servers = {}

        t1 = Thread(target=self.listen)
        t1.start()

        self.shout()

    def listen(self):
        while True:
            msg, address = self.socket.recvfrom(1024)

            msg = json.loads(msg.decode())

            if msg['type'] == 'register':
                self.servers[address] = MonitorConnection()
                self.servers[address].probe_response(msg)

                print("Register", address)
            else:
                self.servers[address].probe_response(msg)

    def shout(self):
        def shout_msg(seq):
            return {'type': 'probe_request',
                    'seq': seq,
                    }

        sequence = 0
        while True:
            for server in self.servers:
                msg = shout_msg(sequence)
                server.probe_request(msg)
                self.socket.sendto(json.dumps(msg.encode()), server)

            time.sleep(5)
            sequence += 1


def main():
    ProxyServerMonitor()


if __name__ == "__main__":
    main()
