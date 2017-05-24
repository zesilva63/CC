import socket
import time
import json
from threading import Thread
from functools import total_ordering

import config


@total_ordering
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

        return self.available()

    def lastN(self, N):
        return [self.conversation[seq] for seq in self.recent_seq[-N:]]

    def available(self):
        if all(time is None for (_, (time, _)) in self.lastN(10)):
            return False

        return True

    def misses(self, N=None):
        conv = self.conversation.values() if N is None else self.lastN(N)

        return sum(1 for ((_, req), (_, resp)) in conv if resp is not None)

    def rtt(self, seq):
        ((t1, _), (t2, _)) = self.conversation[seq]
        return t2 - t1

    def avg_rtt(self, N=None):
        seqs = self.conversation.keys() if N is None else self.recent_seq

        return sum(self.rtt(seq) for seq in seqs) / len(seqs)

    def avg_load(self, N=None):
        conv = self.conversation.values() if N is None else self.lastN(N)

        loads = [resp['load'] for ((_, req), (_, resp)) in conv
                 if resp is not None]
        return sum(loads) / len(loads)

    def avg_tcp_load(self, N=None):
        conv = self.conversation.values() if N is None else self.lastN(N)

        loads = [resp['tcp'] for ((_, req), (_, resp)) in conv
                 if resp is not None]
        return sum(loads) / len(loads)

    def __lt__(self, other):
        N = 10
        if self.avg_tcp_load(N) > 0.8 or other.avg_tcp_load(N) > 0.8:
            return self.avg_tcp_load(N) - other.avg_tcp_load(N)
        if self.avg_load(N) > 1 or other.avg_load(N) > 1:
            return self.avg_load(N) - other.avg_load(N)
        if abs(self.misses(N) - other.misses(N)) >= 2 or \
           abs(self.misses(N) - other.misses(N)) >= 2:
            return self.misses(N) < other.misses(N)
        return self.avg_rtt(N) < other.avg_rtt(N)

    def __eq__(self, other):
        N = 10
        return self.misses(N) == other.misses(N) and \
            self.avg_rtt(N) == other.avg_rtt(N) and \
            self.avg_load(N) == other.avg_load(N) and \
            self.avg_tcp_load(N) == other.avg_tcp_load(N)


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
            print("Recebeu:", msg)

            if 'type' in msg and msg['type'] == 'register':
                self.servers[address] = MonitorConnection()
                # self.servers[address].probe_response(msg)

                print("Register", address)
            else:
                if not(self.servers[address].probe_response(msg)):
                    del(self.servers[address])

    def shout(self):
        def shout_msg(seq):
            return {'type': 'probe_request',
                    'seq': seq,
                    }

        sequence = 0
        while True:
            for server in self.servers:
                msg = shout_msg(sequence)
                self.servers[server].probe_request(msg)
                self.socket.sendto(json.dumps(msg).encode(), server)

            time.sleep(5)
            sequence += 1


def main():
    ProxyServerMonitor()


if __name__ == "__main__":
    main()
