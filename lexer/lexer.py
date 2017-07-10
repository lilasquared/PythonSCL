from _token import Token, ValueToken
from constants import *
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
            self.__end_of_line,
            self.__skip_whitespace,
            self.__end_of_file,
            self.__comment,
            self.__integer_literal,
            self.__string_literal,
            self.__symbol,
            self.__word,
        ]

        self.__errors = []
        self.__advance()

    #
    # Public method to retrieve next token from the given input text.
    # Will return token of type TOKEN_EOF when the end of the input stream is reached
    # Errors are collected internally and accessed via errors() method
    #
    def get_next_token(self):
        for test in self.pipeline:
            result = test()
            if isinstance(result, Token):
                result.line_number = self.current_line
                return result

        self.__error()

    #
    # Public method to retrieve array of all errors found.
    # Errors have a line_number property indicating which line the error was found
    #   and a char property indicating which character caused the error.
    #
    def errors(self):
        return self.__errors

    def __error(self):
        self.__errors.append({'line_number': self.current_line, 'char': self.last_char})

    def __advance(self):
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


    def __skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.__advance()

    def __integer_literal(self):
        result = ''
        if not self.current_char.isdigit():
            return

        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.__advance()

        return ValueToken(TOKEN_INTEGER_LITERAL, int(result))

    def __string_literal(self):
        result = ''
        if self.current_char is not SPECIAL_STRING_CAP:
            return

        self.__advance()
        while self.current_char is not None and self.current_char is not SPECIAL_STRING_CAP:
            result += self.current_char
            self.__advance()
        self.__advance()

        return ValueToken(TOKEN_STRING_LITERAL, result)

    def __comment(self):
        result = ''
        start_position = self.position
        if self.current_char != '/':
            return

        self.__advance()
        if self.current_char is None or (self.current_char != '/' and self.current_char != '*'):
            self.position = start_position
            return

        if self.current_char == '/':
            self.__advance()
            while self.current_char is not None and self.current_char != '\n':
                result += self.current_char
                self.__advance()
            return ValueToken(TOKEN_COMMENT, result)

        if self.current_char == '*':
            self.__advance()
            while self.current_char is not None and self.current_char != '*' and self.next_char != '/':
                result += self.current_char
                self.__advance()
            self.__advance()
            self.__advance()
            return ValueToken(TOKEN_COMMENT, result)

    def __symbol(self):
        if self.current_char not in SYMBOL_LOOKUP:
            return

        if self.next_char not in SYMBOL_LOOKUP:
            self.__advance()
            return SYMBOL_LOOKUP[self.last_char]

        symbol = self.current_char + self.next_char
        if symbol in SYMBOL_LOOKUP:
            self.__advance()
            self.__advance()
            return SYMBOL_LOOKUP[symbol]

        self.__advance()
        return SYMBOL_LOOKUP[self.last_char]

    def __word(self):
        result = ''
        if not self.current_char.isalpha():
            return

        result += self.current_char
        self.__advance()
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.__advance()

        key = result.lower()
        if key in RESERVED_LOOKUP:
            return Token(RESERVED_LOOKUP[key])
        else:
            return ValueToken(TOKEN_IDENTIFIER, result)

    def __end_of_line(self):
        if self.current_char == '\n':
            self.__advance()
            return Token(TOKEN_EOL)

    def __end_of_file(self):
        if self.current_char is None:
            return Token(TOKEN_EOF)
