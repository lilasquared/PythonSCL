from unittest import TestCase
from symbols import issymbol

class SymbolsTest(TestCase):

    def test_valid_symbols(self):
        valid_symbols = ['+', '-', '*', '/', '<=', '>=', '<', '>', '==', '~=', '=', '(', '(']
        for symbol in valid_symbols:
            self.assertEqual(True, issymbol(symbol), "Symbol '{symbol}' failed test".format(symbol=symbol))

    def test_invalid_symbols(self):
        invalid_symbols = ['!', '@', '#', '$', '%', '^', '&', '_', '`', 'a', '1']
        for symbol in invalid_symbols:
            self.assertEqual(False, issymbol(symbol), "Symbol '{symbol}' failed test".format(symbol=symbol))