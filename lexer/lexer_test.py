from unittest import TestCase

from lexer.constants import *
from lexer.lexer import Lexer


class LexerTest(TestCase):
    def test_constructor(self):
        lut = Lexer('hello')
        self.assertEqual(lut.position, 0)
        self.assertEqual(lut.current_char, 'h')

    def test_advance(self):
        lut = Lexer('hello')
        lut.advance()
        self.assertEqual(lut.position, 1)
        self.assertEqual(lut.current_char, 'e')

    def test_skip_whitespace(self):
        lut = Lexer('h    e')
        lut.advance()
        lut.skip_whitespace()
        self.assertEqual(lut.current_char, 'e')

    def test_integer_literal(self):
        lut = Lexer('12345')
        result = lut.integer_literal()
        self.assertEqual(result.value, 12345)

    def test_string_literal(self):
        lut = Lexer('"this is a string !@#$^woooo 1234"')
        result = lut.string_literal()
        self.assertEqual(result.type, TOKEN_STRING_LITERAL)
        self.assertEqual(result.value, 'this is a string !@#$^woooo 1234')

    def test_inline_comment(self):
        lut = Lexer('//comment')
        result = lut.comment()
        self.assertEqual(result.type, TOKEN_COMMENT)
        self.assertEqual(result.value, 'comment')

        lut = Lexer("""  //this is a very
        long string if I had the
        energy to type more and more ...""")
        result = lut.comment()
        self.assertEqual(result.type, TOKEN_COMMENT)
        self.assertEqual(result.value, 'this is a very')

    def test_multi_line_comment(self):
        comment = """this is
        going to be a comment
        that spans many lines"""
        lut = Lexer('/*{comment}*/'.format(comment=comment))
        result = lut.comment()
        self.assertEqual(result.type, TOKEN_COMMENT)
        self.assertEqual(result.value, comment)

    def test_symbol(self):
        lut = Lexer('+')
        result = lut.symbol()
        self.assertEqual(result.type, TOKEN_ADD)

    def test_word_identifier(self):
        lut = Lexer('abc123')
        result = lut.word()
        self.assertEqual(result.type, TOKEN_IDENTIFIER)
        self.assertEqual(result.value, 'abc123')

    def test_word_reserved(self):
        lut = Lexer('BEGIN')
        result = lut.word()
        self.assertEqual(result.type, TOKEN_BEGINFUNCTION)

    def test_get_all_tokens(self):
        lut = Lexer('BEGIN 123 abc ENDFUN')
        result = lut.get_all_tokens()
        self.assertEqual(5, len(result))