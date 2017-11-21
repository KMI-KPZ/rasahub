=======
Rasahub
=======

Rasahub connects `Rasa_Core`_ with `Humhub`_ `Mail`_ .
It contains the database-connector for a Humhub installation and a socket-connector
for RasahubInputChannel which then can be used in Rasa_Core as an input channel.
Rasahub listens for new messages in the database with a bot trigger in the beginning
or direct messages to the bot, sends the messages to Rasa_core using the message_id
and saves the response from Rasa_Core in the Humhub database.

Feel free to extend the database-connector to another mailsystem or develop an API-connector.

----

Prerequisites
=============

* Python installed
* Humhub database access (if remote: make sure you have port 3306 opened)

Installation
============

Pypi package
------------

Install via pip:

    pip install rasahub

Usage
=====

Command-Line API
----------------

Start rasahub:

    rasahub <<parameters>>

Parameters
----------

+------------+------------------+---------------------------------------+-----------+-------------+
| Parameter  | Parameter(long)  | Description                           | Required  | Default     |
+============+==================+=======================================+===========+=============+
| -dbu       | --dbuser         | Database username                     | required  | -           |
+------------+------------------+---------------------------------------+-----------+-------------+
| -dbp       | --dbpwd          | Database userpassword                 | required  | -           |
+------------+------------------+---------------------------------------+-----------+-------------+
| -dbh       | --dbhost         | Database host                         | optional  | 127.0.0.1   |
+------------+------------------+---------------------------------------+-----------+-------------+
| -dbn       | --dbname         | Database name                         | required  | -           |
+------------+------------------+---------------------------------------+-----------+-------------+
| -t         | --trigger        | Trigger-word (!bot for example)       | optional  | \!bot       |
+------------+------------------+---------------------------------------+-----------+-------------+
| -id        | --botid          | The bots Humhub-User ID               | required  | -           |
+------------+------------------+---------------------------------------+-----------+-------------+
| -rh        | --rasahost       | The hostaddress of Rasa_Core          | optional  | 127.0.0.1   |
+------------+------------------+---------------------------------------+-----------+-------------+
| -rp        | --rasaport       | The port of RasahubInputchannel       | optional  | 5020        |
+------------+------------------+---------------------------------------+-----------+-------------+

Example call
------------

    rasahub -dbu humuser -dbp secretpassword -dbn humhub -t !bot -id 5

Configuring Rasa
================

In your Rasa bots run.py just import the channel using

    from rasahub.rasahubchannel import RasahubInputChannel

And let the agent handle the channel:

    agent.handle_channel(RasahubInputChannel('127.0.0.1', 5020))



* License: MIT
* `PyPi`_ - package installation

.. _Rasa_Core: https://github.com/RasaHQ/rasa_core
.. _Humhub: https://www.humhub.org/de/site/index
.. _Mail: https://github.com/humhub/humhub-modules-mail
.. _PyPi: https://pypi.python.org/pypi/rasahub
