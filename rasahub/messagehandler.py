from __future__ import unicode_literals

from rasahub.message import RasahubMessage

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
        self.plugins['interface'] = {}
        self.plugins['interpreter'] = {}
        self.plugins['datastore'] = {}
        self.plugins['all'] = {}

    def add_plugin(self, pluginname, plugintype, plugin):
        plugin.set_name(pluginname)
        if ((plugintype == 'interface') or
           (plugintype == 'interpreter') or
           (plugintype == 'datastore')):
            self.plugins[plugintype][pluginname] = plugin
        self.plugins['all'][pluginname] = plugin
        print("added " + pluginname)

    def start(self):
        self.mainthread = threading.Thread(target = self.main_thread, args = (self.mainqueue, self.thread_event,))
        self.mainthread.start()

        # start interface and interpreter plugins
        for plugin in self.plugins['interface']:
            self.plugins['interface'][plugin].start(self.mainqueue)
        for plugin in self.plugins['interpreter']:
            self.plugins['interpreter'][plugin].start(self.mainqueue)
        print("plugins started")
        return True

    def end_processes(self):
        self.mainqueue.join()
        for plugin in self.plugins['all']:
            self.plugins['all'][plugin].end_process()
        self.thread_event.set()
        return True

    def main_thread(self, main_queue, main_event):
        while (not main_event.is_set()):
            try:
                # get item from main queue
                message = main_queue.get(False)
                # determine target
                if message.target == 'interface':
                    for plugin in self.plugins['interface']:
                        if message.source != plugin:
                            self.plugins['interface'][plugin].outputqueue.put(message)
                elif message.target == 'interpreter':
                    for plugin in self.plugins['interpreter']:
                        if message.source != plugin:
                            self.plugins['interpreter'][plugin].outputqueue.put(message)
                else:
                    for plugin in self.plugins['all']:
                        if message.source != plugin:
                            self.plugins['all'][plugin].outputqueue.put(message)

                main_queue.task_done()
            except queue.Empty:
                pass
