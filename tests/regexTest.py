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
        self.assertEqual(infixToPostfix("' '|\n|\t"), "' '\n|\t|#.")
        self.assertEqual(infixToPostfix("(A)((A|B|C|D)|(0|1|2|3|4|5|6|7|8|9))*"), "A.((AB|C|D|)(01|2|3|4|5|6|7|8|9|)|)* . ")




if __name__ == '__main__':
    unittest.main()
