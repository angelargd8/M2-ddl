from Automata.Node import *


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
    operators = {"|": 2, ".": 2, "*": 1, "+": 1, "?":1 , "#": 3, "^":5, "e":6, "ε":6}

    print('procesando la expresion postfix: ' + postfix)

    # 2
    i = 0 

    while i < len(postfix): 
        simbolo = postfix[i]
        print('procesando simbolo: ' + simbolo)

        #manejar literales entre comillas
        if simbolo in {"'", '"'}:
            quote_char = simbolo
            literal = simbolo
            i += 1
            while i < len(postfix):
                literal += postfix[i]
                if postfix[i] == quote_char:
                    break
                i += 1
            node = Node(literal)
            node.firstpos.add(node.id)
            node.lastpos.add(node.id)
            node.nullable = False
            stack.append(node)
            i += 1
            continue

        #manejar simbolos escapados
        if simbolo == "\\" and i + 1 < len(postfix):
            #tratar el simbolo escapado como una unidad
            simbolo_escapado = simbolo + postfix[i + 1]
            print(f"Encontrado símbolo escapado: {repr(simbolo_escapado)}")
            node = Node(simbolo_escapado)
            node.firstpos.add(node.id)
            node.lastpos.add(node.id)
            node.nullable = False
            stack.append(node)
            i +=2
            continue

        #operando (valor o variable)
        if simbolo not in operators:
            # 3
            node = Node(simbolo)
            node.firstpos.add(node.id)
            node.lastpos.add(node.id)
            node.nullable = False
            stack.append(node)
            i += 1
            continue
            

        if simbolo == "#":
            node = Node(simbolo)
            node.firstpos.add(node.id)
            node.lastpos.add(node.id)
            node.nullable = False
            stack.append(node)
            i += 1
            continue


        if simbolo in ["*", "+",  "?"]:

            #verificar si hay operandos disponibles
            if not stack:
                raise ValueError(f"expresion postfix invalida: {postfix}")

            node = Node(simbolo)
            node.left = stack.pop()
            node.right = None
            

            if simbolo == "*" or simbolo == "?":        # '*' y '?' permiten 0 ocurrencias, por eso son anulables
                node.nullable = True
            else:  
                node.nullable = node.left.nullable

            node.firstpos = node.left.firstpos.copy()
            node.lastpos = node.left.lastpos.copy()

            stack.append(node)
            i += 1
            continue

        if simbolo in [".", "|"]:
            if len(stack) < 2:
                raise ValueError(f"expresion postfix invalida: {postfix}")
            
            node =Node(simbolo)
            node.right = stack.pop()
            node.left = stack.pop()
            node.nullable = node.left.nullable and node.right.nullable
            
            if simbolo == ".":

                if node.left.nullable:
                    node.firstpos = node.left.firstpos.union(node.right.firstpos)
                else:
                    node.firstpos = node.left.firstpos.copy()


                if node.right.nullable:
                    node.lastpos = node.right.lastpos.union(node.left.lastpos)
                else:
                    node.lastpos = node.right.lastpos.copy()


            if simbolo == "|":
                node.firstpos = node.left.firstpos.union(node.right.firstpos)
                node.lastpos = node.right.lastpos.union(node.left.lastpos)
                node.nullable = node.left.nullable or node.right.nullable

            stack.append(node)
            i += 1
            continue

        if simbolo =="^":
            if len(stack) < 1:
                raise ValueError(f"expresion postfix invalida: {postfix}")
            
            node = Node(simbolo)
            node.left = stack.pop()
            node.right = None
            node.nullable = False
            #cuando son de anclaje no cambian los firstpos y lastpos
            node.firstpos = node.left.firstpos.copy()
            node.lastpos = node.left.lastpos.copy()

            stack.append(node)
            i += 1
            continue

        if simbolo =="e" or simbolo == 'ε':
            node = Node(simbolo)
            node.nullable = True
            stack.append(node)
            i += 1
            continue

        #si se llega aca hay un simbolo no reconocido
        raise ValueError(f"simbolo no reconocido en postfix: {simbolo}")
    

    if len(stack) == 1:
        print('arbol sintactico construido correctamente')
        final_node = stack[0]
        return final_node
    else:
        print(f'arbol sintactico construido incorrectamente, elementos en stack: {len(stack)}')
        for idx, node in enumerate(stack):
            print(f"Stack[{idx}]: {node.value}")
        return None
        




"""
esta funcion fue sacada con algo de ayuda de chat porque no salian bien las sangria sjakjsd
"""
def imprimirArbolSintactico(nodo: Node, sangria: str = "", es_ultimo: bool = True):    
    # nodo actual con sangria
    if sangria:
        if es_ultimo:
            print(sangria + "└─ " + str(nodo.displayValue()) + " (" + str(nodo.nullable) +  ") " )# + str(nodo.firstpos))
            sangria_nueva = sangria + "   "
        else:
            print(sangria + "├─ " + str(nodo.displayValue()) + " (" + str(nodo.nullable) +   ") " )# + str(nodo.firstpos) )
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
