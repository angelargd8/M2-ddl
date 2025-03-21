
#un metacaracter o metachar es un caracter que se usa en expresiones regulres para definir criterios de busqueda y manipulacion de texto
class Metachar:
    def __init__(self, value):
        self.value = value
    
    #funcion para determinar el orden de las operaciones de una expresion regular
    def getPrecedence(self, operator):
        precedence = {
        "(":1, 
        "|":2, 
        ".":3, 
        "?":4, 
        "*":4, 
        "+":4, 
        "^":5
        }
        return precedence.get(operator, 6)
    
    def IsOperator(self):
        return self.value in {'|', '?','+','*','^','∗'}
    
    def IsBinaryOperator(self):
        return self.value in {'^', '|'}

    def getValue(self):
        return self.value