from _token import Token
from lexer._constants import *

RESERVED_LOOKUP = {
    'BEGIN': Token(TOKEN_BEGIN)
}


def isreserved(str):
    return str in RESERVED_LOOKUP
