
class ToStringBuilder:
    """
    Builds a string representation from an object. Based on the ToStringBuilder
    from Apache Commons Lang.
    """

    def __init__(self, name):
        self.name = name
        self.fields = []

    def append(self, name, value):
        self.fields.append("{}={}".format(name, value))
        return self

    def to_string(self):
        return self.name + "[" + ",".join(self.fields) + "]"
