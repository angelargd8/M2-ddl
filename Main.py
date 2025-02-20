# Main.py
import os
from constructor import leerArchivo, construirArbolSintactico
from regex import infixToPostfix
from afn import *
from AFD import *
from node import *
from collections import deque, defaultdict
from graficadora import visualize_afd


def construirAFD(postfix):
    # construir el arbol sintactico para la cadena
    ArbolSintactico = construirArbolSintactico(postfix)
    # print(ArbolSintactico)

    # el followpos es la tablita para saber las posiciones que se tienen que seguir
    followpos = defaultdict(set)
    calcular_followPos(ArbolSintactico, followpos)
    # print(followpos)

    # construir el AFD
    afd = construir_AFD(ArbolSintactico, followpos)
    # afd.mostrar()
    return afd


expresiones = leerArchivo("./expresiones.txt")

# Procesar cada expresión regular y generar el AFD
for i, expresion in enumerate(expresiones):
    print("Expresion ingresada: \n" + expresion)
    postfix = infixToPostfix(expresion)
    print("Expresion POSTFIX \n" + postfix + "\n")

    afd = construirAFD(postfix)

    afd.mostrar()

    # Generar la imagen del AFD usando la función de visualización
    # Aquí usamos la expresión regular como parte del nombre, pero se sanitiza internamente.
    visualize_afd(afd, output_dir="Visual_AFD", file_name=f"AFD_{i}")
