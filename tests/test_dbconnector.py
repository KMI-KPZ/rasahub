from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest
import testing.mysqld

import pdb

from rasahub_humhub import HumhubConnector
import mysql.connector
from mysql.connector import errorcode

def handler(mysqld):
    conn = mysql.connector.connect(**mysqld.dsn())
    cursor = conn.cursor(buffered=True)

    cursor.execute("""
        CREATE TABLE `message_entry` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `message_id` int(11) NOT NULL,
        `user_id` int(11) NOT NULL,
        `file_id` int(11) DEFAULT NULL,
        `content` text NOT NULL,
        `created_at` datetime DEFAULT NULL,
        `created_by` int(11) DEFAULT NULL,
        `updated_at` datetime DEFAULT NULL,
        `updated_by` int(11) DEFAULT NULL,
        PRIMARY KEY (`id`),
        KEY `index_user_id` (`user_id`),
        KEY `index_message_id` (`message_id`)
        ) DEFAULT CHARSET=utf8""")

    cursor.execute("""
        CREATE TABLE `user_message` (
        `message_id` int(11) NOT NULL,
        `user_id` int(11) NOT NULL,
        `is_originator` tinyint(4) DEFAULT NULL,
        `last_viewed` datetime DEFAULT NULL,
        `created_at` datetime DEFAULT NULL,
        `created_by` int(11) DEFAULT NULL,
        `updated_at` datetime DEFAULT NULL,
        `updated_by` int(11) DEFAULT NULL,
        PRIMARY KEY (`message_id`,`user_id`),
        KEY `index_last_viewed` (`last_viewed`)
        ) DEFAULT CHARSET=utf8;""")

    cursor.execute("""
        CREATE TABLE `group` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `space_id` int(10) DEFAULT NULL,
        `name` varchar(45) DEFAULT NULL,
        `description` text,
        `created_at` datetime DEFAULT NULL,
        `created_by` int(11) DEFAULT NULL,
        `updated_at` datetime DEFAULT NULL,
        `updated_by` int(11) DEFAULT NULL,
        `ldap_dn` varchar(255) DEFAULT NULL,
        `is_admin_group` tinyint(1) NOT NULL DEFAULT '0',
        `show_at_registration` tinyint(1) NOT NULL DEFAULT '1',
        `show_at_directory` tinyint(1) NOT NULL DEFAULT '1',
        PRIMARY KEY (`id`)
        ) DEFAULT CHARSET=utf8;""")

    cursor.execute("""
        CREATE TABLE `group_user` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `user_id` int(11) NOT NULL,
        `group_id` int(11) NOT NULL,
        `is_group_manager` tinyint(1) NOT NULL DEFAULT '0',
        `created_at` datetime DEFAULT NULL,
        `created_by` int(11) DEFAULT NULL,
        `updated_at` datetime DEFAULT NULL,
        `updated_by` int(11) DEFAULT NULL,
        PRIMARY KEY (`id`)
        ) DEFAULT CHARSET=utf8;""")

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

    cursor.execute("""
        INSERT INTO `user_message`
        (`message_id`, `user_id`, `is_originator`, `last_viewed`, `created_at`, `created_by`, `updated_at`, `updated_by`) VALUES
        (1,	1,	1,	'2017-10-01 10:23:26',	'2017-09-26 11:59:04',	1,	'2017-10-01 10:23:26',	1);""")

    cursor.execute("""
        INSERT INTO `group` (`id`, `space_id`, `name`, `description`, `created_at`, `created_by`, `updated_at`, `updated_by`, `ldap_dn`, `is_admin_group`, `show_at_registration`, `show_at_directory`) VALUES
        (1,	NULL,	'Administrator',	'Administrator Group',	'2017-05-28 14:09:29',	NULL,	NULL,	NULL,	NULL,	1,	0,	0),
        (2,	NULL,	'Users',	'Example Group by Installer',	'2017-05-28 14:09:32',	NULL,	'2017-05-28 14:09:32',	NULL,	NULL,	0,	1,	1),
        (3,	NULL,	'Bots',	'User Group for Bots',	'2017-11-30 13:48:26',	1,	'2017-11-30 13:48:26',	1,	NULL,	0,	0,	1);""")

    cursor.execute("""
        INSERT INTO `group_user` (`id`, `user_id`, `group_id`, `is_group_manager`, `created_at`, `created_by`, `updated_at`, `updated_by`) VALUES
        (1,	1,	1,	0,	'2017-05-28 14:10:59',	NULL,	'2017-05-28 14:10:59',	NULL),
        (2,	4,	2,	0,	'2017-09-07 09:46:13',	1,	'2017-09-07 09:46:13',	1),
        (3,	5,	2,	0,	'2017-09-19 12:48:11',	1,	'2017-09-19 12:48:11',	1),
        (4,	6,	2,	0,	'2017-11-22 18:25:47',	1,	'2017-11-22 18:25:47',	1),
        (5,	6,	1,	0,	'2017-11-22 18:26:12',	1,	'2017-11-22 18:26:12',	1),
        (6,	5,	3,	0,	'2017-11-30 13:48:39',	1,	'2017-11-30 13:48:39',	1);""")

    cursor.close()
    conn.commit()
    conn.close()

Mysqld = testing.mysqld.MysqldFactory(cache_initialized_db=True,
                                      on_initialized=handler)

mysqld = Mysqld()
args = {
    'host': mysqld.dsn()['host'],
    'port': mysqld.dsn()['port'],
    'dbname': mysqld.dsn()['db'],
    'dbuser': mysqld.dsn()['user'],
    'dbpasswd': '',
    'trigger': '!bot'
}
dbconn = HumhubConnector(**args)

def tearDownModule():
    mysqld.stop()
    Mysqld.clear_cache()

class MyTestCase(unittest.TestCase):
    def test_connection(self):
        self.assertIsNotNone(dbconn)

    def test_userID(self):
        self.assertEqual(dbconn.bot_id, 5)

    def test_checkLatestMessageID(self):
        self.assertEqual(dbconn.current_id, 7)

    def test_checkNewDBMessage(self):
        conn = mysql.connector.connect(**mysqld.dsn())
        cursor = conn.cursor()
        cursor.execute("INSERT INTO `message_entry` "
            "(`message_id`, `user_id`, `content`, `created_at`, `created_by`, `updated_at`, `updated_by`) VALUES"
            "(1,	1,	'!bot Test',	'2017-10-02 11:51:03',	1,	'2017-10-02 11:51:03',	1);")
        cursor.close()
        conn.commit()
        conn.close()
        self.assertEqual(dbconn.getNextID(), 8)

    def test_getNewDBMessage(self):
        self.assertEqual(dbconn.getMessage(8), {'message': 'Test', 'message_id': 1})

    def test_saveToDB(self):
        dbconn.send({'reply': 'Bots Answer', 'message_id': 1})

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
