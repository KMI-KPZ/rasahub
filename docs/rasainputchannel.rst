.. Rasainputchannel doc

Configuring Rasa
================

In your Rasa bots run.py just import the channel using

    from rasahub.rasahubchannel import RasahubInputChannel

And let the agent handle the channel:

    agent.handle_channel(RasahubInputChannel('127.0.0.1', 5020))


Communicate with the bot
------------------------

As soon as Rasa_Core is connected you will see a message in Rasahub like

    Connection established: ('127.0.0.1', 47794)

Now you can start sending a message to the bot in Humhub directly
(without the trigger) or trigger the bots action using the bot trigger
(default !bot) in a conversation with another user. You will see new messages
from Humhub and reply messages from Rasa_Core in Rasahub like this:

    Input from db: {
        u'message': u'Ich habe ein Problem mit meiner Tastatur',

        u'message\_id': 4
    }

    Reply from rasa: {
        u'reply': u'Christian Frommert koennte bei dem Anliegen helfen.',

        u'message\_id': 4
    }
