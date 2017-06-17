from unittest import TestCase
from lexer.lexer import Lexer
from _constants import *


class LexerTest(TestCase):
    def test_constructor(self):
        s = Lexer('hello')
        self.assertEqual(s.position, 0)
        self.assertEqual(s.current_char, 'h')

    def test_advance(self):
        s = Lexer('hello')
        s.advance()
        self.assertEqual(s.position, 1)
        self.assertEqual(s.current_char, 'e')

    def test_skip_whitespace(self):
        s = Lexer('h    e')
        s.advance()
        s.skip_whitespace()
        self.assertEqual(s.current_char, 'e')

    def test_integer(self):
        s = Lexer('12345')
        result = s.integer()
        self.assertEqual(result.value, 12345)

    def test_get_next_integer(self):
        s = Lexer('1')
        result = s.get_next_token()
        self.assertEqual(result.type, TOKEN_INTEGER)
        self.assertEqual(result.value, 1)

    def test_get_next_token_identifier(self):
        s = Lexer('abc')
        result = s.get_next_token()
        self.assertEqual(result.type, TOKEN_IDENTIFIER)
        self.assertEqual(result.value, 'abc')

        s1 = Lexer('a1234')
        result = s1.get_next_token()
        self.assertEqual(result.type, TOKEN_IDENTIFIER)
        self.assertEqual(result.value, 'a1234')