import os
from typing import List, Tuple, Union
from node import *
from collections import deque, defaultdict

# leer el archivo

'''
Al refactorizar el leer el archivo se uso IA, y se aplico 
Union[List[str], str] en vez de solo '-> str', como se tenia en el lab de buffer
ya que la IA, recomendo devolver Union[List[str], str] 
para indicar que puede devolver una lista de cadenas o un mensaje de error
'''

def leerArchivo(file: str) ->  Union[List[str], str]:
    try:
        script_dir = os.path.dirname(__file__)  # Directorio del script actual
        file_path = os.path.join(script_dir, file)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            expresiones = f.read().split('\n')
        
        print(expresiones, type(expresiones))
        return expresiones
    except FileNotFoundError:
        return "El archivo no fue encontrado"
    except IOError:
        return "Error al leer el archivo"
    
#esto era para el afn
def construirArbol(e):
    stack = []
    operators = {'|':2 , '.':2, '*':1, '+':1}

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
    operators = {'|':2 , '.':2, '*':1, '+':1}

    for c in e:
        if c not in operators:
            node = Node(c)
            
            node.firstpos.add(node.id)
            node.lastpos.add(node.id)
            node.nullable = False

            stack.append(node)

        else:
            if operators[c] == 2:
                if len(stack) < 2:
                    raise ValueError(f"expresion postfix invalida: {e}")
                
                right_operand = stack.pop() 
                left_operand = stack.pop()
                node = Node(c)
                node.left = left_operand
                node.right = right_operand

                if c == '|':
                    node.nullable = left_operand.nullable or right_operand.nullable
                    node.firstpos = left_operand.firstpos.union(right_operand.firstpos)
                    node.lastpos = left_operand.lastpos.union(right_operand.lastpos)
                    # print('node |')
                    # print(node)
                elif c == '.':
                    node.nullable = left_operand.nullable and right_operand.nullable
                    if left_operand.nullable:
                        node.firstpos = left_operand.firstpos.union(right_operand.firstpos)
                    else:
                        node.firstpos = left_operand.firstpos
                    
                    if right_operand.nullable:
                        node.lastpos = right_operand.lastpos.union(left_operand.lastpos)
                    else:
                        node.lastpos = right_operand.lastpos

                    # print('node .')
                    # print(node)

                stack.append(node)
            else:
                if not stack:
                    raise ValueError(f"expresion postfix invalida: {e}")
                
                operand = stack.pop()
                node = Node(c)
                node.left = operand

                if c == '*':
                    node.nullable = True #aqui es true porque como se puede repetir 0 o mas veces, siemrpe es nullable
                    node.firstpos = operand.firstpos
                    node.lastpos = operand.lastpos
                    # print('node *')
                    # print(node)

                if c == '+':
                    node.nullable = operand.nullable #este solo puede ser nullable solo si la expresion se tiene que repetir una o mas veces
                    node.firstpos = operand.firstpos
                    node.lastpos = operand.lastpos
                    # print('node +')
                    # print(node)

                stack.append(node)       
    if len(stack) != 1:
        raise ValueError(f"expresion postfix invalida: {e}")    

    # print(stack)
    return stack.pop()

