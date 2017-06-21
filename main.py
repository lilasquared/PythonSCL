from lexer.constants import TOKEN_EOF
from lexer.lexer import Lexer

with open('sample_program.scl') as f:
    text = ''.join(s for s in f.readlines())

lexer = Lexer(text)
token = None
while token is None or (token is not None and token.type is not TOKEN_EOF):
    try:
        token = lexer.get_next_token()
    except Exception as ex:
        print(ex)

    print(token)