from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest
import time

from rasahub.messagehandler import RasahubHandler
from rasahub.message import RasahubMessage
from rasahub.plugin import RasahubPlugin

from tests.test_plugin import RasaTestPlugin

class RasaTest(unittest.TestCase):
    def setUp(self):
        self.messagehandler = RasahubHandler()

        self.test1 = RasaTestPlugin()
        self.test2 = RasaTestPlugin()

        self.test1.add_target('test2')
        self.test2.add_target('test1')

        self.messagehandler.add_plugin('test1', 'interface', self.test1)
        self.messagehandler.add_plugin('test2', 'interface', self.test2)

        self.messagehandler.start()

    def test_message(self):
        message = RasahubMessage(message = "Test Message", message_id = 1, target = "test2", source = "test1")
        self.assertIsNotNone(message)

    def test_receive(self):
        self.test1.set_message('Test Message')
        time.sleep(3)
        self.assertEqual(self.test1.sent_message, 'Test Message')

    def test_transfer(self):
        self.test1.set_message('Test Message')
        # wait for transfer
        time.sleep(3)
        self.assertEqual(self.test2.message_out.message, 'Test Message')

    def tearDown(self):
        self.messagehandler.end_processes()

if __name__ == '__main__':
    unittest.main()
