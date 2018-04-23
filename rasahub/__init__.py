from __future__ import unicode_literals
from Queue import Queue
from threading import Thread
from rasahub.handler.dbconnector import DBConnector
from rasahub.handler.rasaconnector import RasaConnector
import argparse

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

def process_new_message(q, dbconn, rasaconn):
    while True:
        new_id = q.get()
        inputmsg = dbconn.getMessage(new_id)
        print("Input from db: {}".format(inputmsg))
        reply = rasaconn.getReply(inputmsg)
        if reply is not None:
            print("Reply from rasa: {}".format(reply))
            dbconn.saveToDB(reply)
        else:
            print("No reply from Rasa.")
        q.task_done()

def main():
    """
    Initializes DBConnector and RasaConnector, handles messages
    """
    arg_parser = create_argument_parser()
    cmdline_args = arg_parser.parse_args()

    dbconn = DBConnector(cmdline_args.dbhost,
                         cmdline_args.dbname,
                         cmdline_args.dbport,
                         cmdline_args.dbuser,
                         cmdline_args.dbpassword,
                         cmdline_args.trigger)
    print("Connected to database. Waiting for socket connection from Rasa on port {}".format(cmdline_args.rasaport))

    rasaconn = RasaConnector(cmdline_args.rasahost,
                             cmdline_args.rasaport)

    q = Queue()
    # spawn threads
    for i in range(num_fetch_threads):
        worker = Thread(target=process_new_message, args=(q, dbconn, rasaconn,))
        worker.setDaemon(True)
        worker.start()

    while (True):
        new_id = dbconn.getNextID()
        if (dbconn.current_id != new_id): # new messages
            dbconn.current_id = new_id
            q.put(new_id) # put new message to query

    q.join()
