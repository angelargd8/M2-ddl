import os
from constructor import leerArchivo, construirArbolSintactico, construirArbol
from regex import infixToPostfix
from afn import *
from AFD import *
from node import *
from collections import deque, defaultdict
from graficadora import visualize_afd
import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler and a stream handler
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
    # print(ArbolSintactico)
    # logger.info('Arbol sintactico construido')

    # # el followpos es la tablita para saber las posiciones que se tienen que seguir
    followpos = defaultdict(set)
    calcular_followPos(ArbolSintactico, followpos)
    # # logger.info('Followpos calculado')
    # print('followpos')
    # print(followpos)

    # # construir el AFD
    afd = construir_AFD(ArbolSintactico, followpos)
    afd = minimizar_afd(afd)
    # # logger.info('AFD construido')
    return afd


expresiones = leerArchivo("./expresiones.txt")

# Procesar cada expresión regular y generar el AFD
for i, expresion in enumerate(expresiones):
    logger.info(f'Procesando expresion {i+1}: {expresion}')
    postfix = infixToPostfix(expresion)
    logger.info(f'Expresion POSTFIX: {postfix}')

    afd = construirAFD(postfix)

    afd.mostrar()
    logger.info('AFD mostrado')

    # Generar la imagen del AFD usando la función de visualización
    # Aquí usamos la expresión regular como parte del nombre, pero se sanitiza internamente.
    visualize_afd(afd, output_dir="Visual_AFD", file_name=f"AFD_{i}")
    logger.info(f'Imagen del AFD generada: AFD_{i}')