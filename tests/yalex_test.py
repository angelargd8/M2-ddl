import unittest
from Yalex.yalReader import yalReader

code = """(* hola soy un 
comentario yupi(*
*)

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


class MyTestCase(unittest.TestCase):
    def test_delete_comments(self):
        self.assertEqual(yalReader.remove_comments(code), code2)  # add assertion here


if __name__ == '__main__':
    unittest.main()
