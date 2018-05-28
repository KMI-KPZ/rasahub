.. Configuration doc

Configuration parameters
========================

+------------+---------------------------------------+-----------+
| Parameter  | Description                           | Required  |
+============+=======================================+===========+
| package    | Python package name of plugin         | required  |
+------------+---------------------------------------+-----------+
| classname  | Name of plugin class                  | required  |
+------------+---------------------------------------+-----------+
| init       | Initialization parameters             | required  |
+------------+---------------------------------------+-----------+
| out        | Output route                          | required  |
+------------+---------------------------------------+-----------+
| type       | Type of plugin, see below             | required  |
+------------+---------------------------------------+-----------+

Plugin types
------------

Currently there are three plugin types implemented:

* interface: Receives and sends user-facing messages
* interpreter: Receives message, interpretes and sends back interpreted message
* datastore: Will not be started but serves as data provider
