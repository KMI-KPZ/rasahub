from __future__ import unicode_literals

from rasahub import RasahubPlugin

class RasaTestPlugin(RasahubPlugin):
    """
    RasaTest is a testing plugin.

    """

    def __init__(self, **kwargs):
        """

        """
        super(RasaTestPlugin, self).__init__()

        self.message_in = []
        self.sent_message = ""
        self.message_out = ""

    def send(self, messagedata, main_queue):
        """
        Sends message to Rasa via socket connection
        messagedata is RasahubMessage object
        """
        self.message_out = messagedata

    def receive(self):
        """
        Receives message from socket connection to Rasa

        :returns: dictionary - the reply from Rasa as string and conversation ID as string
        """
        if len(self.message_in) > 0:
            self.sent_message = self.message_in.pop()
            message = {
                'message': self.sent_message,
                'message_id': 1
            }
            return message
        else:
            return None

    def set_message(self, message_string):
        self.message_in.append(message_string)

    def end(self):
        """
        """
        return "ended"
