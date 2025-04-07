from Automata.constructor import leerArchivo
from Automata.arboles import *
from Automata.Regex import *
from Automata.AFD import *
from Automata.Node import *
from collections import defaultdict
import logging

# Create a logger
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

# # Create a file handler and a stream handlerh
# file_handler = logging.FileHandler("afd_generation.log")
# stream_handler = logging.StreamHandler()

# Create a formatter and add it to the handlers
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# file_handler.setFormatter(formatter)
# stream_handler.setFormatter(formatter)


# Add the handlers to the logger
# logger.addHandler(file_handler)
# logger.addHandler(stream_handler)


def construirAFD(postfix):
    # construir el arbol sintactico para la cadena
    postfix = infixToPostfix(expresion)
    postfixTokenizado = tokenize_postfix(postfix)
    ArbolSintactico = construirArbolSintactico(postfixTokenizado)

    if ArbolSintactico:
        print("arbol construido correctamente")
        imprimirArbolSintactico(ArbolSintactico, "", True)

    else:
        print("Error al construir el arbol sintactico")
        return None

    # # # el followpos es la tablita para saber las posiciones que se tienen que seguir
    followpos = defaultdict(set)
    calcular_followPos(ArbolSintactico, followpos)

    # # # construir el AFD
    afd = construir_AFD(ArbolSintactico, followpos)

    return afd


# expresiones = leerArchivo("../expresiones.txt")

# Procesar cada expresión regular y generar el AFD
# for i, expresion in enumerate(expresiones):
    # logger.info(f"Procesando expresion {i + 1}: {expresion} \n")

# expresion = "#bb|*a.b.b*.ab|*.#."
# expresion = "01|2|3|4|5|6|7|8|9|+01|2|3|4|5|6|7|8|9|+?.E\+-|?.01|2|3|4|5|6|7|8|9|+.?.#."
expresion = "(((0|1|2|3|4|5|6|7|8|9))+)(\\.(((0|1|2|3|4|5|6|7|8|9))+))?(E(\\+|-)?(((0|1|2|3|4|5|6|7|8|9))+))?"


afd = construirAFD(expresion)

    # afd.mostrar()
