from __future__ import unicode_literals

import threading
import sys
import json
is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue

class RasahubHandler():
    """
    Handles messages, keeps main queue, gets tasks from queue and sends to plugin workers
    """

    def __init__(self):
        self.mainqueue = queue.Queue()
        self.thread_event = threading.Event()
        self.plugins = {}

    def add_plugin(self, pluginname, plugin):
        plugin.set_name(pluginname)
        self.plugins[pluginname] = plugin
        print("added " + pluginname)

    def start(self):
        self.mainthread = threading.Thread(target = self.main_thread, args = (self.mainqueue, self.thread_event,))
        self.mainthread.start()

        for plugin in self.plugins:
            self.plugins[plugin].start(self.mainqueue)
        print("plugins started")
        return True

    def end(self):
        self.mainqueue.join()
        for plugin in self.plugins:
            self.plugins[plugin].end()
        self.thread_event.set()
        return True

    def main_thread(self, main_queue, main_event):
        while (not main_event.is_set()):
            try:
                # get item from main queue
                message = main_queue.get(False)
                # determine target
                self.plugins[message['target']].outputqueue.put(message)
                main_queue.task_done()
            except queue.Empty:
                pass
