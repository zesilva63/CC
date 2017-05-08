TCP_IP = 'localhost'
TCP_PORT = 80
BUFFER_SIZE = 4086

def main():

    

    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpServer.bind((TCP_IP, TCP_PORT))
    threads = []

    while True:
        tcpServer.listen(20)
        print("Multithreaded Python server : Waiting for connections from TCP clients...")
        (client_socket, (ip,port)) = tcpServer.accept()
        #backend_socket = chooseBest()
        thread = ClientThread(client_socket,backend_socket)
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
