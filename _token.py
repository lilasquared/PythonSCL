class Token(object):
    def __init__(self, type):
        self.type = type
        self.line_number = None

    def __str__(self):
        return '{number}: Token({type})'.format(type=self.type, number=self.line_number)

    def __repr__(self):
        return self.__str__()

class ValueToken(Token):
    def __init__(self, type, value):
        Token.__init__(self, type)
        self.value = value

    def __str__(self):
        return '{number}: Token({type}, {value})'.format(number=self.line_number, type=self.type, value=self.value)

    def __repr__(self):
        return self.__str__()