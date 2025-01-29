import os
from typing import List, Tuple


# leer el archivo
def leer_archivo(archivo: str) -> str:
    return open("../M2-ddl/" + archivo, "r").read()


# Código base para iniciar
def cargar_buffer(entrada: List[str], inicio: int, tamano_buffer: int) -> List[str]:
    buffer = entrada[inicio : inicio + tamano_buffer]
    return buffer


def eol_handler(lexemas: list, lexema_actual: str):
    print("New Line")
    return


def eof_handler():
    print("--------------- You have reaced the end of file ---------------")
    return


def add_lexema(lexema_actual: str, lexemas: list[str]):
    lexemas.append(lexema_actual)


def add_caracter(caracter: str, lexema_actual: str, is_final: bool):
    lexema_actual += caracter
    if is_final:
        eof_handler()


def buffer_handler(buffer_size: int, file_path: str):
    buffer_count = 0
    entrada = leer_archivo(file_path)
    lexemas = []
    lexema_incompleto = ""
    lexema_actual = lexema_incompleto

    for i in range(len(entrada)):
        buffer_count += 1
        buffer = cargar_buffer(entrada, i, buffer_size)

        for j in range(len(buffer)):
            pointer = buffer[j]
            is_final = j + buffer_size * buffer_count == len(entrada)

            match pointer:
                case "\n":
                    eol_handler(lexema_actual=lexema_actual, lexemas=lexemas)
                case _:
                    add_caracter(
                        caracter=pointer, lexema_actual=lexema_actual, is_final=is_final
                    )

        pass
