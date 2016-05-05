
class FilterContext():
    """
    ContextManager to make adding multiple subscriptions with the same filter easier.
    Uses the python "with" statement.

    TODO: Perhaps rather than using the constructor directly, add a method to message_bus to
    create a FilterContext instead?

    """

    def __init__(self, messagebus, message_filter):

        self.messagebus = messagebus
        self.message_filter = message_filter

    def add(self, handler):
        self.messagebus.subscribe(handler, self.message_filter)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
