.. Rasahub documentation master file, created by
   sphinx-quickstart on Thu Nov 16 10:57:36 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Rasahub's documentation!
===================================

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


----

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   configuration
   usage
   plugin_model
   command_hooks


.. toctree::
   :maxdepth: 2
   :caption: APIDoc:

   rasahub
   modules


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
