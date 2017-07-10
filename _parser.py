from constants import *


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None
        self.statements = []
        self.errors = []
        self.simple_statement_rules = {
            STATEMENT_IMPORT: [TOKEN_IMPORT, TOKEN_STRING_LITERAL],
            STATEMENT_SYMBOL: [TOKEN_SYMBOL, TOKEN_IDENTIFIER, TOKEN_INTEGER_LITERAL],

        }
        self.rules = [
            self.__make_simple_statment_check(STATEMENT_IMPORT),
            self.__make_simple_statment_check(STATEMENT_SYMBOL)
        ]

    def __advance(self):
        self.current_token = self.lexer.get_next_token()

    def __error(self):
        self.errors.append('Unexpected Token : {type}'.format(type=self.current_token.type))

    def __make_simple_statment_check(self, type):
        _this = self
        def check():
            token_order = _this.simple_statement_rules[type]
            statement_tokens = []
            for token_index, token_type in enumerate(token_order):
                if (_this.current_token.type != token_type):
                    if (token_index == 0):
                        return
                    else:
                        _this.__error()
                        return
                statement_tokens.append(_this.current_token)
                _this.__advance()
            _this.statements.append(Statement(type, statement_tokens))
        return check

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
        return self.type

    def __repr__(self):
        return self.__str__()

class Identifier(object):
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value