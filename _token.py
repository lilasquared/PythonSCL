class Token(object):
    def __init__(self, type):
        self.type = type

    def __str__(self):
        return 'Token({type})'.format(type=self.type)

    def __repr__(self):
        return self.__str__()

class ValueToken(Token):
    def __init__(self, type, value):
        Token.__init__(self, type)
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(type=self.type, value=self.value)

    def __repr__(self):
        return self.__str__()