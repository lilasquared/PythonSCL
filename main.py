from lexer.constants import TOKEN_EOF
from lexer.lexer import Lexer

with open('sample_program.scl') as f:
    text = ''.join(s for s in f.readlines())

lexer = Lexer(text)
token = lexer.get_next_token()
tokens = [token]
while token.type is not TOKEN_EOF:
    token = lexer.get_next_token()
    tokens.append(token)

[print(token) for token in tokens]