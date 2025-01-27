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
    buffer: List[str], lexema_incompleto: str = ""
) -> Tuple[List[str], str]:
    print("-------    buffer: " + str(buffer))

    avance = 0  # posición del puntero de avance

    # Procesar y extraer lexemas del buffer
    lexemas = []
    lexema_actual = (
        lexema_incompleto  # esto va a hacer que no se corte al final de cada buffer
    )

    while avance < len(buffer):
        caracter = buffer[avance]
        # print("caracter: " +caracter)
        avance += 1

        # ignorar espacios y si es eof
        if caracter != " " and caracter != "eof":
            # agregar caracter al lexema actual
            lexema_actual += caracter
        else:
            # si el lexema actual no está vacío, agregarlo a la lista de lexemas y reiniciar el lexema actual
            if lexema_actual != "":
                print("lexema procesado: " + lexema_actual)
                lexemas.append(lexema_actual)
                lexema_actual = ""
            # si el lexema es eof, salir del ciclo
            if caracter == "eof":
                # print("lexema procesado: eof")
                lexemas.append("eof")
                break

    if lexema_actual != "":
        lexemas.append(lexema_actual)
    return (
        lexemas,
        lexema_actual,
    )  # devolver los lexemas y el incompleto   # retornar la lista de lexemas procesados del buffer


# entrada = list("Esto es un ejemplo con entrada eof")
entrada = list(leer_archivo("archivo.txt"))
# entrada.append("eof")
# # entrada = leer_archivo("archivo.txt")

# puntero de inicio
inicio = 0
tamano_buffer = 10
lexema_incompleto = ""

while inicio < len(entrada):
    buffer = cargar_buffer(entrada, inicio, tamano_buffer)
    lexemas, lexema_incompleto = procesar_buffer(buffer, lexema_incompleto)
    # print("Lexemas:", lexemas)
    # inicio += len(buffer)
    # cerrar el while cuando sea eof
    if "eof" in buffer:
        break
    inicio += tamano_buffer  # avanzar el inicio del buffer para la próxima lectura
