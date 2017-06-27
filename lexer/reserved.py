from _token import Token
from lexer.constants import *

RESERVED_LOOKUP = {
    'import': Token(TOKEN_IMPORT),
    'symbol': Token(TOKEN_SYMBOL),
    'forward': Token(TOKEN_FORWARD),
    'specifications': Token(TOKEN_SPECIFICATIONS),
    'references': Token(TOKEN_REFERENCES),
    'function': Token(TOKEN_FUNCTION),
    'type': Token(TOKEN_TYPE),
    'struct': Token(TOKEN_TYPE_STRUCT),
    'integer': Token(TOKEN_TYPE_INTEGER),
    'array': Token(TOKEN_TYPE_ARRAY),
    'pointer': Token(TOKEN_TYPE_POINTER),
    'enum' : Token(TOKEN_TYPE_ENUM),
    'declarations': Token(TOKEN_DECLARATIONS),
    'implementations': Token(TOKEN_IMPLEMENTATIONS),
    'main': Token(TOKEN_MAIN),
    'parameters': Token(TOKEN_PARAMETERS),
    'constant': Token(TOKEN_CONSTANT),
    'begin': Token(TOKEN_BEGINFUNCTION),
    'endfun': Token(TOKEN_ENDFUNCTION),
    'if': Token(TOKEN_IF),
    'then': Token(TOKEN_THEN),
    'else': Token(TOKEN_ELSE),
    'endif': Token(TOKEN_ENDIF),
    'repeat': Token(TOKEN_REPEAT),
    'until': Token(TOKEN_UNTIL),
    'endrepear': Token(TOKEN_ENDREPEAT),
    'display': Token(TOKEN_DISPLAY),
    'set': Token(TOKEN_SET),
    'return': Token(TOKEN_RETURN)
}
