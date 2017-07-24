#  Aaron Roberts
#  CS4308 – Concepts of Programming Language
#  Summer 2017 Online

# Reserved words used by the lexer class

from constants import *

RESERVED_LOOKUP = {
    'import': TOKEN_IMPORT,
    'symbol': TOKEN_SYMBOL,
    'forward': TOKEN_FORWARD,
    'global': TOKEN_GLOBAL,
    'specifications': TOKEN_SPECIFICATIONS,
    'references': TOKEN_REFERENCES,
    'function': TOKEN_FUNCTION,
    'declarations': TOKEN_DECLARATIONS,
    'implementations': TOKEN_IMPLEMENTATIONS,
    'main': TOKEN_MAIN,
    'parameters': TOKEN_PARAMETERS,
    'variables': TOKEN_VARIABLES,
    'constants': TOKEN_CONSTANTS,
    'begin': TOKEN_BEGINFUNCTION,
    'endfun': TOKEN_ENDFUNCTION,
    'if': TOKEN_IF,
    'then': TOKEN_THEN,
    'else': TOKEN_ELSE,
    'endif': TOKEN_ENDIF,
    'repeat': TOKEN_REPEAT,
    'until': TOKEN_UNTIL,
    'endrepear': TOKEN_ENDREPEAT,
    'display': TOKEN_DISPLAY,
    'set': TOKEN_SET,
    'return': TOKEN_RETURN,
    'define': TOKEN_DEFINE,
    'of': TOKEN_OF,
    'type': TOKEN_TYPE,
    'array': TOKEN_TYPE_ARRAY,
    'struct': TOKEN_TYPE_STRUCT,
    'pointer': TOKEN_TYPE_POINTER,
    'integer': TOKEN_TYPE_INTEGER,
    'short': TOKEN_TYPE_SHORT,
    'enum' : TOKEN_TYPE_ENUM
}
