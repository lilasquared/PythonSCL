#  Aaron Roberts
#  CS4308 – Concepts of Programming Language
#  Summer 2017 Online

# Parser class used to identify statements from groups of tokens from the lexer (scanner)

from constants import *
from _parser.rules import SIMPLE_STATEMENT_RULES, TYPE_TOKENS

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None
        self.statements = []
        self.errors = []
        self.rules = [
            self.__import,
            self.__symbol,
            self.__variable_def,
            self.__function_def,
            self.__constant_def,
            self.__display
        ]

    def __advance(self):
        self.current_token = self.lexer.get_next_token()

    def __error(self):
        self.errors.append('Unexpected Token : {token}'.format(token=self.current_token.__str__()))

    def __check(self, token_order):
        statement_tokens = []
        for token_index, token_type in enumerate(token_order):
            if (self.current_token.type != token_type):
                if (token_index == 0):
                    return []
                else:
                    self.__error()
                    return []
            statement_tokens.append(self.current_token)
            self.__advance()
        return statement_tokens

    def __import(self):
        tokens = self.__check(SIMPLE_STATEMENT_RULES[STATEMENT_IMPORT])
        if (len(tokens) == 0): return
        self.statements.append(Statement(STATEMENT_IMPORT, tokens))

    def __symbol(self):
        tokens = self.__check(SIMPLE_STATEMENT_RULES[STATEMENT_SYMBOL])
        if (len(tokens) == 0): return
        self.statements.append(Statement(STATEMENT_SYMBOL, tokens))

    def __variable_def(self):
        tokens = self.__check(SIMPLE_STATEMENT_RULES[STATEMENT_VARIABLE_DEF])
        if (len(tokens) == 0): return

        if (self.current_token.type not in TYPE_TOKENS):
            self.__error()
            return

        tokens.append(self.current_token)
        self.statements.append(Statement(STATEMENT_VARIABLE_DEF, tokens))

    def __function_def(self):
        tokens = self.__check(SIMPLE_STATEMENT_RULES[STATEMENT_FUNCTION_DEF])
        if (len(tokens) == 0): return

        if (self.current_token.type not in TYPE_TOKENS):
            self.__error()
            return

        tokens.append(self.current_token)
        self.statements.append(Statement(STATEMENT_FUNCTION_DEF, tokens))

    def __constant_def(self):
        tokens = self.__check(SIMPLE_STATEMENT_RULES[STATEMENT_CONSTANT_DEF])
        if (len(tokens) == 0): return
        self.statements.append(Statement(STATEMENT_CONSTANT_DEF, tokens))

    def __display(self):
        if (self.current_token.type != TOKEN_DISPLAY): return
        tokens = [self.current_token]
        self.__advance()

        if (self.current_token.type != TOKEN_STRING_LITERAL and self.current_token.type != TOKEN_IDENTIFIER):
            self.__error()
            return

        tokens.append(self.current_token)
        self.__advance()

        while (True):
            if (self.current_token.type != TOKEN_COMMA):
                break

            tokens.append(self.current_token)
            self.__advance()

            if (self.current_token.type != TOKEN_STRING_LITERAL and self.current_token.type != TOKEN_IDENTIFIER):
                self.__error()
                return

            tokens.append(self.current_token)
            self.__advance()

        self.statements.append(Statement(STATEMENT_DISPLAY, tokens))

    def parse(self):
        self.__advance()
        while self.current_token.type != TOKEN_EOF:
            for rule in self.rules:
                rule()
            self.__advance()

        return self.statements


class Statement(object):
    def __init__(self, type, tokens):
        self.type = type
        self.tokens = tokens

    def __str__(self):
        str = self.type + ' | '
        for token in self.tokens:
            str += token.__str__() + ', '
        return str

    def __repr__(self):
        return self.__str__()

class Identifier(object):
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value