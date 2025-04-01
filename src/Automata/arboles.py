from Automata.Node import *

#arbol sintactico
#1. preparar stack vacio
#2. pricesar cada simbolo de la expresion postfix
#3. crear nosots para cada operando 
#4. continuar procesando hasta el final de cada expresion

#funciones del arbol sintactico
#anulable, primerapos, ultimapos, siguientepos

def tokenize_postfix(postfix: str) -> list:
    tokens = []
    i = 0
    while i < len(postfix):

        # if postfix[i] == "\\" and i + 1 < len(postfix) or postfix[i] == "\\\\" and i + 1 < len(postfix):
        #     tokens.append(postfix[i] + postfix[i + 1])
        #     i += 2

        #manejo de caracteres escapados
        if postfix[i] == "\\":
            if i + 1 < len(postfix):
                #caso 1: escapes comunes: \n, \t, \r, \v, \\
                if postfix[i + 1] in {"n", "t", "r", "v", "\\"}:
                    tokens.append(postfix[i] + postfix[i + 1])
                    i += 2
                    continue

                #caso 2: \+ o \- 
                if postfix[i + 1] == "\\" and i + 2 < len(postfix):
                    escaped_char = postfix[i + 2]
                    tokens.append("\\" + escaped_char)  #\+
                    i += 3
                    continue

                #cualquier otro tipo de escape
                tokens.append(postfix[i] + postfix[i + 1])
                i += 2
                continue



        # Manejo de literales entre comillas
        elif postfix[i] in {"'", '"', "`"}:
            # Si el literal empieza con una comilla, buscar el cierre
            # y agregarlo como un token completo
            quote_char = postfix[i]
            literal = postfix[i]
            i += 1
            while i < len(postfix):
                literal += postfix[i]
                if postfix[i] == quote_char:
                    break
                i += 1
            tokens.append(literal)
            i += 1
        else:
            tokens.append(postfix[i])
            i += 1
    return tokens


def construirArbolSintactico(postfix: str) -> Node:
    #1
    stack = []
    operators = {"|": 2, ".": 2, "*": 1, "+": 1, "?":1 , "#": 3, "^":5, "e":6, "ε":6}

    print('procesando la expresion postfix: ' + postfix)
    # 2
    tokens = tokenize_postfix(postfix)
    print(f"Tokens: {tokens}")
    print("POSTFIX:", postfix)

    for simbolo in tokens:
        
        print('procesando simbolo: ' + simbolo)

        # cuando es un operando, diagamos literales, escapados o comillas
        if simbolo not in operators:
            node = Node(simbolo)
            node.firstpos.add(node.id)
            node.lastpos.add(node.id)
            node.nullable = False
            stack.append(node)
            continue
            

        if simbolo == "#":
            node = Node(simbolo)
            node.firstpos.add(node.id)
            node.lastpos.add(node.id)
            node.nullable = False
            stack.append(node)
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
            continue

        if simbolo =="e" or simbolo == 'ε':
            node = Node(simbolo)
            node.nullable = True
            stack.append(node)
            continue

        #si se llega aca hay un simbolo no reconocido
        raise ValueError(f"simbolo no reconocido en postfix: {simbolo}")
    

    if len(stack) == 1:
        print('arbol sintactico construido correctamente')
        final_node = stack[0]
        print("Stack final:", len(stack))
        return final_node
    else:
        print(f'arbol sintactico construido incorrectamente, elementos en stack: {len(stack)}')
        for idx, node in enumerate(stack):
            print(f"Stack[{idx}]: {node.value}")
        if len(stack) > 1:
            print("Error: Quedaron múltiples nodos sin combinar en la pila.")
            print("Esto puede deberse a operadores binarios sin suficientes operandos.")
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
