=======
Rasahub
=======

.. image:: https://travis-ci.org/frommie/rasahub.svg?branch=master
    :target: https://travis-ci.org/frommie/rasahub


Rasahub provides an message interface to connect user interfaces with chatbots
and several, data-providing services. Therefore it uses a plugin model.

Currently there are following plugins available:

* `Rasahub-Rasa`_ to send and get messages to and from `Rasa_Core`_ .
* `Rasahub-Humhub`_ to read and save messages from and to `Humhub`_ `Mail`_ .
* `Rasahub-Google-Calendar`_ to retrieve and save calendar entries from and to Google Calendar.
* `Rasahub-Debug`_ to send and receive messages to and from a socket debugger called `Rasahub-Debug-Client`_ .


These plugins are available as source and also as pypi packages:

* Rasahub: pip install rasahub
* Rasahub-Rasa: pip install rasahub-rasa
* Rasahub-Humhub: pip install rasahub-humhub
* Rasahub-Google-Calendar: pip install rasahub-google-calendar
* Rasahub-Debug: pip install rasahub-debug
* Rasahub-Debug-Client: pip install rasahub-debug-client


Feel free to develop your own plugin!

Please read the `Documentation`_ .

----

Prerequisites
=============

* Python installed

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

You can use the built-in configuration creation tool.
Be sure to install your desired plugins before running the tool, for example
rasahub_humhub and rasahub_rasa. Afterwards you can call the tool like follows:

.. code-block:: bash

    python3 -m rasahub.config -p rasahub_humhub rasahub_rasa -o config2.yml


+------------+-------------------------------------------+-----------+
| Parameter  | Description                               | Required  |
+============+===========================================+===========+
| -p         | Lists all plugins                         | required  |
+------------+-------------------------------------------+-----------+
| -o         | sets the output config file path and name | required  |
+------------+-------------------------------------------+-----------+


Manually create configuration
-----------------------------

Create file config.yml in working path. Example:

.. code-block:: yaml

  rasa:
    package: 'rasahub_rasa'
    classname: 'RasaConnector'
    out: 'humhub'
    type: 'interpreter'
    init:
      host: '127.0.0.1'
      port: 5020

  humhub:
    package: 'rasahub_humhub'
    classname: 'HumhubConnector'
    out: 'rasa'
    type: 'interface'
    init:
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

  python -m rasahub -c config.yml


+------------+------------------------------+-----------+------------+
| Parameter  | Description                  | Required  | Default    |
+============+==============================+===========+============+
| -c         | Path to configuration file   | optional  | config.yml |
+------------+------------------------------+-----------+------------+



Testing
=======

Prerequisites:

* testing dependencies installed: pip install .[test]

Run Test:

.. code-block:: python

  python -m pytest tests/



* License: MIT
* `PyPi`_ - package installation


.. _Rasahub-Rasa: https://github.com/frommie/rasahub-rasa
.. _Rasahub-Humhub: https://github.com/frommie/rasahub-humhub
.. _Rasahub-Google-Calendar: https://github.com/frommie/rasahub-google-calendar
.. _Rasahub-Debug: https://github.com/frommie/rasahub-debug
.. _Rasahub-Debug-Client: https://github.com/frommie/rasahub-debug-client
.. _Rasa_Core: https://github.com/RasaHQ/rasa_core
.. _Humhub: https://www.humhub.org/de/site/index
.. _Mail: https://github.com/humhub/humhub-modules-mail
.. _PyPi: https://pypi.python.org/pypi/rasahub
.. _Documentation: https://rasahub.readthedocs.io
