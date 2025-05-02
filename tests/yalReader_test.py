import unittest
from src.Yalex.yalReader import yalReader

code = """(* Lexer para Gramática No. 2 - Expresiones aritméticas extendidas *)

(* Introducir cualquier header aqui *)

let delim = ['\s''\t''\n']
let ws = delim+
let letter = ['A'-'Z''a'-'z']
let digit = ['0'-'9']
let digits = digit+
let id = letter(letter|digit)*
let number = digits('.'digits)?('E'['+''-']?digits)?

rule tokens = 
    ws        { return WHITESPACE }               (* Cambie por una acción válida, que devuelva el token *)
  | id        { return ID }
  | number    { return NUMBER }
  | '+'       { return PLUS }
  | '-'       { return MINUS }
  | '*'       { return TIMES }
  | '/'       { return DIV }
  | '('       { return LPAREN }
  | ')'       { return RPAREN }

(* Introducir cualquier trailer aqui *)
"""
code2 = """{header}
let delim = [' ''\t''\n']
let ws = delim+
let letter = ['A'-'Z''a'-'z']
let digit = ['0'-'9']
let id = letter(letter|digit)*

rule tokens = 
    ws
  | id        { return ID }               
  | '+'       { return PLUS }
  | '*'       { return TIMES }
  | '('       { return LPAREN }
  | ')'       { return RPAREN }"""

# yal = yalReader(code)


yal2 = yalReader("[' ''\t''\n']")
yal2.list.append("delim")
yal2.dicc = {"delim": "['+''\t''\n']"}

yal3 = yalReader("['a'-'d']")
yal3.list.append("delim")
yal3.dicc = {"delim": "['a'-'d']"}

regex = "(((0|1|2|3|4|5|6|7|8|9))+)(\\.(((0|1|2|3|4|5|6|7|8|9))+))?(E(\\+|-)?(((0|1|2|3|4|5|6|7|8|9))+))?"
regez = "(((0|1|2|3|4|5|6|7|8|9)+)(\\.((0|1|2|3|4|5|6|7|8|9)+))?(E(\\+|-)?((0|1|2|3|4|5|6|7|8|9)+)))?"
yal5 = yalReader("[\"+\t\n\"]")
yal5.list.append("delim")
yal5.list.append("delim2")
yal5.dicc = {"delim": "['a'-'d']", "delim2": "delim+['a']"}


class MyTestCase(unittest.TestCase):
    def test_delete_comments(self):
        self.assertEqual(yal.remove_comments(), code2)  # add assertion here

    def test_read(self):
        self.assertEqual(yalReader(code), True)

    def test_parse(self):
        self.assertEqual(" |\t|\n", yal2.parse())

    def test_parse2(self):
        self.assertEqual("a|b|c|d", yal3.parse())

    def test_parse3(self):
        yal4 = yalReader("[\"\s\t\n\"]")
        yal4.list.append("delim")
        yal4.dicc = {"delim": "[\"\s\t\n\"]"}
        self.assertEqual("\s|\t|\n", yal4.parse())

    def test_ascci(self):
        self.assertEqual("b|c|d", yal2.get_ascii("a", "d"))

    def test_parse4(self):
        self.assertEqual("(a|b|c|d)+a", yal5.parse())


    def test_parse5(self):
        yalReader(code)


if __name__ == '__main__':
    unittest.main()
