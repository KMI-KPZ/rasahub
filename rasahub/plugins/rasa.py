from __future__ import unicode_literals

import socket
import time
import select

from rasahub.plugin import RasahubPlugin

class RasaConnector(RasahubPlugin):
    """
    RasaConnector is subclass of RasahubPlugin
    """

    def __init__(self, ip, port):
        """
        Initializes the RasaConnector, establishes the server socket

        :param rasaIP: IP address of Rasa_Core instance
        :type name: str.
        :param rasaPort: Port number set in Rasa_Core RasahubInputChannel
        :type state: int.
        """
        super(RasaConnector, self).__init__()

        rasasocket = socket.socket()
        rasasocket.bind((ip, port))
        rasasocket.listen(5)
        c, addr = rasasocket.accept()
        self.con = c

    def send(self, messagedata):
        """
        Sends message to Rasa via socket connection
        """
        self.con.send(json.dumps(messagedata).encode())

    def receive(self):
        """
        Receives message from socket connection to Rasa

        :param messagedata: Input message as string and conversation ID
        :type name: dictionary.
        :returns: dictionary - the reply from Rasa as string and conversation ID as string
        """
        timeout = time.time() + 5
        ready = select.select([self.con], [], [], 5)
        if ready[0]:
            reply = self.con.recv(1024).decode('utf-8')
            reply = json.loads(reply)
            replydata = {
                'reply': reply['message'],
                'message_id': reply['message_id']
            }
            return replydata
        else:
            return None
