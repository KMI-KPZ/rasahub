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
    Initializes plugins, handles messages
    """
    messagehandler = RasahubHandler()
    configpath = "config.yml"
    config = yaml.safe_load(open(configpath))

    for plugin in config:
        try:
            lib = __import__(config[plugin]['package'])
            method = config[plugin]['classname']
            globals()[plugin] = lib
        except:
            print("Package " + config[plugin]['package'] + " not found.")
        try:
            if config[plugin]['init'] is not None:
                plugin_instance = eval(plugin + '.' + method)(**config[plugin]['init'])
            else:
                plugin_instance = eval(plugin + '.' + method)()
            if plugin_instance is not None:
                plugin_instance.add_target(config[plugin]['out']) # depracted
                messagehandler.add_plugin(plugin, config[plugin]['type'], plugin_instance)
            else:
                print("plugin " + plugin + "could not be started")
        except:
            print("plugin " + plugin + " could not be started")

    messagehandler.start()

    print("Input threads started")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Closing worker threads..")
        messagehandler.end_processes()
        return True
