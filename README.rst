=======
Rasahub
=======

.. image:: https://travis-ci.org/frommie/Rasahub.svg?branch=master
    :target: https://travis-ci.org/frommie/Rasahub

Rasahub connects `Rasa_Core`_ with `Humhub`_ `Mail`_ .
It contains the database-connector for a Humhub installation and a socket-connector
for RasahubInputChannel which then can be used in Rasa_Core as an input channel.
Rasahub listens for new messages in the database with a bot trigger in the beginning
or direct messages to the bot, sends the messages to Rasa_core using the message_id
and saves the response from Rasa_Core in the Humhub database.

Feel free to extend the database-connector to another mailsystem or develop an API-connector.

Please read the `Documentation`_ .

----

Prerequisites
=============

* Python installed
* Humhub database access (if remote: make sure you have port 3306 opened)
* Bots Humhub User Group created (name 'Bots')
* Assign Bot User to Bots User Group in Humhub Backend

Installation
============

Pypi package
------------

Install via pip:

.. code-block:: bash

  pip install rasahub


Usage
=====

Create configuration
--------------------

Create file config.yml in working path. Example:

.. code-block:: yaml

  rasa:
    host: '127.0.0.1'
    port: 5020

  humhub:
    host: '127.0.0.1'
    port: 3306
    dbname: 'humhub'
    dbuser: 'humhubuser'
    dbpasswd: 'humhub123'
    trigger: '!bot'


Command-Line API
----------------

Start rasahub:

.. code-block:: bash

  python -m rasahub



Configuring Rasa
================

In your Rasa bots run.py just import the channel using

.. code-block:: python

  from rasahub.rasahubchannel import RasahubInputChannel


And let the agent handle the channel:

.. code-block:: python

  agent.handle_channel(RasahubInputChannel('127.0.0.1', 5020))



Testing
=======

Prerequisites:

* mysql-server installed
* testing dependencies installed: pip install .[test]

Run Test:

.. code-block:: python

  python -m pytest tests/



* License: MIT
* `PyPi`_ - package installation

.. _Rasa_Core: https://github.com/RasaHQ/rasa_core
.. _Humhub: https://www.humhub.org/de/site/index
.. _Mail: https://github.com/humhub/humhub-modules-mail
.. _PyPi: https://pypi.python.org/pypi/rasahub
.. _Documentation: https://rasahub.readthedocs.io
