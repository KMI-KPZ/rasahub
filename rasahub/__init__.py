from __future__ import unicode_literals
from Queue import Queue
from rasahub.handler.dbconnector import DBConnector
from rasahub.plugins.rasa import RasaConnector
import argparse
import time
import threading

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


def rasa_in_thread(outputqueue, run_event):
    global rasaconn
    while run_event.is_set():
        # if new message from rasa: save to db
        reply = rasaconn.getReply()
        if reply is not None:
            print("Reply from Rasa: {}".format(reply))
            outputqueue.put(reply)
            print("Reply enqueued to Humhub")
        time.sleep(0.5)

def humhub_in_thread(outputqueue, run_event):
    global dbconn
    while run_event.is_set():
        new_id = dbconn.getNextID()
        if (dbconn.current_id != new_id): # new messages
            dbconn.current_id = new_id
            inputmsg = dbconn.getMessage(new_id)
            print("New message: " + inputmsg['message'])
            outputqueue.put(inputmsg) # put new message to rasa queue
            print("Reply enqueued to Rasa")
        time.sleep(0.5)

def rasa_output_handler(queue, run_event):
    global rasaconn
    while run_event.is_set():
        msg = queue.get()
        rasaconn.send(msg)
        print("Sent message to Rasa")
        queue.task_done()

def humhub_output_handler(queue, run_event):
    global dbconn
    while run_event.is_set():
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

    setup_connections(cmdline_args);

    rasamodule = RasaConnector(cmdline_args.rasahost, cmdline_args.rasaport)

    # global run event
    run_event = threading.Event()
    run_event.set()

    # create queues for each job
    rasaqueue = Queue()
    humhubqueue = Queue()

    rasamodule.start(run_event, rasaqueue, humhubqueue)

    # create and start threads for input channels
    t2 = threading.Thread(target = humhub_in_thread, args=(rasaqueue, run_event,))

    t2.start()

    print("Input threads started")

    # spawn output worker threads
    for i in range(num_fetch_threads):
        worker = threading.Thread(target=humhub_output_handler, args=(humhubqueue, run_event,))
        worker.setDaemon(True)
        worker.start()

    print("Rasa output threads started")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Closing worker threads..")
        run_event.clear()
        rasamodule.end()
        t2.join()
        humhub_output_queue.join()
        print("All threads closed properly.")
        pass
