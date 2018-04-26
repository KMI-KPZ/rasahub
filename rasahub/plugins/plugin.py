from __future__ import unicode_literals

import json
import time
import threading
import sys
is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue


class RasahubPlugin(object):

    def __init__(self):
        print("create queue")
        self.queue = queue.Queue()
        print("queue created")

    def start(self, run_event, outputqueue):
        # start receiving and sending tasks
        self.receiving = threading.Thread(target = self.in_thread, args = (outputqueue, run_event,))
        self.sending = threading.Thread(target = self.out_thread, args = (self.queue, run_event,))

        self.receiving.start()
        self.sending.start()
        return True

    def end(self):
        self.receiving.join()
        self.sending.join()
        return True

    def in_thread(self, outputqueue, run_event):
        while run_event.is_set():
            in_message = self.receive()
            if in_message is not None:
                print("Reply from Rasa: {}".format(in_message))
                outputqueue.put(in_message)
                print("Reply enqueued to Humhub")
            time.sleep(0.5)

    def out_thread(self, inputqueue, run_event):
        while run_event.is_set():
            out_message = inputqueue.get()
            self.send(out_message)
            print("Sent message to Rasa")
            inputqueue.task_done()

    def send(self, messagedata):
        raise NotImplementedError

    def receive(self):
        raise NotImplementedError
