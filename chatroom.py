class Chatroom():

    def __init__(self, room_name):
        self.room_name = room_name
        self.subscribers = {}

    def get_name(self):
        return self.room_name

    def subscribe(self, client_name, client_ip, client_port):
        """
        add a subscribe to a chat room
        """
        if client_name in self.subscribers:
            """
            name already in use
            """
            pass
        else:
            self.subscribers[client_name] = (client_ip, client_port)

    def unsubscribe(self, client_name):
        """
        unsubscribe from chatroom
        """
        self.subscribers.pop(client_name)

    def get_publish_list(self, speaker):
        """
        return a list of subscribers ip and port numbers in a tuple each
        so a message can be sent to all the subscribers of the channel
        """
        return_list = []
        for i in self.subscribers:
            if i == speaker:
                pass
            else:
                return_list.append(self.subscribers[i])
        return return_list
