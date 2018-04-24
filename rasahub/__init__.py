from __future__ import unicode_literals
from Queue import Queue
from threading import Thread
from rasahub.handler.dbconnector import DBConnector
from rasahub.handler.rasaconnector import RasaConnector
import argparse
import time

num_fetch_threads = 2

global dbconn
global rasaconn

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

def setup_connections(cmdline_args):
    global dbconn
    global rasaconn

    dbconn = DBConnector(cmdline_args.dbhost,
                              cmdline_args.dbname,
                              cmdline_args.dbport,
                              cmdline_args.dbuser,
                              cmdline_args.dbpassword,
                              cmdline_args.trigger)
    print("DB connection established")
    rasaconn = RasaConnector(cmdline_args.rasahost,
                                  cmdline_args.rasaport)
    print("Rasa connection established")

def rasa_in_thread(outputqueue):
    global rasaconn
    while True:
        # if new message from rasa: save to db
        reply = rasaconn.getReply()
        if reply is not None:
            print("Reply from Rasa: {}".format(reply))
            outputqueue.put(reply)
            print("Reply enqueued to Humhub")
        time.sleep(0.5)

def humhub_in_thread(outputqueue):
    global dbconn
    while True:
        new_id = dbconn.getNextID()
        if (dbconn.current_id != new_id): # new messages
            dbconn.current_id = new_id
            inputmsg = dbconn.getMessage(new_id)
            print("New message: " + inputmsg['message'])
            outputqueue.put(inputmsg) # put new message to rasa queue
            print("Reply enqueued to Rasa")
        time.sleep(0.5)

def rasa_output_handler(queue):
    global rasaconn
    while True:
        msg = queue.get()
        rasaconn.send(msg)
        print("Sent message to Rasa")
        queue.task_done()

def humhub_output_handler(queue):
    global dbconn
    while True:
        reply = queue.get()
        dbconn.saveToDB(reply)
        print("Saved reply to DB")
        queue.task_done()

def main():
    """
    Initializes DBConnector and RasaConnector, handles messages
    """
    arg_parser = create_argument_parser()
    cmdline_args = arg_parser.parse_args()

    setup_connections(cmdline_args)

    # create queues for each job
    rasa_output_queue = Queue()
    humhub_output_queue = Queue()

    print("Queues created")

    #rasa_input_thread = Thread(target=rasa_input_handler, args=(humhub_output_queue,))
    #rasa_input_thread.start()

    t1 = Thread(target = rasa_in_thread, args=(humhub_output_queue,))
    t2 = Thread(target = humhub_in_thread, args=(rasa_output_queue,))

    t1.start()
    t2.start()

    #humhub_input_thread = Thread(target=humhub_input_handler, args=(rasa_output_queue,))
    #humhub_input_thread.start()

    print("Input threads started")

    # spawn worker threads
    for i in range(num_fetch_threads):
        worker = Thread(target=humhub_output_handler, args=(humhub_output_queue,))
        worker.setDaemon(True)
        worker.start()

    print("Humhub output threads started")

    for i in range(num_fetch_threads):
        worker = Thread(target=rasa_output_handler, args=(rasa_output_queue,))
        worker.setDaemon(True)
        worker.start()

    print("Rasa output threads started")

    while True:
        pass
