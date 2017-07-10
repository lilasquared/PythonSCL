#  Aaron Roberts
#  CS4308 – Concepts of Programming Language
#  Summer 2017 Online

# Unit tests for the parser class

from unittest import TestCase

from constants import *
from lexer.lexer import Lexer
from _parser.parser import Parser


class Parser_Test(TestCase):
    def __construct_parser(self, program):
        lexer = Lexer(program)
        parser = Parser(lexer)

        return parser

    def test_import(self):
        parser = self.__construct_parser('import "abc"')

        statements = parser.parse()

        self.assertEqual(len(statements), 1)
        self.assertEqual(statements[0].type, STATEMENT_IMPORT)

    def test_import_error(self):
        parser = self.__construct_parser('import 123')

        statements = parser.parse()

        self.assertEqual(len(statements), 0)
        self.assertEqual(len(parser.errors), 1)

    def test_symbol(self):
        parser = self.__construct_parser('symbol MM 45')

        statements = parser.parse()

        self.assertEqual(len(statements), 1)
        self.assertEqual(statements[0].type, STATEMENT_SYMBOL)

    def test_symbol_error(self):
        parser = self.__construct_parser('symbol "MM" 45')

        statements = parser.parse()

        self.assertEqual(len(statements), 0)
        self.assertEqual(len(parser.errors), 1)

    def test_display(self):
        parser = self.__construct_parser('display myvar, "string_literal", otherVar, "other string" ')

        statements = parser.parse()

        self.assertEqual(len(statements), 1)
        self.assertEqual(statements[0].type, STATEMENT_DISPLAY)

    def test_display_error(self):
        parser = self.__construct_parser('display myvar, function')

        statements = parser.parse()

        self.assertEqual(len(statements), 0)
        self.assertEqual(len(parser.errors), 1)