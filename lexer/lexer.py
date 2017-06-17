from _token import Token, ValueToken
from lexer._constants import *
from lexer.reserved import RESERVED_LOOKUP, isreserved
from lexer.symbols import SYMBOL_LOOKUP, issymbol


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.current_token = None
        self.current_char = self.text[self.position]

    @staticmethod
    def error():
        raise Exception('Invalid Syntax')

    def advance(self):
        self.position += 1
        if self.position > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.position]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def alnum_string(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        return result

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return ValueToken(TOKEN_INTEGER, int(result))

    def symbol(self):
        result = ''
        while self.current_char is not None and issymbol(self.current_char):
            result += self.current_char
            self.advance()
        if issymbol(result):
            return SYMBOL_LOOKUP[result]
        else:
            raise Exception('Unexpected Symbol {symbol}'.format(symbol=self.current_char))

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return self.integer()
            if issymbol(self.current_char):
                return self.symbol()
            if self.current_char.isalpha():
                alnum_string = self.alnum_string()
                if isreserved(alnum_string):
                    return RESERVED_LOOKUP[alnum_string]

        return Token(TOKEN_EOF)
