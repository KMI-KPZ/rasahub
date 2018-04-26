from __future__ import unicode_literals

import json
import socket
import time
import select
from Queue import Queue
import threading

class RasaConnector:
    """
    Rasa Connection handler using sockets
    """

    def __init__(self, ip, port):
        """
        Initializes the RasaConnector, establishes the server socket

        :param rasaIP: IP address of Rasa_Core instance
        :type name: str.
        :param rasaPort: Port number set in Rasa_Core RasahubInputChannel
        :type state: int.
        """
        self.messagequeue = Queue()
        rasasocket = socket.socket()
        rasasocket.bind((ip, port))
        rasasocket.listen(5)
        c, addr = rasasocket.accept()
        self.con = c

    def start(self, run_event, inputqueue, outputqueue):
        # start receiving and sending tasks
        self.receiving = threading.Thread(target = self.rasa_in_thread, args = (outputqueue, run_event,))
        self.sending = threading.Thread(target = self.rasa_output_handler, args = (inputqueue, run_event,))

        self.receiving.start()
        self.sending.start()
        return True

    def end(self):
        self.receiving.join()
        self.sending.join()
        return True

    def rasa_in_thread(self, outputqueue, run_event):
        while run_event.is_set():
            # if new message from rasa: save to db
            reply = self.getReply()
            if reply is not None:
                print("Reply from Rasa: {}".format(reply))
                outputqueue.put(reply)
                print("Reply enqueued to Humhub")
            time.sleep(0.5)

    def rasa_output_handler(self, queue, run_event):
        while run_event.is_set():
            msg = queue.get()
            self.send(msg)
            print("Sent message to Rasa")
            queue.task_done()

    def send(self, messagedata):
        self.con.send(json.dumps(messagedata).encode())

    def receive(self, queue, run_event):
        while run_event.is_set():
            # if new message from rasa: save to db
            reply = rasaconn.getReply()
            if reply is not None:
                print("Reply from Rasa: {}".format(reply))
                queue.put(reply)
                print("Reply enqueued to Humhub")
            time.sleep(0.5)

    def getReply(self):
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
