
class RasahubMessage():
    """Class of rasahub Message object

    """

    def __init__(self, message = None, message_id = None, target = None, source = None):
        """Init-Method sets message parameters.

        Args:
            message: Message content
            message_id: ID of message
            target: Target plugin of message
            source: Source plugin of the message

        """
        self.message = message
        self.message_id = message_id
        self.target = target
        self.source = source

    def __str__(self):
        """String-Method returns message as string

        Returns:
            message content as string

        """
        return self.message
