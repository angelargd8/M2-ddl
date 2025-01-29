# Buffer simulator 🤑
# Autores: - Cesar Lopez #22535
#          - Francis Aguilar #22243
#          - Angela Garcia #22869

import os
from typing import List, Tuple

"""
especificaciones:
- El programa debe simular un búfer con un tamaño fijo de 10 caracteres.
- Utilicen una lista de caracteres como entrada, terminando en un carácter especial eof.
- Implementen dos punteros: inicio y avance, para simular la lectura del búfer.
- Cuando el puntero avance alcance el final del búfer, recarguen los datos desde una entrada simulada.
- El programa debe imprimir cada lexema (caracteres entre dos espacios o el final) procesado del búfer.

"""
ruta_actual = os.getcwd()


# leer el archivo
def leer_archivo(archivo: str) -> str:
    return open("../M2-ddl/" + archivo, "r").read()


# Código base para iniciar
def cargar_buffer(entrada: List[str], inicio: int, tamano_buffer: int) -> List[str]:
    buffer = entrada[inicio : inicio + tamano_buffer]
    return buffer


def procesar_buffer(
    bufferCount: int,
    buffer: List[str],
    lexema_incompleto: str = "",
    tamaño_buffer: int = 10,
    entradaLength: int = 10,
) -> Tuple[List[str], str]:

    avance = 0  # posición del puntero de avance

    # Procesar y extraer lexemas del buffer
    lexemas = []
    lexema_actual = (
        lexema_incompleto  # esto va a hacer que no se corte al final de cada buffer
    )
    bufferCount + 1

    while avance < len(buffer):
        caracter = buffer[avance]
        avance += 1

        # ignorar espacios
        if caracter != " ":

            # Si encuentra un salto de linea tratarlo como un eol
            if caracter == "\n":
                lexema_actual += ""
                print(f"New Line")
            else:
                # agregar caracter al lexema actual
                lexema_actual += caracter
            # Si llega al final del archivo, guardar el ultimo lexema
            if avance + tamaño_buffer * bufferCount == entradaLength:
                print("lexema procesado: " + lexema_actual)
                lexemas.append(lexema_actual)

        # Al encontrar un espacio, mostrar el lexema guardado
        else:
            # Agregar a la lista de lexemas y reiniciar el lexema actual
            print("lexema procesado: " + lexema_actual)

            if lexema_actual == "eof":
                # si el lexema es eof, salir del ciclo
                return ([], "EOF")
            if lexema_actual == "eol":
                print(f"New Line")
            lexemas.append(lexema_actual)
            lexema_actual = ""

    if lexema_actual != "":
        lexemas.append(lexema_actual)
    return (
        lexemas,
        lexema_actual,
    )  # devolver los lexemas y el incompleto   # retornar la lista de lexemas procesados del buffer


entrada = list(leer_archivo("archivo.txt"))

# puntero de inicio
inicio = 0
tamano_buffer = 10
lexema_incompleto = ""
bufferCount = 0

while inicio <= len(entrada) + 1:
    buffer = cargar_buffer(entrada, inicio, tamano_buffer)
    lexemas, lexema_incompleto = procesar_buffer(
        bufferCount,
        buffer,
        lexema_incompleto,
        tamano_buffer,
        len(entrada),
    )
    bufferCount += 1

    if inicio >= len(entrada):
        print("--------------- You have reaced the end of file ---------------")
        break

    if lexemas == [] and lexema_incompleto == "EOF":
        print("--------------- You have reaced the end of file ---------------")
        break
    inicio += tamano_buffer  # avanzar el inicio del buffer para la próxima lectura