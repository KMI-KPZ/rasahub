from __future__ import unicode_literals
import json
import time
import threading
import sys
import yaml
import os
import imp
import importlib
is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue

num_fetch_threads = 2

class RasahubPlugin(object):
    """
    Main class for a plugin
    """

    plugins = set()

    def __init__(self):
        """
        Creates Message sending queue
        """
        self.queue = queue.Queue()
        self.in_event = threading.Event()
        self.out_event = threading.Event()
        self.plugins.add(self)

    def start(self, outputqueue):
        """
        Starts sending and receiving threads
        """
        self.receiving = threading.Thread(target = self.in_thread, args = (outputqueue, self.in_event,))
        self.sending = threading.Thread(target = self.out_thread, args = (self.queue, self.out_event,))

        self.receiving.start()
        self.sending.start()
        return True

    def end(self):
        """
        Safely closes threads
        """
        self.queue.join()
        print("queue joined..")
        self.in_event.set()
        print("in threads closed..")
        self.out_event.set()
        print("out threads closed..")
        return True

    def in_thread(self, outputqueue, run_event):
        """
        Input message thread
        """
        while (not run_event.is_set()):
            in_message = self.receive()
            if in_message is not None:
                print("Reply from Rasa: {}".format(in_message))
                outputqueue.put(in_message)
                print("Reply enqueued to Humhub")
            time.sleep(0.5)

    def out_thread(self, inputqueue, run_event):
        """
        Output message thread
        """
        while (not run_event.is_set()):
            try:
                out_message = inputqueue.get(False)
                self.send(out_message)
                inputqueue.task_done()
                print("Sent message to Rasa")
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

def main():
    """
    Initializes DBConnector and RasaConnector, handles messages
    """
    # loader:
    # from rasahub.humhub import HumhubConnector
    # ...

    # load plugins from plugins directory
    configpath = "config.yml"
    config = yaml.safe_load(open(configpath))
    plugins = {}
    for plugin in config:
        try:
            lib = __import__('rasahub_' + plugin)
        except:
            print("Plugin rasahub_" + plugin + "not found.")
        else:
            method = config[plugin]['classname']
            globals()[plugin] = lib
            plugins[plugin] = eval(plugin + '.' + method)(**config[plugin]['init'])
    for plugin in plugins:
        plugins[plugin].start(plugins[config[plugin]['out']].queue)

    print("Input threads started")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Closing worker threads..")
        for plugin in plugins:
            plugins[plugin].end()
        return True
