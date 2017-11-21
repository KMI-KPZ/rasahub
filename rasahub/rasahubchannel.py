from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import socket
import json

from rasa_core.channels.channel import UserMessage
from rasa_core.channels.channel import InputChannel, OutputChannel

class RasahubInputChannel(InputChannel):
    """
    Receives Messages via socket
    """
    def __init__(self, ip, port):
        self.socket = socket.socket()
        self.socket.connect((ip, port))

    def start_async_listening(self, message_queue):
        self._record_messages(message_queue.enqueue)

    def start_sync_listening(self, message_handler):
        self._record_messages(message_handler)

    def _record_messages(self, on_message):
        while True:
            try:
                text = json.loads(self.socket.recv(1024).decode('utf-8')) # gets message data: message and message_id
                on_message(UserMessage(text['message'], RasahubOutputChannel(self.socket), text['message_id']))
            except socket.timeout:
                continue

class RasahubOutputChannel(OutputChannel):
    """
    Sends messages via socket
    """
    def __init__(self, socket):
        self.socket = socket
    def send_text_message(self, recipient_id, message):
        self.socket.sendall(message.encode('utf-8'))
