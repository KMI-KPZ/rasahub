.. Test your Plugin doc

Test your Plugin!
=================

Testing your created plugin is very simple. Just test against message sending
and receiving using a RasahubTest-Plugin. Source of the test_plugin.py:

.. code-block:: python

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

With Unittest you should create the messagehandler in setUpClass method and also
initialize the testing plugin. Then you can put a message in the test_plugin
queue and check if the message will be received by your plugin. Also you should
send a message using your plugin and see if the testing plugin receives it
using plugin.sent_message.

As an example you should check out the testing of `rasahub-humhub`_ .


.. _rasahub-humhub: https://github.com/frommie/rasahub-humhub/blob/master/tests/test_dbconnector.py
.. _virtualenv: https://virtualenv.pypa.io/en/stable/
