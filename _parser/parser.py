#  Aaron Roberts
#  CS4308 – Concepts of Programming Language
#  Summer 2017 Online

# Parser class used to identify statements from groups of tokens from the lexer (scanner)

from constants import *
from _parser.rules import SIMPLE_STATEMENT_RULES, TYPE_TOKENS

identifiers = {}

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None
        self.statements = []
        self.errors = []

        self.rules = [
            self.__import,
            self.__symbol,
            self.__forward_declarations,
            self.__global_declarations,
            self.__variable_definition,
            self.__constant_definition,
            self.__display
        ]

    def __advance(self):
        self.current_token = self.lexer.get_next_token()
        while(self.current_token.type == TOKEN_EOL or self.current_token.type == TOKEN_COMMENT):
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

    def __forward_declarations(self):
        tokens = self.__check(SIMPLE_STATEMENT_RULES[STATEMENT_FORWARD_DECLARATIONS])
        if (len(tokens) == 0): return
        self.statements.append(Statement(STATEMENT_FORWARD_DECLARATIONS, tokens))

    def __global_declarations(self):
        tokens = self.__check(SIMPLE_STATEMENT_RULES[STATEMENT_GLOBAL_DECLARATIONS])
        if (len(tokens) == 0): return
        self.statements.append(Statement(STATEMENT_GLOBAL_DECLARATIONS, tokens))

    #
    # When a variable declaration is found the variable is added to the global identifiers dictionary
    # A default value of 0 is assigned to all integer variables
    # If the identifier already exists in the table it is simply overwritten.
    #
    def __variable_definition(self):
        if (self.current_token.type != TOKEN_VARIABLES): return
        self.__advance()
        tokens = self.__check(SIMPLE_STATEMENT_RULES[STATEMENT_VARIABLE_DEF])
        while (len(tokens) > 0):
            identifierName = tokens[1].value
            self.statements.append(Statement(STATEMENT_VARIABLE_DEF, tokens))

            identifiers[identifierName] = Identifier(identifierName, TOKEN_TYPE_INTEGER, 0)
            tokens = self.__check(SIMPLE_STATEMENT_RULES[STATEMENT_VARIABLE_DEF])
        return

    #
    # When a constant declaration is found the variable is added to the global identifiers dictionary
    # The value provided is assigned to the identifier
    # If the identifier already exists in the table an error is thrown
    #
    def __constant_definition(self):
        if (self.current_token.type != TOKEN_CONSTANTS): return
        self.__advance()
        tokens = self.__check(SIMPLE_STATEMENT_RULES[STATEMENT_CONSTANT_DEF])
        while (len(tokens) > 0):
            identifierName = tokens[1].value
            constantValue = tokens[3].value
            self.statements.append(Statement(STATEMENT_CONSTANT_DEF, tokens))

            identifiers[identifierName] = Identifier(identifierName, TOKEN_TYPE_INTEGER, constantValue)
            tokens = self.__check(SIMPLE_STATEMENT_RULES[STATEMENT_CONSTANT_DEF])
        return

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

    def __set(self):
        if (self.current_token.type != TOKEN_SET) : return
        tokens = [self.current_token]
        self.__advance()

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

    def __str__(self):
        str = '{name:<20} | {type:<20} | {value:>10}'.format(name=self.name, type=self.type, value=self.value)
        return str

    def __repr__(self):
        return self.__str__()