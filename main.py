from lexer.constants import TOKEN_EOF
from lexer.lexer import Lexer

path = input('Path to SCL source program: ')

try:
    with open(path) as f:
        text = ''.join(s for s in f.readlines())
except:
    raise Exception('invalid input or bad file path')

lexer = Lexer(text)
token = None
while token is None or (token is not None and token.type is not TOKEN_EOF):
    try:
        token = lexer.get_next_token()
    except Exception as ex:
        print(ex)

    print(token)