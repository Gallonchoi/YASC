class MessageBuffer(object):
    def __init__(self):
        self.message = list()

    def get(self):
        return self.message

    def push(self, new_message):
        self.message.append(new_message)

message_buffer = MessageBuffer()
