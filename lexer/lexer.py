from _token import Token, ValueToken
from lexer.constants import *
from lexer.reserved import RESERVED_LOOKUP
from lexer.symbols import SYMBOL_LOOKUP


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.position = -1
        self.current_line = 1
        self.current_token = None
        self.last_char = None
        self.current_char = None
        self.next_char = None

        self.pipeline = [
            self.end_of_line,
            self.skip_whitespace,
            self.end_of_file,
            self.comment,
            self.integer_literal,
            self.string_literal,
            self.symbol,
            self.word,
        ]

        self.__errors = []
        self.advance()

    def __error(self):
        self.__errors.append({'line': self.current_line, 'char': self.last_char})

    def errors(self):
        return self.__errors

    def advance(self):
        if self.last_char == '\n':
            self.current_line += 1

        self.position += 1
        self.last_char = self.current_char

        if self.position > len(self.text) - 1:
            self.current_char = None
            self.next_char = None
        else:
            self.current_char = self.text[self.position]
            if self.position > len(self.text) - 2:
                self.next_char = None
            else:
                self.next_char = self.text[self.position + 1]


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

    def comment(self):
        result = ''
        start_position = self.position
        if self.current_char != '/':
            return

        self.advance()
        if self.current_char is None or (self.current_char != '/' and self.current_char != '*'):
            self.position = start_position
            return

        if self.current_char == '/':
            self.advance()
            while self.current_char is not None and self.current_char != '\n':
                result += self.current_char
                self.advance()
            return ValueToken(TOKEN_COMMENT, result)

        if self.current_char == '*':
            self.advance()
            while self.current_char is not None and self.current_char != '*' and self.next_char != '/':
                result += self.current_char
                self.advance()
            self.advance()
            self.advance()
            return ValueToken(TOKEN_COMMENT, result)

    def symbol(self):
        if self.current_char not in SYMBOL_LOOKUP:
            return

        if self.next_char not in SYMBOL_LOOKUP:
            self.advance()
            return SYMBOL_LOOKUP[self.last_char]

        symbol = self.current_char + self.next_char
        if symbol in SYMBOL_LOOKUP:
            self.advance()
            self.advance()
            return SYMBOL_LOOKUP[symbol]

        self.advance()
        return SYMBOL_LOOKUP[self.last_char]

    def word(self):
        result = ''
        if not self.current_char.isalpha():
            return

        result += self.current_char
        self.advance()
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        key = result.lower()
        if key in RESERVED_LOOKUP:
            return RESERVED_LOOKUP[key]
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
                return result

        self.__error()
