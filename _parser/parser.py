#  Aaron Roberts
#  CS4308 – Concepts of Programming Language
#  Summer 2017 Online

# Parser class used to identify statements from groups of tokens from the lexer (scanner)

from lexer.symbols import ARITHMETIC_OPERATOR_LOOKUP
from constants import *
from _parser.rules import SIMPLE_STATEMENT_RULES

identifiers = {}
functions = {}


class Parser(object):
    def __init__(self, lexer):
        self.position = -1
        self.current_token = None
        self.statements = []
        self.errors = []

        self.tokens = []

        current_token = lexer.get_next_token()
        while current_token is not None and current_token.type != TOKEN_EOF:
            while current_token.type == TOKEN_EOL or current_token.type == TOKEN_COMMENT:
                current_token = lexer.get_next_token()
            self.tokens.append(current_token)
            current_token = lexer.get_next_token()

        self.pipeline = [
            self.__import,
            self.__symbol,
            self.__forward_declarations,
            self.__global_declarations,
            self.__variable_definition,
            self.__constant_definition,
            self.__function_definition,
            self.__display,
            self.__input,
            self.__set,
            self.__error
        ]

    def __advance(self):
        self.position = self.position + 1
        if self.position > len(self.tokens) - 1:
            self.current_token = None
            return

        self.current_token = self.tokens[self.position]

    def __reset(self, position):
        self.position = position
        self.current_token = self.tokens[position]

    def __error(self):
        self.errors.append('Unexpected Token : {token}'.format(token=self.current_token.__str__()))
        self.__advance()

    def __check(self, token_order):
        statement_tokens = []
        current_position = self.position
        for token_index, token_type in enumerate(token_order):
            if self.current_token.type != token_type:
                self.__reset(current_position)
                return []

            statement_tokens.append(self.current_token)
            self.__advance()
        return statement_tokens

    def __import(self):
        tokens = self.__check(SIMPLE_STATEMENT_RULES[STATEMENT_IMPORT])
        if len(tokens) == 0: return
        return Statement(STATEMENT_IMPORT, tokens)

    def __symbol(self):
        tokens = self.__check(SIMPLE_STATEMENT_RULES[STATEMENT_SYMBOL])
        if len(tokens) == 0: return
        return Statement(STATEMENT_SYMBOL, tokens)

    def __forward_declarations(self):
        tokens = self.__check(SIMPLE_STATEMENT_RULES[STATEMENT_FORWARD_DECLARATIONS])
        if (len(tokens) == 0): return
        return Statement(STATEMENT_FORWARD_DECLARATIONS, tokens)

    def __global_declarations(self):
        tokens = self.__check(SIMPLE_STATEMENT_RULES[STATEMENT_GLOBAL_DECLARATIONS])
        if (len(tokens) == 0): return
        return Statement(STATEMENT_GLOBAL_DECLARATIONS, tokens)

    def __parameter_definition(self):
        tokens = self.__check(SIMPLE_STATEMENT_RULES[STATEMENT_PARAMETER_DEF])
        if (len(tokens) == 0): return
        return Statement(STATEMENT_PARAMETER_DEF, tokens)

    #
    # When a variable declaration is found the variable is added to the global identifiers dictionary
    # A default value of 0 is assigned to all integer variables
    # If the identifier already exists in the table it is simply overwritten.
    #
    def __variable_definition(self):
        tokens = self.__check(SIMPLE_STATEMENT_RULES[STATEMENT_VARIABLE_DEF])
        if (len(tokens) == 0): return

        identifierName = tokens[1].value

        identifiers[identifierName] = Identifier(identifierName, TOKEN_TYPE_INTEGER, 0)
        return Statement(STATEMENT_VARIABLE_DEF, tokens)

    #
    # When a constant declaration is found the variable is added to the global identifiers dictionary
    # The value provided is assigned to the identifier
    # If the identifier already exists in the table an error is thrown
    #
    def __constant_definition(self):
        tokens = self.__check(SIMPLE_STATEMENT_RULES[STATEMENT_CONSTANT_DEF])
        if (len(tokens) == 0): return

        identifierName = tokens[1].value
        constantValue = tokens[3].value

        identifiers[identifierName] = Identifier(identifierName, TOKEN_TYPE_INTEGER, constantValue)
        return Statement(STATEMENT_CONSTANT_DEF, tokens)

    #
    # When a fuction declaration is found the variable is added to the global functions dictionary
    #
    def __function_definition(self):
        if (self.current_token.type != TOKEN_FUNCTION): return
        tokens = self.__check(SIMPLE_STATEMENT_RULES[STATEMENT_FUNCTION_DEF])

        if (len(tokens) == 0): return

        identifierName = tokens[1].value

        parameters = self.__function_parameters();
        self.__function_variables()
        statements = self.__function_body()

        functions[identifierName] = Function(identifierName, statements, parameters)
        return Statement(STATEMENT_FUNCTION_DEF, tokens)

    def __function_parameters(self):
        if self.current_token.type != TOKEN_PARAMETERS: return
        self.__advance()

        parameters = []
        while self.current_token.type != TOKEN_VARIABLES:
            result = self.__parameter_definition()
            if (result is not None): parameters.append(result)
            else: break
        return parameters

    def __function_variables(self):
        if self.current_token.type != TOKEN_VARIABLES: return
        self.__advance()

        while self.current_token.type != TOKEN_BEGINFUNCTION:
            self.__variable_definition()

    def __function_body(self):
        if self.current_token.type != TOKEN_BEGINFUNCTION: return
        self.__advance()

        statements = []
        while self.current_token.type != TOKEN_ENDFUNCTION:
            statement = self.__try_get_statement()
            if (statement is not None): statements.append(statement)

        return statements

    def __arithmetic_expression(self):
        tokens = []
        if (self.current_token.type != TOKEN_IDENTIFIER): return

        tokens.append(self.current_token)
        self.__advance()

        if (self.current_token.type not in ARITHMETIC_OPERATOR_LOOKUP): return

        tokens.append(self.current_token)
        self.__advance()

        if (self.current_token.type != TOKEN_IDENTIFIER): return

        tokens.append(self.current_token)
        self.__advance()
        return tokens

    def __set(self):
        tokens = self.__check(SIMPLE_STATEMENT_RULES[STATEMENT_SET])
        if (len(tokens) == 0): return

        expression = self.__arithmetic_expression()

        if (expression is None or len(expression) == 0): return

        [tokens.append(e) for e in expression]

        return Statement(STATEMENT_SET, tokens)

    def __input(self):
        tokens = self.__check(SIMPLE_STATEMENT_RULES[STATEMENT_INPUT])
        if (len(tokens) == 0): return

        return Statement(STATEMENT_INPUT, tokens)

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

        return Statement(STATEMENT_DISPLAY, tokens)

    def __try_get_statement(self):
        for test in self.pipeline:
            result = test()
            if isinstance(result, Statement):
                return result

    def parse(self):
        self.__advance()
        while self.current_token is not None and self.current_token.type != TOKEN_EOF:
            statement = self.__try_get_statement()
            if (statement is not None): self.statements.append(statement)

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


class Function(object):
    def __init__(self, name, statements, parameters):
        self.name = name
        self.parameters = parameters
        self.statements = statements

    def __str__(self):
        me = '{name:<20}'.format(name=self.name)
        for s in self.statements:
            me = me + '\n     {s}'.format(s=s)
        return me

    def __repr__(self):
        return self.__str__()