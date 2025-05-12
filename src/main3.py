from collections import defaultdict
from Automata.arboles import *
from Automata.Regex import *
from Automata.AFD import *
from Automata.graficadora import visualize_afd
from typing import List, Union
import os
def leerArchivo(file: str) -> Union[List[str], str]:
    try:
        script_dir = os.path.dirname(__file__)  # Directorio del script actual
        file_path = os.path.join(script_dir, file)

        with open(file_path, "r", encoding="utf-8") as f:
            expresiones = f.read().split("\n")

        print(expresiones, type(expresiones))
        return expresiones
    except FileNotFoundError:
        return "El archivo no fue encontrado"
    except IOError:
        return "Error al leer el archivo"
    

def construirAFD(postfix):
    # construir el arbol sintactico para la cadena
    print('procesando la expresion postfix: ' + str(postfix))
    postfixTokenizado = tokenize_postfix(postfix)

    ArbolSintactico = construirArbolSintactico(postfixTokenizado)

    if ArbolSintactico:
        print("arbol construido correctamente")
        imprimirArbolSintactico(ArbolSintactico, "", True)

    else:
        print("Error al construir el arbol sintactico")
        return None

    # # # # el followpos es la tablita para saber las posiciones que se tienen que seguir
    followpos = defaultdict(set)
    calcular_followPos(ArbolSintactico, followpos)

    # # # construir el AFD
    afd = construir_AFD(ArbolSintactico, followpos)
    
    return afd


# expresion = "bb|*a.b.b*.ab|*.#."
# expresion = "01|2|3|4|5|6|7|8|9|+01|2|3|4|5|6|7|8|9|+?.E\+-|?.01|2|3|4|5|6|7|8|9|+.?.#."
# expresion = "01|2|3|4|5|6|7|8|9|+\\.01|2|3|4|5|6|7|8|9|+?.e\\+-|?.01|2|3|4|5|6|7|8|9|+.?.#."

token1 = "(((0|1|2|3|4|5|6|7|8|9))+)(\\.(((0|1|2|3|4|5|6|7|8|9))+))?(E(\\+|-)?(((0|1|2|3|4|5|6|7|8|9))+))?"
token2 = "(\\s|\t|\n)+"
token3 = "(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)((A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)|(0|1|2|3|4|5|6|7|8|9))*"
token4= "\\+"
token5 = "-"
token6 = "\\*"
token7 = "/"
token8 = "\\("
token9 = "\\)"

expresion1 = infixToPostfix(token1)
expresion2 = infixToPostfix(token2)
expresion3 = infixToPostfix(token3)
expresion4 = infixToPostfix(token4)
expresion5 = infixToPostfix(token5)
expresion6 = infixToPostfix(token6)
expresion7 = infixToPostfix(token7)
expresion8 = infixToPostfix(token8)
expresion9 = infixToPostfix(token9)


afd , estados_dict , estado_id_a_conjunto =construirAFD(expresion1)
afd , estados_dict , estado_id_a_conjunto =construirAFD(expresion2)
afd , estados_dict , estado_id_a_conjunto =construirAFD(expresion3)
afd , estados_dict , estado_id_a_conjunto =construirAFD(expresion4)
afd , estados_dict , estado_id_a_conjunto =construirAFD(expresion5)
afd , estados_dict , estado_id_a_conjunto =construirAFD(expresion6)
afd , estados_dict , estado_id_a_conjunto =construirAFD(expresion7)
afd , estados_dict , estado_id_a_conjunto =construirAFD(expresion8)
afd , estados_dict , estado_id_a_conjunto =construirAFD(expresion9)


visualize_afd(afd, output_dir="Visuall", file_name=f"AFD")

# afd.mostrar()

