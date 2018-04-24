from __future__ import unicode_literals
from Queue import Queue
from rasahub.handler.dbconnector import DBConnector
from rasahub.handler.rasaconnector import RasaConnector
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
    rasaconn = RasaConnector(cmdline_args.rasahost,
                                  cmdline_args.rasaport)
    print("Rasa connection established")

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

    setup_connections(cmdline_args)

    run_event = threading.Event()
    run_event.set()

    # create queues for each job
    rasa_output_queue = Queue()
    humhub_output_queue = Queue()

    print("Queues created")

    # create and start threads for input channels
    t1 = threading.Thread(target = rasa_in_thread, args=(humhub_output_queue, run_event,))
    t2 = threading.Thread(target = humhub_in_thread, args=(rasa_output_queue, run_event,))

    t1.start()
    t2.start()

    print("Input threads started")

    # spawn output worker threads
    for i in range(num_fetch_threads):
        worker = threading.Thread(target=humhub_output_handler, args=(humhub_output_queue, run_event,))
        worker.setDaemon(True)
        worker.start()

    print("Humhub output threads started")

    for i in range(num_fetch_threads):
        worker = threading.Thread(target=rasa_output_handler, args=(rasa_output_queue, run_event,))
        worker.setDaemon(True)
        worker.start()

    print("Rasa output threads started")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Closing worker threads..")
        run_event.clear()
        t1.join()
        t2.join()
        rasa_output_queue.join()
        humhub_output_queue.join()
        print("All threads closed properly.")
        pass
