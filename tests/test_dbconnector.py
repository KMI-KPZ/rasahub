from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest
import testing.mysqld

import pdb

from rasahub.handler.dbconnector import DBConnector
import mysql.connector
from mysql.connector import errorcode

def handler(mysqld):
    conn = mysql.connector.connect(**mysqld.dsn())
    cursor = conn.cursor(buffered=True)

    cursor.execute("CREATE TABLE `message_entry` ("
        "`id` int(11) NOT NULL AUTO_INCREMENT,"
        "`message_id` int(11) NOT NULL,"
        "`user_id` int(11) NOT NULL,"
        "`file_id` int(11) DEFAULT NULL,"
        "`content` text NOT NULL,"
        "`created_at` datetime DEFAULT NULL,"
        "`created_by` int(11) DEFAULT NULL,"
        "`updated_at` datetime DEFAULT NULL,"
        "`updated_by` int(11) DEFAULT NULL,"
        "PRIMARY KEY (`id`),"
        "KEY `index_user_id` (`user_id`),"
        "KEY `index_message_id` (`message_id`)"
        ") DEFAULT CHARSET=utf8")

    cursor.execute("CREATE TABLE `user_message` ("
        "`message_id` int(11) NOT NULL,"
        "`user_id` int(11) NOT NULL,"
        "`is_originator` tinyint(4) DEFAULT NULL,"
        "`last_viewed` datetime DEFAULT NULL,"
        "`created_at` datetime DEFAULT NULL,"
        "`created_by` int(11) DEFAULT NULL,"
        "`updated_at` datetime DEFAULT NULL,"
        "`updated_by` int(11) DEFAULT NULL,"
        "PRIMARY KEY (`message_id`,`user_id`),"
        "KEY `index_last_viewed` (`last_viewed`)"
        ") DEFAULT CHARSET=utf8;")

    cursor.executemany(
        """INSERT INTO `message_entry`
        (`message_id`, `user_id`, `content`, `created_at`, `created_by`, `updated_at`, `updated_by`)
        VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        [
            (1, 1, 'Foo', '2017-09-26 11:59:04', 1, '2017-09-26 11:59:04', 1),
            (1, 1, '!bot Bar', '2017-09-26 11:59:09', 1, '2017-09-26 11:59:09', 1),
            (1, 1, '!bot Foo', '2017-09-26 12:09:46', 1, '2017-09-26 12:09:46', 1),
            (1, 1, '!bot Foobar', '2017-09-26 12:11:10', 1, '2017-09-26 12:11:10', 1),
            (1, 1, 'Lorem','2017-09-27 11:32:15', 1, '2017-09-27 11:32:15', 1),
            (1, 1, '!bot Lipsum','2017-09-28 12:58:20', 1, '2017-09-28 12:58:20', 1),
            (1, 1, 'Lorem Lipsum','2017-10-01 10:23:26', 1, '2017-10-01 10:23:26', 1)
        ]
    )

    cursor.execute("INSERT INTO `user_message` "
        "(`message_id`, `user_id`, `is_originator`, `last_viewed`, `created_at`, `created_by`, `updated_at`, `updated_by`) VALUES "
        "(1,	1,	1,	'2017-10-01 10:23:26',	'2017-09-26 11:59:04',	1,	'2017-10-01 10:23:26',	1);")

    cursor.close()
    conn.commit()
    conn.close()

Mysqld = testing.mysqld.MysqldFactory(cache_initialized_db=True,
                                      on_initialized=handler)

mysqld = Mysqld(my_cnf={'skip-networking': None})
dbconn = DBConnector(mysqld.dsn()['host'],
                     mysqld.dsn()['db'],
                     mysqld.dsn()['port'],
                     mysqld.dsn()['user'],
                     '',
                     '!bot',
                     '5')

def tearDownModule():
    mysqld.stop()
    Mysqld.clear_cache()

class MyTestCase(unittest.TestCase):
    def test_connection(self):
        self.assertIsNotNone(dbconn)

    def test_checkNewMessages(self):
        self.assertFalse(dbconn.checkNewDBMessages(), False)

    def test_checkLatestMessageID(self):
        self.assertEqual(dbconn.getCurrentID(), 7)

    def test_checkNewDBMessage(self):
        conn = mysql.connector.connect(**mysqld.dsn())
        cursor = conn.cursor()
        cursor.execute("INSERT INTO `message_entry` "
            "(`message_id`, `user_id`, `content`, `created_at`, `created_by`, `updated_at`, `updated_by`) VALUES"
            "(1,	1,	'!bot Test',	'2017-10-02 11:51:03',	1,	'2017-10-02 11:51:03',	1);")
        cursor.close()
        conn.commit()
        conn.close()
        self.assertTrue(dbconn.checkNewDBMessages())

    def test_getNewDBMessage(self):
        self.assertEqual(dbconn.getNewDBMessage(), {'message': 'Test', 'message_id': 1})

    def test_saveToDB(self):
        dbconn.saveToDB({'reply': 'Bots Answer', 'message_id': 1})

        conn = mysql.connector.connect(**mysqld.dsn())
        cursor = conn.cursor()
        cursor.execute("SELECT id, content FROM `message_entry` ORDER BY ID DESC LIMIT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.commit()
        conn.close()

        self.assertEqual(result, (9, u'Bots Answer'))

if __name__ == '__main__':
    unittest.main()
