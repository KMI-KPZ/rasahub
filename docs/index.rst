.. Rasahub documentation master file, created by
   sphinx-quickstart on Thu Nov 16 10:57:36 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Rasahub's documentation!
===================================

Rasahub connects `Rasa_Core`_ with `Humhub`_ `Mail`_ .

It contains the database-connector for a Humhub installation and a socket-connector
for RasahubInputChannel which then can be used in Rasa_Core as an input channel.

Rasahub listens for new messages in the database with a bot trigger in the beginning
or direct messages to the bot, sends the messages to Rasa_core using the message_id
and saves the response from Rasa_Core in the Humhub database.

Feel free to extend the database-connector to another mailsystem or develop an API-connector.

----

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   rasainputchannel


.. toctree::
   :maxdepth: 2
   :caption: APIDoc:

   rasaconnector
   dbconnector


* License: MIT
* `PyPi`_ - package installation

.. _Rasa_Core: https://github.com/RasaHQ/rasa_core
.. _Humhub: https://www.humhub.org/de/site/index
.. _Mail: https://github.com/humhub/humhub-modules-mail
.. _PyPi: https://pypi.python.org/pypi/rasahub
