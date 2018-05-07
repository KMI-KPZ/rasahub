from __future__ import unicode_literals

import json
import time
import sys
import yaml
import os
import importlib

from rasahub.messagehandler import RasahubHandler
from rasahub.plugin import RasahubPlugin

def main():
    """
    Initializes DBConnector and RasaConnector, handles messages
    """
    messagehandler = RasahubHandler()
    configpath = "config.yml"
    config = yaml.safe_load(open(configpath))
    for plugin in config:
        try:
            lib = __import__(config[plugin]['package'])
        except:
            print("Package " + config[plugin]['package'] + " not found.")
        else:
            method = config[plugin]['classname']
            globals()[plugin] = lib
            if config[plugin]['init'] is not None:
                plugin_instance = eval(plugin + '.' + method)(**config[plugin]['init'])
            else:
                plugin_instance = eval(plugin + '.' + method)()
            plugin_instance.add_target(config[plugin]['out'])
            messagehandler.add_plugin(plugin, plugin_instance)

    messagehandler.start()
    #import pdb; pdb.set_trace()

    print("Input threads started")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Closing worker threads..")
        messagehandler.end()
        return True
