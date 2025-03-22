import unittest
from Yalex.yalReader import yalReader


code = """(* hola soy un 
comentario yupi(*
*)
{header}
let delim = [' ''\t''\n']
let ws = delim+
let letter = ['A'-'Z''a'-'z']
let digit = ['0'-'9']
let id = letter(letter|digit)*

rule tokens = 
    ws
  | id        { return ID }               (* Cambie por una acción válida, que devuelva el token *)
  | '+'       { return PLUS }
  | '*'       { return TIMES }
  | '('       { return LPAREN }
  | ')'       { return RPAREN }

(* Introducir cualquier trailer aqui *)
"""
code2 = """let delim = [' ''\t''\n']
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

yal = yalReader(code)

yal2 = yalReader("[' ''\t''\n']")
yal2.list.append("delim")
yal2.dicc = {"delim": "[' ''\t''\n']"}

yal3 = yalReader("['a'-'d']")
yal3.list.append("delim")
yal3.dicc = {"delim": "['a'-'d']"}

class MyTestCase(unittest.TestCase):
    def test_delete_comments(self):
        self.assertEqual(yal.remove_comments(), code2)  # add assertion here

    def test_read(self):
        self.assertEqual(yal.read_yalex(), True)

    def test_parse(self):
        self.assertEqual(" |\t|\n", yal2.parse())

    def test_parse2(self):
        self.assertEqual("a|b|c|d", yal3.parse())

    def test_ascci(self):
        self.assertEqual("b|c|d", yal2.get_ascii("a", "d"))

if __name__ == '__main__':
    unittest.main()
