from __future__ import unicode_literals

import json
import socket
import time
import select

class RasaConnector():
    """
    Connects to Rasa, send and receive messages
    """

    def __init__(self, rasaIP, rasaPort):
        """
        Initializes the RasaConnector, establishes the server socket

        :param rasaIP: IP address of Rasa_Core instance
        :type name: str.
        :param rasaPort: Port number set in Rasa_Core RasahubInputChannel
        :type state: int.
        """
        socket = self.establishSocket(rasaIP, rasaPort)
        socket.listen(5)
        c, addr = socket.accept()
        self.con = c

    def establishSocket(self, ip, port):
        """
        Establishes the socket

        :param ip: IP address of Rasa_Core instance
        :type name: str.
        :param port: Port number set in Rasa_Core RasahubInputChannel
        :type state: int.
        :returns: socket -- the serversocket
        """
        newSocket = socket.socket()
        newSocket.bind((ip, port))
        return newSocket

    def send(self, messagedata):
        self.con.send(json.dumps(messagedata).encode())

    def getReply(self):
        """
        Sends message to Rasa_Core, returns reply

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
