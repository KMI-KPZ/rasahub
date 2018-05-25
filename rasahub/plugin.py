from __future__ import unicode_literals

from rasahub.message import RasahubMessage

import threading
import sys
import time
import json

is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue

class RasahubPlugin(object):
    """
    Main class for a plugin
    """

    def __init__(self):
        """
        Creates Message sending queue
        """
        self.outputqueue = queue.Queue()
        self.in_event = threading.Event()
        self.out_event = threading.Event()
        self.target = ''
        self.name = ''

    def start(self, main_queue):
        """
        Starts sending and receiving threads
        """
        self.main_queue = main_queue
        self.receiving = threading.Thread(target = self.in_thread, args = (self.main_queue, self.in_event,))
        self.sending = threading.Thread(target = self.out_thread, args = (self.outputqueue, self.main_queue, self.out_event,))

        self.receiving.start()
        self.sending.start()
        return True

    def end_process(self):
        """
        Safely closes threads
        """
        self.outputqueue.join()
        print(self.name + " queue joined..")
        self.in_event.set()
        print(self.name + " in threads closed..")
        self.out_event.set()
        print(self.name + " out threads closed..")
        self.end()
        return True

    def add_target(self, classname):
        self.target = classname

    def set_name(self, pluginname):
        self.name = pluginname

    def in_thread(self, main_queue, run_event):
        """
        Input message thread
        """
        while (not run_event.is_set()):
            in_message = self.receive()
            if in_message is not None:
                # add source and target to message
                message = RasahubMessage(message = in_message['message'], message_id = in_message['message_id'], source = self.name, target = self.target)
                main_queue.put(message)
            #time.sleep(0.5)

    def out_thread(self, outputqueue, main_queue, run_event):
        """
        Output message thread
        """
        while (not run_event.is_set()):
            try:
                out_message = outputqueue.get(False)
                if len(out_message.message) > 0 and out_message.message[0] == '$':
                    # find escape characters in message string
                    first_index = out_message.message.find('$')
                    second_index = out_message.message[first_index+1:].find('$')

                    command = out_message.message[first_index+1:second_index+1]
                    payload = {}
                    if len(out_message.message[second_index+2:]) > 0:
                        payload['args'] = json.loads(out_message.message[second_index+2:])
                    payload['message_id'] = out_message.message_id
                    payload['message_source'] = out_message.source
                    payload['message_target'] = out_message.target
                    out_message = self.process_command(command, payload, out_message)
                # check target after processing
                if out_message is not None:
                    if out_message.target == self.name:
                        self.send(out_message, main_queue)
                        # free space
                        del out_message
                    else:
                        main_queue.put(out_message)
                outputqueue.task_done()
            except queue.Empty:
                pass

    def send(self, messagedata):
        """
        Sending function, to be implemented by plugin
        """
        raise NotImplementedError

    def receive(self):
        """
        Receiving function, to be implemented by plugin
        """
        raise NotImplementedError

    def process_command(self, message, out_message):
        """
        Output message hook, to be implemented by plugin
        """
        raise NotImplementedError

    def end(self):
        """
        Function to close connections etc., to be implemented by plugin
        """
        raise NotImplementedError
