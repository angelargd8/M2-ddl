#un metacaracter o metachar es un caracter que se usa en expresiones regulres para definir criterios de busqueda y manipulacion de texto
class Metachar:

    #se cambio la clase con metodos estaticos, porque el value que se obtenia, no se le hacia un uso realmente mas que valdiar

    #se define la precedencia de los metacaracteres, para el manejo de la expresion regular
    precedence = {
        "(": 1,
        "|": 2,
        ".": 3,
        "?": 4,
        "*": 4,
        "+": 4,
        "^": 5
    }

    #funcion para determinar el orden de las operaciones de una expresion regular
    @staticmethod
    def getPrecedence(operator):
        return Metachar.precedence.get(operator, 6)

    @staticmethod
    def IsOperator(char):
        return char in {'|', '?', '+', '*', '^', '∗', '.'}

    @staticmethod
    def IsBinaryOperator(char):
        return char in {'^', '|', '.'}

    @staticmethod
    def IsEscaped(char):
        return char in {'t', 'n', 'r', 'v', '\\', '0', '|', '?', '+', '*', '^', '∗', '(', ')', 's', '-'}

    @staticmethod
    def IsQuoted(char):
        return char in {'"', "'", "`"}

    
