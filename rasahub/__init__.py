from __future__ import unicode_literals
import time
import threading
import yaml
import os
import imp

import sys
is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue

num_fetch_threads = 2

def main():
    """
    Initializes DBConnector and RasaConnector, handles messages
    """
    # load plugins from plugins directory
    plugins = os.listdir("plugins/")
    rasa = imp.load_source("RasaConnector","./plugins/rasa.py")
    humhub = imp.load_source("HumhubConnector","./plugins/humhub.py")
    #for plugin in plugins:

    # load config
    configpath = "config.yml"
    config = yaml.safe_load(open(configpath))

    rasamodule = rasa.RasaConnector(config['rasa']['host'],
                               config['rasa']['port'])

    humhubmodule = humhub.HumhubConnector(config['humhub']['host'],
                                   config['humhub']['dbname'],
                                   config['humhub']['port'],
                                   config['humhub']['dbuser'],
                                   config['humhub']['dbpasswd'],
                                   config['humhub']['trigger'])

    rasamodule.start(humhubmodule.queue)
    humhubmodule.start(rasamodule.queue)

    print("Input threads started")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Closing worker threads..")
        humhubmodule.end()
        rasamodule.end()
        return True
