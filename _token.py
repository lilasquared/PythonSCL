#  Aaron Roberts
#  CS4308 – Concepts of Programming Language
#  Summer 2017 Online

# Token class used to store token type and line number

class Token(object):
    def __init__(self, type):
        self.type = type
        self.line_number = None

    def __str__(self):
        return '{number}: Token({type})'.format(type=self.type, number=self.line_number)

    def __repr__(self):
        return self.__str__()

# ValueToken class inherited from Token class used to store token type, line number, and value

class ValueToken(Token):
    def __init__(self, type, value):
        Token.__init__(self, type)
        self.value = value

    def __str__(self):
        return '{number}: Token({type}, {value})'.format(number=self.line_number, type=self.type, value=self.value)

    def __repr__(self):
        return self.__str__()