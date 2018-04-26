from rasahub.plugin import RasahubPlugin

import mysql.connector
from mysql.connector import errorcode

class HumhubConnector(RasahubPlugin):
    """
    HumhubConnector is subclass of RasahubPlugin
    """
    def __init__(self, dbHost, dbName, dbPort, dbUser, dbPwd, trigger):
        """
        Initializes database connection

        :param dbHost: database host address
        :type state: str.
        :param dbName: database name
        :type state: str.
        :param dbPort: database host port
        :type state: int.
        :param dbUser: database username
        :type name: str.
        :param dbPwd: database userpassword
        :type state: str.
        """
        super(HumhubConnector, self).__init__()

        self.cnx = self.connectToDB(dbHost, dbName, dbPort, dbUser, dbPwd)
        self.cursor = self.cnx.cursor()
        self.current_id = self.getCurrentID()
        self.trigger = trigger
        self.bot_id = self.getBotID()

    def connectToDB(self, dbHost, dbName, dbPort, dbUser, dbPwd):
        """
        Establishes connection to the database

        :param dbHost: database host address
        :type state: str.
        :param dbName: database name
        :type state: str.
        :param dbPort: database host port
        :type state: int.
        :param dbUser: database username
        :type name: str.
        :param dbPwd: database userpassword
        :type state: str.
        :returns: MySQLConnection -- Instance of class MySQLConnection
        """
        try:
            cnx = mysql.connector.connect(user=dbUser, port=int(dbPort), password=dbPwd, host=dbHost, database=dbName, autocommit=True)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            return cnx

    def getCurrentID(self):
        """
        Gets the current max message ID from Humhub

        :returns: int -- Current max message ID
        """
        query = "SELECT MAX(id) FROM message_entry;"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def getBotID(self):
        """
        Gets a suitable Bot User ID from a Humhub User Group called 'Bots'

        :returns: int -- Bots Humhub User ID
        """
        query = "SELECT `user_id` FROM `group` JOIN `group_user` ON `group`.`id` = `group_user`.`group_id` WHERE `group`.`name` = 'Bots' ORDER BY user_id DESC LIMIT 1;"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def getNextID(self):
        """
        Gets the next message ID from Humhub

        :returns: int -- Next message ID to process
        """
        query = ("SELECT id FROM message_entry WHERE user_id <> %(bot_id)s AND (content LIKE %(trigger)s OR message_entry.message_id IN "
            "(SELECT DISTINCT message_entry.message_id FROM message_entry JOIN user_message "
            "ON message_entry.message_id=user_message.message_id WHERE user_message.user_id = 5 ORDER BY message_entry.message_id)) "
            "AND id > %(current_id)s ORDER BY id ASC")
        data = {
            'bot_id': self.bot_id,
            'trigger': self.trigger + '%', # wildcard for SQL
            'current_id': self.current_id,
        }
        self.cursor.execute(query, data)
        results = self.cursor.fetchall()
        if len(results) > 0: # fetchall returns list of results, each as a tuple
            return results[0][0]
        else:
            return self.current_id

    def getMessage(self, msg_id):
        """
        Gets the newest message

        :returns: dictionary -- Containing the message itself as string and the conversation ID
        """
        query = "SELECT message_id, content FROM message_entry WHERE (user_id <> 5 AND id = {})".format(msg_id)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        message_id = result[0]
        if result[1][:len(self.trigger)] == self.trigger:
            message = result[1][len(self.trigger):].strip()
        else:
            message = result[1].strip()
        messagedata = {
            'message': message,
            'message_id': message_id
        }
        return messagedata

    def send(self, messagedata):
        """
        Saves reply message from Rasa_Core to db

        :param messagedata: Containing the reply from Rasa as string and the conversation id
        :type state: dictionary.
        """
        query = ("INSERT INTO message_entry(message_id, user_id, content, created_at, created_by, updated_at, updated_by) "
            "VALUES (%(msg_id)s, %(bot_id)s, %(message)s, NOW(), %(bot_id)s, NOW(), %(bot_id)s)")
        data = {
          'msg_id': messagedata['message_id'],
          'bot_id': self.bot_id,
          'message': messagedata['reply'],
        }
        try:
            self.cursor.execute(query, data)
            self.cnx.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def receive(self):
        """
        Implements receive function

        :returns: dictionary - Received message with conversation ID
        """
        new_id = self.getNextID()
        if (self.current_id != new_id): # new messages
            self.current_id = new_id
            inputmsg = self.getMessage(new_id)
            return inputmsg
