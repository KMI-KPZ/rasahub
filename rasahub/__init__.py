from __future__ import unicode_literals
from rasahub.plugins.rasa import RasaConnector
from rasahub.plugins.humhub import HumhubConnector
import time
import threading
import yaml

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
    configpath = "config.yml"
    config = yaml.safe_load(open(configpath))

    rasamodule = RasaConnector(config['rasa']['host'],
                               config['rasa']['port'])

    humhubmodule = HumhubConnector(config['humhub']['host'],
                                   config['humhub']['dbname'],
                                   config['humhub']['port'],
                                   config['humhub']['dbuser'],
                                   config['humhub']['dbpasswd'],
                                   config['humhub']['trigger'])

    # global run event
    run_event = threading.Event()
    run_event.set()

    rasamodule.start(run_event, humhubmodule.queue)
    humhubmodule.start(run_event, rasamodule.queue)

    print("Input threads started")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Closing worker threads..")
        run_event.clear()
        rasamodule.end()
        humhubmodule.end()
        print("All threads closed properly.")
        pass
