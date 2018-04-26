from __future__ import unicode_literals
from rasahub.plugins.rasa import RasaConnector
from rasahub.plugins.humhub import HumhubConnector
import argparse
import time
import threading

import sys
is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue

num_fetch_threads = 2

def create_argument_parser():
    parser = argparse.ArgumentParser(
            description='starts rasahub')
    parser.add_argument(
            '-dbu', '--dbuser',
            required=True,
            type=str,
            help="database username")
    parser.add_argument(
            '-dbp', '--dbpassword',
            required=True,
            type=str,
            help="database user password")
    parser.add_argument(
            '-dbh', '--dbhost',
            type=str,
            default='127.0.0.1',
            help="database hostname")
    parser.add_argument(
            '-dbprt', '--dbport',
            type=int,
            default='3306',
            help="database port")
    parser.add_argument(
            '-dbn', '--dbname',
            required=True,
            type=str,
            help="database name")
    parser.add_argument(
            '-t', '--trigger',
            type=str,
            default='!bot',
            help="bot trigger string")
    parser.add_argument(
            '-rh', '--rasahost',
            type=str,
            default='127.0.0.1',
            help="host address of rasa_core")
    parser.add_argument(
            '-rp', '--rasaport',
            type=int,
            default=5020,
            help="port of rasa_core rasahubchannel")
    return parser

def main():
    """
    Initializes DBConnector and RasaConnector, handles messages
    """
    arg_parser = create_argument_parser()
    cmdline_args = arg_parser.parse_args()

    rasamodule = RasaConnector(cmdline_args.rasahost, cmdline_args.rasaport)
    humhubmodule = HumhubConnector(cmdline_args.dbhost,
                              cmdline_args.dbname,
                              cmdline_args.dbport,
                              cmdline_args.dbuser,
                              cmdline_args.dbpassword,
                              cmdline_args.trigger)

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
