import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from Automata.Regex import *

class TestRegex(unittest.TestCase):

    def test_infixToPostfix(self):
        self.assertEqual(infixToPostfix("(a|b)*abb"), "ab|*a.b.b.#.")
        self.assertEqual(infixToPostfix("(a|b)+"), "ab|ab|*.#.")
        self.assertEqual(infixToPostfix("(\t|\n)+"), "\t\n|\t\n|*.#.")
        self.assertEqual(infixToPostfix("(a|b)\+"), "ab|\+.#.")
        self.assertEqual(infixToPostfix("\t|\n"), "\t\n|#.")
        self.assertEqual(infixToPostfix("|\t|\n"), "ε\t|\n|#.")



if __name__ == '__main__':
    unittest.main()
