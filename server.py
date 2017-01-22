'''
Server class
'''
import socket
import os
from threadpool import ThreadPool
from chatroom import Chatroom


class server:
    """docstring for server."""
    def __init__(self, host, port):
        self.max_threads = 8
        self.host = host
        self.port = port
        self.chatrooms = {}      # room_name -> room
        self.chatroom_ids = {}   # id -> name
        self.client_ids = {}
        self.setup_socket()
        self.tp = ThreadPool(self.max_threads)
        self.accept_connections()

    def setup_socket(self):
        '''
        Sets up a tcp socket that listens on the host and port given
        '''
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, int(self.port)))
        self.s.listen(50)

    def accept_connections(self):
        while True:
            client, address = self.s.accept()
            print("in accept, client: " + str(client))
            print("in accept, address: " + str(address))
            self.client_thread(client, address)
            print("loops in accept connection")

    def client_thread(self, client, addr):
        kargs = {"client": client, "address": addr}
        self.tp.add_task(self.handle, **kargs)
        # t = threading.Thread(target=self.handle, kwargs=kargs).start()

    def handle(self, **kwargs):
            client = kwargs["client"]  # client ip
            address = kwargs["address"]
            data = client.recv(1024)
            data = data.decode("utf-8")
            print(data)
            if data[:5] == "HELO ":
                text = data[6:]
                self.handle_helo(client, text)
            elif data[:len("KILL_SERVICE")] == "KILL_SERVICE":
                self.handle_kill()
            elif data[:4] == "join":
                message = data.split("\n")
                # these need to be changed the remove the labels, now it takes just the label
                message[0] = message[0][14:] # chatroom name
                message[1] = message[1][10:]  # port
                message[2] = message[2][5:]  # ip
                message[3] = message[3][13:] # client name
                print("message recieved: ")
                for i in message:
                    i = i.strip()
                    print(i)
                self.handle_join_room(message[0], message[3], client, address)
            elif data[:len("DISCONNECT: ")] == "DISCONNECT: ":
                self.handle_disconnect()
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
        called when we receive an unhandled message
        """
        pass

    def handle_join_room(self, room_name, client_name,
                         client_ip=0, client_port=0):
        if room_name not in self.chatrooms:
            room = Chatroom(room_name)
            self.chatrooms[room_name] = room
            self.chatroom_ids[room.get_id()] = room_name
            room.subscribe(client_name, client_ip)
        else:
            # create and join room
            room = self.chatrooms[room_name]    
            room.subscribe(client_name, client_ip)
        room.subscribe(client_name, client_ip, client_port)
        l = room.get_publish_list()
        client_ip.send(self.success_response(room_name, self.host, self.port, room.get_id(), id(client_name)).encode())
        self.client_ids[id(client_name)] = client_name
        for i in l:
           # print("i in l loop: " + str(i) + "\n\n")
            i[1].sendall((str(client_name) + " has joined the room").encode())
            print("sent")
            # this could be wrong

    def success_response(self, room_name0, host, port, room_id, client_id):
        return "JOINED_CHATROOM: " + room_name0 + "\n" +\
        "SERVER_IP: " + str(host) + "\n" +\
        "PORT: " + str(port) + "\n" +\
        "ROOM_REF: " + str(room_id) + "\n" +\
        "JOIN_ID: " + str(client_id)

    def handle_leave_chatroom(self, host, port, room_id, client_name):
        room = self.chatrooms[self.chatroom_ids[room_id]]
        room.unsubscribe(client_name)
        host.send(self.leave_message(room_id, client_name))
        l = room.get_publish_list()
        for i in l:
            i[0].sendall(self.left_message(room_id, client_name).encode())


    def leave_message(self, room_id, client_name):
        cid = self.client_ids[client_name]
        return "LEAVE_CHATROOM: " + str(room_id) + "\n" +\
            "JOIN_ID: " + str(cid) + "\n" +\
            "CLIENT_NAME: " + client_name

    def left_message(self, room_id, client_name):
        cid = self.chatroom_ids[client_name]
        return "LEFT_CHATROOM: " + str(room_id) + "\n" +\
            "JOIN_ID: " + str(cid)

    def handle_disconnect(self):
        self.s.close()

    def handle_chat(self, room_id, client_name, msg):
        mmessage = "CHAT: " + str(room_id) + "\n" +\
            "CLIENT_NAME: " + client_name + "\n" +\
            "MESSAGE: " + msg
        room = self.chatrooms[self.chatroom_ids[room_id]]
        l = room.get_publish_list()
        for i in l:
            i[0].sendall(mmessage.encode())
