

class RasahubMessage():
    """
    Message object
    """

    def __init__(self, message = None, message_id = None, target = None, source = None):
        self.message = message
        self.message_id = message_id
        self.target = target
        self.source = source

    def __str__(self):
        return self.message
