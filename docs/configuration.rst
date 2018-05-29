.. Configuration doc

Configuration parameters
========================

+------------+---------------------------------------+-----------+
| Parameter  | Description                           | Required  |
+============+=======================================+===========+
| package    | Python package name of plugin         | required  |
+------------+---------------------------------------+-----------+
| init       | Initialization parameters             | required  |
+------------+---------------------------------------+-----------+
| out        | Output route                          | required  |
+------------+---------------------------------------+-----------+


Create configuration file
-------------------------

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
