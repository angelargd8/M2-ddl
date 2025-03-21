from src.node import *


#arbol sintactico
#1. preparar stack vacio
#2. pricesar cada simbolo de la expresion postfix
#3. crear nosots para cada operando 
#4. continuar procesando hasta el final de cada expresion

#funciones del arbol sintactico
#anulable, primerapos, ultimapos, siguientepos


def construirArbolSintactico(postfix: str) -> Node:
    #1
    stack = []
    operators = {"|": 2, ".": 2, "*": 1, "+": 1, "#": 3, "^":5}

    print('procesando la expresion postfix: ' + postfix)

    # 2
    for i, simbolo in enumerate(postfix):
        print('procesando simbolo: ' + simbolo)

        #operando (valor o variable)
        if simbolo not in operators:
            # 3
            node = Node(simbolo)
            node.firstpos.add(node.id)
            node.lastpos.add(node.id)
            node.nullable = False
            stack.append(node)
            # print('variable')
            # print(node.__str__())
            continue
            

        if simbolo == "#":
            if not stack:
                raise ValueError(f"expresion postfix invalida: {postfix}")

            node = Node(simbolo)
            node.firstpos.add(i+1)
            node.lastpos.add(i+1)
            node.nullable = False
            # print('node para #')
            # print(node.__str__())

            node_punto = stack.pop()
            node_punto.right = node
            stack.append(node_punto)
            continue


        if simbolo in ["*", "+"]:
            node = Node(simbolo)

            node.left = stack.pop()
            node.right = None
            node.firstpos = node.left.firstpos
            node.lastpos = node.left.lastpos
            node.nullable = True if simbolo == "*" else False
            # print('node para + o *')
            # print(node.__str__())
            stack.append(node)
            continue

        if simbolo in [".", "|"]:
            if len(stack) < 2:
                raise ValueError(f"expresion postfix invalida: {postfix}")
            
            node =Node(simbolo)
            node.right = stack.pop()
            node.left = stack.pop()
            node.nullable = node.left.nullable and node.right.nullable
            
            if simbolo == ".":
                node.firstpos = node.left.firstpos if node.left.nullable else node.left.firstpos.union(node.right.firstpos)
                node.lastpos = node.right.lastpos if node.right.nullable else node.right.lastpos.union(node.left.lastpos)
                # print('node para .')
                # print(node.__str__())

            if simbolo == "|":
                node.firstpos = node.left.firstpos.union(node.right.firstpos)
                node.lastpos = node.right.lastpos.union(node.left.lastpos)
                # print('node para |')
                # print(node.__str__())

            stack.append(node)
            continue

        if simbolo =="^":
            if len(stack) < 1:
                raise ValueError(f"expresion postfix invalida: {postfix}")
            
            node = Node(simbolo)
            node.left = stack.pop()
            node.right = None
            node.nullable = False
            #cuando son de anclaje no cambian los firstpos y lastpos
            node.firstpos = node.left.firstpos
            node.lastpos = node.left.lastpos

            stack.append(node)
            continue

    
    # print('stack:')
    # for i in stack:
    #     print(i.__str__())

    if len(stack) == 1:
        print('arbol sintactico construido correctamente')
        final_node = stack[0]
        return final_node
    else:
        print('arbol sintactico construido incorrectamente')
        return None
        




"""
esta funcion fue sacada con algo de ayuda de chat porque no salian bien las sangria sjakjsd
"""
def imprimirArbolSintactico(nodo: Node, sangria: str = "", es_ultimo: bool = True):    
    # nodo actual con sangria
    if sangria:
        if es_ultimo:
            print(sangria + "└─ " + str(nodo.value))
            sangria_nueva = sangria + "   "
        else:
            print(sangria + "├─ " + str(nodo.value))
            sangria_nueva = sangria + "│  "
    else:
        print(str(nodo.__str__()))
        sangria_nueva = "   "  # sangria para los hijos del nodo raiz

    # hijos recursivos
    if nodo.left:
        imprimirArbolSintactico(nodo.left, sangria_nueva, nodo.right is None)
    if nodo.right:
        imprimirArbolSintactico(nodo.right, sangria_nueva, True)



#esta parte es el arbol que ya teníamos en TC
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
