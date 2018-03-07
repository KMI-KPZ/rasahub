from __future__ import unicode_literals
from rasahub.handler.dbconnector import DBConnector
from rasahub.handler.rasaconnector import RasaConnector

import argparse

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

    dbconn = DBConnector(cmdline_args.dbhost,
                         cmdline_args.dbname,
                         cmdline_args.dbport,
                         cmdline_args.dbuser,
                         cmdline_args.dbpassword,
                         cmdline_args.trigger)
    print("Connected to database. Waiting for socket connection from Rasa on port {}".format(cmdline_args.rasaport))

    rasaconn = RasaConnector(cmdline_args.rasahost,
                             cmdline_args.rasaport)

    while (True):
        if (dbconn.checkNewDBMessages()):
            inputmsg = dbconn.getNewDBMessage()
            print("Input from db: {}".format(inputmsg))
            reply = rasaconn.getReply(inputmsg)
            if reply is not None:
                print("Reply from rasa: {}".format(reply))
                dbconn.saveToDB(reply)
            else:
                print("No reply from Rasa.")
                continue
