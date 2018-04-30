from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import socket
import json
import sys

from rasa_core.channels.channel import UserMessage
from rasa_core.channels.channel import InputChannel, OutputChannel

def getFormat(message):
    is_py2 = sys.version[0] == '2'
    if is_py2:
        return message.encode('utf-8')
    else:
        return message

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
        reply = {
            "message": getFormat(message),
            "message_id": recipient_id
        }
        self.socket.sendall(json.dumps(reply).encode('utf-8'))
