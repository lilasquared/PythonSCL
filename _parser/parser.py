from constants import *
from _parser.rules import SIMPLE_STATEMENT_RULES

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None
        self.statements = []
        self.errors = []
        self.rules = [
            self.__import,
            self.__symbol,
            self.__variable_definition
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

    def __variable_definition(self):
        tokens = self.__check(SIMPLE_STATEMENT_RULES[STATEMENT_VARIABLE_DEF])
        if (len(tokens) == 0): return

        if (self.current_token.type == TOKEN_TYPE_INTEGER):
            tokens.append(self.current_token)
            self.statements.append(Statement(STATEMENT_VARIABLE_DEF, tokens))
            return

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