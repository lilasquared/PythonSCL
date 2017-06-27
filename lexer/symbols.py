from _token import Token
from lexer.constants import *

SYMBOL_LOOKUP = {
    '+': Token(TOKEN_ADD),
    '-': Token(TOKEN_SUB),
    '*': Token(TOKEN_MUL),
    '/': Token(TOKEN_DIV),
    '^': Token(TOKEN_POW),
    '<=': Token(TOKEN_LTE),
    '>=': Token(TOKEN_GTE),
    '<': Token(TOKEN_LT),
    '>': Token(TOKEN_GT),
    '==': Token(TOKEN_EQ),
    '~=': Token(TOKEN_NEQ),
    '=': Token(TOKEN_ASSIGN),
    '(': Token(TOKEN_LPAREN),
    ')': Token(TOKEN_RPAREN),
    '[': Token(TOKEN_RBRACKET),
    ']': Token(TOKEN_LBRACKET),
    ',': Token(TOKEN_COMMA),
}
