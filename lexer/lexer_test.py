from unittest import TestCase

from constants import *
from lexer.lexer import Lexer


class LexerTest(TestCase):
    def test_handles_empty_string(self):
        lut = Lexer('')
        result = lut.get_next_token()
        self.assertEqual(result.type, TOKEN_EOF)

    def test_handles_whitespace(self):
        lut = Lexer('        ')
        result = lut.get_next_token()
        self.assertEqual(result.type, TOKEN_EOF)

    def test_handles_integer_literal(self):
        lut = Lexer('12345')
        result = lut.get_next_token()
        self.assertEqual(result.type, TOKEN_INTEGER_LITERAL)
        self.assertEqual(result.value, 12345)

    def test_continues_after_integer_literal(self):
        lut = Lexer('12345 54321')

        result = lut.get_next_token()
        self.assertEqual(result.type, TOKEN_INTEGER_LITERAL)
        self.assertEqual(result.value, 12345)

        result = lut.get_next_token()
        self.assertEqual(result.type, TOKEN_INTEGER_LITERAL)
        self.assertEqual(result.value, 54321)

    def test_handles_string_literal(self):
        string1 = 'this is a string !@#$^woooo 1234'
        lut = Lexer('"{string1}"'.format(string1=string1))
        result = lut.get_next_token()
        self.assertEqual(result.type, TOKEN_STRING_LITERAL)
        self.assertEqual(result.value, string1)

    def test_continues_after_string_literal(self):
        string = 'this is a string !@#$^woooo 1234'
        integer = 12345
        lut = Lexer('"{string}" {integer}'.format(string=string, integer=integer))
        result = lut.get_next_token()
        self.assertEqual(result.type, TOKEN_STRING_LITERAL)
        self.assertEqual(result.value, string)

        result = lut.get_next_token()
        self.assertEqual(result.type, TOKEN_INTEGER_LITERAL)
        self.assertEqual(result.value, integer)

    def test_handles_inline_comment(self):
        comment = 'comment'
        lut = Lexer('//{comment}'.format(comment=comment))
        result = lut.get_next_token()
        self.assertEqual(result.type, TOKEN_COMMENT)
        self.assertEqual(result.value, comment)

    def test_continues_after_inline_comment(self):
        comment = 'this is a string !@#$^woooo 1234'
        integer = 12345
        lut = Lexer("""//{comment}
        {integer}""".format(comment=comment, integer=integer))
        lut.get_next_token() #comment
        self.assertEqual(lut.get_next_token().type, TOKEN_EOL)

        result = lut.get_next_token()
        self.assertEqual(result.type, TOKEN_INTEGER_LITERAL)
        self.assertEqual(result.value, integer)

    def test_handles_multi_line_comment(self):
        comment = """this is
        going to be a comment
        that spans many lines"""
        lut = Lexer('  /*{comment}*/  '.format(comment=comment))
        result = lut.get_next_token()
        self.assertEqual(result.type, TOKEN_COMMENT)
        self.assertEqual(result.value, comment)

    def test_continues_after_multi_line_comment(self):
        comment = """this is
                going to be a comment
                that spans many lines"""
        integer = 12345
        lut = Lexer('  /*{comment}*/  {integer}'.format(comment=comment, integer=integer))

        lut.get_next_token()
        result = lut.get_next_token()

        self.assertEqual(result.type, TOKEN_INTEGER_LITERAL)
        self.assertEqual(result.value, integer)

    def test_handles_single_character_symbol(self):
        lut = Lexer('+')
        result = lut.get_next_token()
        self.assertEqual(result.type, TOKEN_ADD)

    def test_continues_after_single_character_symbol(self):
        integer = 12345
        lut = Lexer('+ {integer}'.format(integer=integer))

        lut.get_next_token()
        result = lut.get_next_token()

        self.assertEqual(result.type, TOKEN_INTEGER_LITERAL)
        self.assertEqual(result.value, integer)

    def test_handles_valid_double_character_symbol(self):
        lut = Lexer('==')
        result = lut.get_next_token()
        self.assertEqual(result.type, TOKEN_EQ)

    def test_handles_invalid_double_character_symbol(self):
        lut = Lexer('[]')
        self.assertEqual(lut.get_next_token().type, TOKEN_LBRACKET)
        self.assertEqual(lut.get_next_token().type, TOKEN_RBRACKET)

    def test_handles_identifier_abc123(self):
        lut = Lexer('abc123')
        result = lut.get_next_token()
        self.assertEqual(result.type, TOKEN_IDENTIFIER)
        self.assertEqual(result.value, 'abc123')

    def test_handles_identifier_abc_123(self):
        lut = Lexer('abc_123')
        result = lut.get_next_token()
        self.assertEqual(result.type, TOKEN_IDENTIFIER)
        self.assertEqual(result.value, 'abc_123')

    def test_handles_reserved_word(self):
        lut = Lexer('BEGIN')
        result = lut.get_next_token()
        self.assertEqual(result.type, TOKEN_BEGINFUNCTION)

    def test_continues_after_reserved_word(self):
        lut = Lexer('FUNCTION main')

        lut.get_next_token()
        result = lut.get_next_token()

        self.assertEqual(result.type, TOKEN_MAIN)

    def test_assigns_correct_line_number_to_token(self):
        lut = Lexer("""12345
        54321
        /*
        long
        comment
        */
        12345
        """)
        integer = lut.get_next_token()
        self.assertEqual(integer.line_number, 1)

        eol = lut.get_next_token()
        self.assertEqual(eol.line_number, 1)

        integer2 = lut.get_next_token()
        self.assertEqual(integer2.line_number, 2)

        eol = lut.get_next_token()
        self.assertEqual(eol.line_number, 2)

        comment = lut.get_next_token()
        self.assertEqual(comment.line_number, 6)

        eol = lut.get_next_token()
        self.assertEqual(eol.line_number, 6)

        integer2 = lut.get_next_token()
        self.assertEqual(integer2.line_number, 7)

    def test_collects_errors(self):
        lut = Lexer('&')
        lut.get_next_token()
        self.assertEqual(len(lut.errors()), 1)
