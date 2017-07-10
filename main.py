from lexer.lexer import Lexer
from _parser.parser import Parser

path = input('Path to SCL source program: ')

try:
    with open(path) as f:
        text = ''.join(s for s in f.readlines())
except:
    raise Exception('invalid input or bad file path')

lexer = Lexer(text)
parser = Parser(lexer)

statements = parser.parse()

[print(s) for s in statements]
[print(e) for e in parser.errors]