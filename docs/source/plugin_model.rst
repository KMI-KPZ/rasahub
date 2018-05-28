.. Plugin Model doc

How to write your own plugin
============================

To develop your own Rasahub plugin and provide it as a pypi package there are a
few steps needed.

First, create a directory to store all your plugin files, for example:
'example-plugin'.
Then, create another directory in your newly created one with the name of your
plugin with rasahub\_ prefix. For example: rasahub_example.

In example-plugin you have to create following files:

* LICENSE.txt - containing the license information of your plugin

* MANIFEST.in - containing following string:

.. code-block:: bash

    include LICENSE README.rst


* README.rst - with a basic documentation of your plugin

* setup.py - with setup information for python.

Content of setup.py
-------------------

In setup.py you state the plugins name, dependency, version and so on. A basic
example of setup.py looks like this:

.. code-block:: python

   from setuptools import setup, find_packages

   install_requires = [
       'rasahub',
   ]

   tests_requires = [
   ]

   extras_requires = {
       'test': tests_requires
   }

   setup(name='rasahub-example',
         version='0.0.1',
         description='Example plugin for Rasahub',
         url='http://github.com/frommie/rasahub-example',
         author='Jon Doe',
         author_email='jon.doe@foobar.baz',
         license='MIT',
         classifiers=[
             'Development Status :: 3 - Alpha',
             'License :: OSI Approved :: MIT License',
             'Intended Audience :: Developers',
             'Programming Language :: Python :: 2.7',
             'Topic :: Software Development',
         ],
         keywords='rasahub example plugin',
         packages=find_packages(exclude=['docs', 'tests']),
         install_requires=install_requires,
         tests_require=tests_requires,
         extras_require=extras_requires,
   )


The Plugin Itself
-----------------

After we created all the python-related files we can start developing the
plugin itself!
In your rasahub_example directory create a file called __init__.py . There
you define your Plugin class and the initialization method:

.. code-block:: python

    from rasahub import RasahubPlugin
    from rasahub.message import RasahubMessage

    import fancy_api

        class ExamplePlugin(RasahubPlugin):
            """
            ExamplePlugin is subclass of RasahubPlugin
            """
            def __init__(self, **kwargs):
                """
                Initializes the example plugin
                """

                super(HumhubConnector, self).__init__()

                parameter = kwargs.get('parameter', 'default-value')
                self.exampleparameter = parameter
                self.apiconnection = fancy_api.connect(parameter)


            def send(self, messagedata, main_queue):
                """
                Sends message to example plugin output like socket connection or
                database
                """
                self.apiconnection.save(messagedata)


            def receive(self):
                """
                Receives message from plugin input
                """
                return self.apiconnection.receive()


            def process_command(self, command, payload, out_message):
                """
                Command hook before sending, returns a Rasahub message object
                """
                reply = RasahubMessage(
                    message = "Command unknown",
                    message_id = payload['message_id'],
                    target = payload['message_target'],
                    source = payload['message_source']
                )
                return reply


                def end(self):
                    """
                    Closes connections
                    """
                    self.apiconnection.close()
