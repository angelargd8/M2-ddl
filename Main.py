# Laboratorio - Construcción Directa de AFD y ecosistema de reconocimiento de expresiones regulares
# autores: - Francis Alguilar, 22243
#         - Cesar Lopez, 22505
#         - Angela Garcia, 22869
"""
El objetivo es desarrollar la base del generador de analizadores léxicos. A partir de r deberá construir un AFD, utilizando el algoritmo de construcción directa.

Objetivos

Generales
- Implementación de (algunos) algoritmos básicos de autómatas finitos y expresiones regulares.
- Desarrollar la base de la implementación del generador de analizadores léxicos.

especificos:
Implementación del algoritmo de Construcción directa de AFD (DFA): el que vimos en este curso, que toma una RE y la transforma en un AFD.
Implementación del algoritmo de Minimización de AFD (DFA), simulación de un AFN, simulación de un AFD, Generación visual de los AF, 
Shunting yard para convertir de infix a postfix

funcionamiento del programa:
Debe aceptar expresiones regulares para definir el AFD y también cadenas para procesarlas.
Al procesar las expresiones regulares, muestre en pantalla el AFD.
Luego permita procesar cadenas, y para cada una indique si es aceptada o no.

"""

import os

from constructor import leerArchivo, construirArbol, construirArbolSintactico
from graficadora import graficar_afd
from regex import infixToPostfix
from afn import *
from AFD import *
from node import *
from collections import deque, defaultdict


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

    nombre_archivo = f"AFD {i} "
    afd.mostrar()
