.. Usage doc

Usage
=====

Configuration
-------------

First, you have to create a configuration, initializing all your plugins and
route messages. Needed parameters for each plugin should be in there respective
documentation. Following a basic debug-configuration to get an idea:

.. code-block:: YAML

    debug1:
      package: 'rasahub_debug'
      classname: 'DebugConnector'
      init:
        host: '127.0.0.1'
        port: 5020
      out: 'debug2'
      type: 'interface'

    debug2:
      package: 'rasahub_debug'
      classname: 'DebugConnector'
      init:
        host: '127.0.0.1'
        port: 5021
      out: 'debug1'
      type: 'interface'


Save this as config.yml in your current directory.


Starting
--------

Now you can start rasahub using:

.. code-block:: bash

    python -m rasahub
