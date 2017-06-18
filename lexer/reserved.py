from _token import Token
from lexer.constants import *

RESERVED_LOOKUP = {
    'FUNCTION': Token(TOKEN_FUNCTION),
    'BEGIN': Token(TOKEN_BEGINFUNCTION),
    'ENDFUN': Token(TOKEN_ENDFUNCTION),
    'RETURN': Token(TOKEN_RETURN),
    'DISPLAY': Token(TOKEN_DISPLAY),
    'LET': Token(TOKEN_LET),
    'IF': Token(TOKEN_IF),
    'THEN': Token(TOKEN_THEN),
    'ELSE': Token(TOKEN_ELSE),
    'ENDIF': Token(TOKEN_ENDIF)
}
