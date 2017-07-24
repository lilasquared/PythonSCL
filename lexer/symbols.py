#  Aaron Roberts
#  CS4308 – Concepts of Programming Language
#  Summer 2017 Online

# symbols used by the Lexer class

from constants import *

SYMBOL_LOOKUP = {
    '+': TOKEN_ADD,
    '-': TOKEN_SUB,
    '*': TOKEN_MUL,
    '/': TOKEN_DIV,
    '^': TOKEN_POW,
    '<=': TOKEN_LTE,
    '>=': TOKEN_GTE,
    '<': TOKEN_LT,
    '>': TOKEN_GT,
    '==': TOKEN_EQ,
    '~=': TOKEN_NEQ,
    '=': TOKEN_ASSIGN,
    '(': TOKEN_LPAREN,
    ')': TOKEN_RPAREN,
    '[': TOKEN_LBRACKET,
    ']': TOKEN_RBRACKET,
    ',': TOKEN_COMMA,
}

ARITHMETIC_OPERATOR_LOOKUP = {
    TOKEN_ADD,
    TOKEN_SUB,
    TOKEN_MUL,
    TOKEN_DIV
}