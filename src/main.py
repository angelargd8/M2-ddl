from constructor import leerArchivo
from arboles import construirArbolSintactico, imprimirArbolSintactico
from Regex import infixToPostfix
from Automata.AFD import *
from node import *
from collections import defaultdict
from graficadora import visualize_afd
import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler and a stream handlerh
file_handler = logging.FileHandler('afd_generation.log')
stream_handler = logging.StreamHandler()

# Create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)


# Add the handlers to the logger
# logger.addHandler(file_handler)
# logger.addHandler(stream_handler)


def construirAFD(postfix):
    # construir el arbol sintactico para la cadena
    ArbolSintactico = construirArbolSintactico(postfix)

    if ArbolSintactico:
        print("arbol construido correctamente")
        imprimirArbolSintactico(ArbolSintactico, "", True)

    else:
        print("Error al construir el arbol sintactico")


    # # # el followpos es la tablita para saber las posiciones que se tienen que seguir
    followpos = defaultdict(set)
    calcular_followPos(ArbolSintactico, followpos)

    # # # construir el AFD
    afd = construir_AFD(ArbolSintactico, followpos)

    return afd


expresiones = leerArchivo("../expresiones.txt")

# Procesar cada expresión regular y generar el AFD
for i, expresion in enumerate(expresiones):
    logger.info(f'Procesando expresion {i + 1}: {expresion} \n')
    postfix = infixToPostfix(expresion)
    print(f'Expresion POSTFIX: {postfix}\n')

    afd = construirAFD(postfix)

    # afd.mostrar()
    logger.info('AFD mostrado')

    # Generar la imagen del AFD usando la función de visualización
    # Aquí usamos la expresión regular como parte del nombre, pero se sanitiza internamente.
    visualize_afd(afd, output_dir="Visual_AFD", file_name=f"AFD_{i}")
    logger.info(f'Imagen del AFD generada: AFD_{i}')