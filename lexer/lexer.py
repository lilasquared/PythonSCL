from _token import Token, ValueToken
from lexer.constants import *
from lexer.reserved import RESERVED_LOOKUP
from lexer.symbols import SYMBOL_LOOKUP


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.current_line = 1
        self.current_token = None
        self.current_char = self.text[self.position]

        self.pipeline = [
            self.end_of_file,
            self.end_of_line,
            self.skip_whitespace,
            self.integer_literal,
            self.string_literal,
            self.symbol,
            self.word,
        ]

    def error(self):
        raise Exception('Unexpected token: {token}'.format(token=self.current_char))

    def advance(self):
        self.position += 1
        if self.position > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.position]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer_literal(self):
        result = ''
        if not self.current_char.isdigit():
            return

        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        return ValueToken(TOKEN_INTEGER_LITERAL, int(result))

    def string_literal(self):
        result = ''
        if self.current_char is not SPECIAL_STRING_CAP:
            return

        self.advance()
        while self.current_char is not None and self.current_char is not SPECIAL_STRING_CAP:
            result += self.current_char
            self.advance()
        self.advance()

        return ValueToken(TOKEN_STRING_LITERAL, result)

    def symbol(self):
        result = ''
        if self.current_char not in SYMBOL_LOOKUP:
            return

        while self.current_char is not None and self.current_char in SYMBOL_LOOKUP:
            result += self.current_char
            self.advance()

        if result in SYMBOL_LOOKUP:
            return SYMBOL_LOOKUP[result]
        else:
            raise Exception('Unexpected Symbol {symbol}'.format(symbol=self.current_char))

    def word(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        if result in RESERVED_LOOKUP:
            return RESERVED_LOOKUP[result]
        else:
            return ValueToken(TOKEN_IDENTIFIER, result)

    def end_of_line(self):
        if self.current_char == '\n':
            self.advance()
            return Token(TOKEN_EOL)

    def end_of_file(self):
        if self.current_char is None:
            return Token(TOKEN_EOF)

    def get_next_token(self):
        for test in self.pipeline:
            result = test()
            if isinstance(result, Token):
                result.line_number = self.current_line
                if result.type is TOKEN_EOL:
                    self.current_line += 1
                return result

        self.error()