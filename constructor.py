import os
from typing import List, Tuple, Union
from node import *
from collections import deque, defaultdict

# leer el archivo

"""
Al refactorizar el leer el archivo se uso IA, y se aplico 
Union[List[str], str] en vez de solo '-> str', como se tenia en el lab de buffer
ya que la IA, recomendo devolver Union[List[str], str] 
para indicar que puede devolver una lista de cadenas o un mensaje de error
"""


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


# esto era para el afn
def construirArbol(e):
    stack = []
    operators = {"|": 2, ".": 2, "*": 1, "+": 1}

    for c in e:
        if c not in operators:
            node = Node(c)
            stack.append(node)
        else:
            if operators[c] == 2:
                right_operand = stack.pop()
                try:
                    left_operand = stack.pop()
                except IndexError:
                    node = Node(c)
                    node.left = None
                    node.right = right_operand
                    stack.append(node)
                    continue

                node = Node(c)
                node.right = right_operand
                node.left = left_operand
                stack.append(node)

            else:
                operand = stack.pop()
                node = Node(c)
                node.left = operand
                node.right = None
                stack.append(node)

    return stack.pop()


def construirArbolSintactico(e):
    stack = []
    operators = {"|": 2, ".": 2, "*": 1, "+": 1, "#": 3}
    
    print("\nProcesando expresión:", e)
    
    for i, c in enumerate(e):
        # print(f"Procesando: {c}")
        # print("Stack actual:", [n.value for n in stack])
        
        if c not in operators:
            node = Node(c)
            node.firstpos.add(node.id)
            node.lastpos.add(node.id)
            node.nullable = False
            stack.append(node)
            continue

        if c == "#":
            if not stack:
                raise ValueError(f"expresion postfix invalida: {e}")
                
            prev_node = stack.pop()
            node = Node(c)
            node.nullable = False
            node.firstpos = prev_node.firstpos
            node.lastpos = prev_node.lastpos
            node.left = prev_node
            node.right = None  # Aseguramos que right es None
            stack.append(node)
            continue

        if c in ["|", "."]:
            if len(stack) < 2:
                raise ValueError(f"expresion postfix invalida: {e}")

            right = stack.pop()
            left = stack.pop()
            node = Node(c)
            node.right = right
            node.left = left
            
            if c == "|":
                node.nullable = left.nullable or right.nullable
                node.firstpos = left.firstpos.union(right.firstpos)
                node.lastpos = left.lastpos.union(right.lastpos)
            elif c == ".":
                node.nullable = left.nullable and right.nullable
                node.firstpos = left.firstpos if not left.nullable else left.firstpos.union(right.firstpos)
                node.lastpos = right.lastpos if not right.nullable else right.lastpos.union(left.lastpos)
            
            stack.append(node)
            continue

        if c in ["*", "+"]:
            if not stack:
                raise ValueError(f"expresion postfix invalida: {e}")

            operand = stack.pop()
            node = Node(c)
            node.left = operand
            node.right = None  # Aseguramos que right es None
            node.nullable = True if c == "*" else operand.nullable
            node.firstpos = operand.firstpos
            node.lastpos = operand.lastpos
            stack.append(node)

    if len(stack) != 1:
        raise ValueError(f"expresion postfix invalida: {e}")
        
    final_node = stack[0]
    
    # Validación final
    if final_node.value != "#":
        raise ValueError(f"El nodo raíz debe ser '#', pero es '{final_node.value}'")
    
    return final_node