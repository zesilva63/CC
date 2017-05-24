import proxymonitor
import clientHandler
import config

def main():

    monitor = proxymonitor.ProxyServerMonitor()
    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpServer.bind((config.TCP_IP, config.TCP_PORT))
    threads = []

    while True:
        tcpServer.listen(30)
        (client_socket, (ip,port)) = tcpServer.accept()
        backend_ip = min(monitor.servers.values())
        thread = clientHandler.ClientThread(client_socket,backend_ip)
        thread.start()
        threads.append(thread)


if __name__ == "__main__":
    main()
