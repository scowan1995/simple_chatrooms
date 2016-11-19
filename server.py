'''
Server class
'''
import socket
import os
from threadpool import ThreadPool
import threading
from threadpool import AlreadyRunningError


class server:
    """docstring for server."""
    def __init__(self, host, port):
        self.max_threads = 8
        self.host = host
        self.port = port
        self.setup_socket()
        self.tp = ThreadPool(self.max_threads)
        self.accept_connections()

    def setup_socket(self):
        '''
        Sets up a tcp socket that listens on the host and port given
        '''
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, int(self.port)))
        self.s.listen(5)

    def accept_connections(self):
        while True:
            client, address = self.s.accept()
            self.client_thread(client)
            print("loops in accept connection")

    def client_thread(self, client):
        kargs = {"client": client}
        self.tp.add_task(self.handle, **kargs)
        #t = threading.Thread(target=self.handle, kwargs=kargs).start()

    def handle(self, **kwargs):
            client = kwargs["client"]
            data = client.recv(1024)
            data = data.decode("utf-8")
            print(data)
            if data[:5] == "HELO ":
                text = data[6:]
                self.handle_helo(client, text)
            elif data[:len("KILL_SERVICE")] == "KILL_SERVICE":
                self.handle_kill()
            else:
                self.handle_other()

    def handle_helo(self, client, text):
        """
        send back required information
        """
        ip = socket.gethostbyname(socket.gethostname())
        reply = "HELO " + text + "IP:" + ip + "\nPort:" + str(self.port) +\
            "\nStudentID:13325878\n"
        client.send(reply.encode('utf-8'))

    def handle_kill(self):
        """
        shuts down service
        """
        os._exit(0)

    def handle_other(self):
        """
        called when we recieve an unhandled message
        """
        pass
