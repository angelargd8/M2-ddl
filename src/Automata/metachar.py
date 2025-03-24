
#un metacaracter o metachar es un caracter que se usa en expresiones regulres para definir criterios de busqueda y manipulacion de texto
class Metachar:
    def __init__(self, value):

        self.value = value

        self.is_escaped = False#isinstance(value, str) and len(value) > 1 and value[0] == '\\'

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
        if self.is_escaped:
            return False
        return self.value in {'|', '?','+','*','^','∗'}

    def IsBinaryOperator(self):
        if self.is_escaped :
            return False

        return self.value in {'^', '|', '.'}

    def getValue(self):
        return self.value

    def IsEscaped(self):
        if self.value in {'t', 'n', 'r', 'v', '\\', '0', '|', '?','+','*','^','∗'} :
            return True
        return False
