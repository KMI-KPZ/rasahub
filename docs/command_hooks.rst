.. Command Hooks doc

Command Hooks
=============

Before sending out of plugins you can access the message object and modify it.
Commands are stated as $command_name$ and are suffixed with parameters in
dumped JSON format.

All hooks are defined in the plugins process_command function:

    def process_command(self, command, payload, out_message):

The command is the command_name without '$'. The payload contains
* payload['args']: Arguments after $command_name$
* payload['message_id']: Origin message ID
* payload['message_source']: Origin message source
* payload['message_target']: Origin message target
