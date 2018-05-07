from __future__ import unicode_literals

import threading
import sys
import time

is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue

class RasahubPlugin(object):
    """
    Main class for a plugin
    """

    plugins = set()

    def __init__(self):
        """
        Creates Message sending queue
        """
        self.outputqueue = queue.Queue()
        self.in_event = threading.Event()
        self.out_event = threading.Event()
        self.plugins.add(self)

    def start(self, main_queue):
        """
        Starts sending and receiving threads
        """
        self.receiving = threading.Thread(target = self.in_thread, args = (main_queue, self.in_event,))
        self.sending = threading.Thread(target = self.out_thread, args = (self.outputqueue, main_queue, self.out_event,))

        self.receiving.start()
        self.sending.start()
        return True

    def end(self):
        """
        Safely closes threads
        """
        self.outputqueue.join()
        print("queue joined..")
        self.in_event.set()
        print("in threads closed..")
        self.out_event.set()
        print("out threads closed..")
        return True

    def add_target(self, classname):
        self.target = classname

    def in_thread(self, main_queue, run_event):
        """
        Input message thread
        """
        while (not run_event.is_set()):
            in_message = self.receive()
            if in_message is not None:
                # add source and target to message
                message = {'source': self, 'target': self.target, 'message': in_message}
                main_queue.put(message)
            time.sleep(0.5)

    def out_thread(self, outputqueue, main_queue, run_event):
        """
        Output message thread
        """
        while (not run_event.is_set()):
            try:
                out_message = outputqueue.get(False)
                self.send(out_message['message'], main_queue)
                outputqueue.task_done()
            except queue.Empty:
                pass

    def send(self, messagedata, main_queue):
        """
        Sending function, to be implemented by plugin
        """
        raise NotImplementedError

    def receive(self):
        """
        Receiving function, to be implemented by plugin
        """
        raise NotImplementedError
