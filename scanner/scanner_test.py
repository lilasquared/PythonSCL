from unittest import TestCase
from scanner.scanner import Scanner
from _constants import *


class ScannerTest(TestCase):
    def test_constructor(self):
        s = Scanner('hello')
        self.assertEqual(s.position, 0)
        self.assertEqual(s.current_char, 'h')

    def test_advance(self):
        s = Scanner('hello')
        s.advance()
        self.assertEqual(s.position, 1)
        self.assertEqual(s.current_char, 'e')

    def test_skip_whitespace(self):
        s = Scanner('h    e')
        s.advance()
        s.skip_whitespace()
        self.assertEqual(s.current_char, 'e')

    def test_integer(self):
        s = Scanner('12345')
        result = s.integer()
        self.assertEqual(result, 12345)

    def test_get_next_integer(self):
        s = Scanner('1')
        result = s.get_next_token()
        self.assertEqual(result.type, TOKEN_INTEGER)
        self.assertEqual(result.value, 1)

    def test_get_next_token_identifier(self):
        s = Scanner('abc')
        result = s.get_next_token()
        self.assertEqual(result.type, TOKEN_IDENTIFIER)
        self.assertEqual(result.value, 'abc')

        s1 = Scanner('a1234')
        result = s1.get_next_token()
        self.assertEqual(result.type, TOKEN_IDENTIFIER)
        self.assertEqual(result.value, 'a1234')