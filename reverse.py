import random, socket, sys, threading

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # receive request
        data = str(self.request.recv(2048), 'ascii')

        # choose best
        # connect to best
        # send data to best

        # returns current thread
        cur_thread = threading.current_thread()
        # mete a data em bytes
        response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
        # envia os mesmos dados
        self.request.sendall(response)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

"""
def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print("Received: {}".format(response))
    finally:
        sock.close()
"""

if __name__ == "__main__":
    HOST, PORT = "localhost", 80
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)

    client(ip, port, "Hello World 1")
    client(ip, port, "Hello World 2")
    client(ip, port, "Hello World 3")

    server.shutdown()
    server.server_close()
