import proxyserver
import clientHandler
import config

def main():

    monitor = proxyserver.ProxyServerMonitor()
    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpServer.bind((config.TCP_IP, config.TCP_PORT))
    threads = []

    while True:
        tcpServer.listen(30)
        print("Multithreaded Python server : Waiting for connections from TCP clients...")
        (client_socket, (ip,port)) = tcpServer.accept()
        #backend_ip = monitor.chooseBest()
        thread = clientHandler.ClientThread(client_socket,backend_ip)
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
