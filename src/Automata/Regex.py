from Automata.metachar import Metachar


# funcion para formatear la expresion regular para que se pueda trabajar con ella
def formatRegEx(regex):
    
    #eliminar los espacios en blanco
    regex = regex.replace(" ", "")

    #verificar que no es una expresion vacia
    if not regex: 
        return "e" #devuelbe epsilon para la expresion vacia

    stack_temp = []

    i = 0

    while i < len(regex):
        c1 = regex[i]

        #manejo de caracteres de escape
        if c1 == "\\" and i+1 < len(regex):
            stack_temp.append(c1 + regex[i+1])
            i += 2
            continue

        #manejo de operadores
        elif c1 == "?":
            if not stack_temp:
                raise ValueError("operador ?, sin operador previo en la posicion: " + str(i))
           
            t = stack_temp.pop() #obtener el ultimo valor ingresado

            #si es un parentesis tomar todo lo que esta dentro del parentesis
            if t[0] == ")":
                balanceador_i = 0 
                balanceador_d = 1
                while balanceador_i!= balanceador_d and stack_temp:

                    if not stack_temp:
                        raise ValueError("Parentesis no balanceados")
                    
                    top = stack_temp.pop()

                    if top == ")":
                        balanceador_d += 1
                    if top == "(":
                        balanceador_i += 1
                    t.append(top)
            t.reverse()
            t = "".join(t)
            stack_temp.append("(")
            stack_temp.append("e")
            stack_temp.append("|")
            stack_temp.append(t)
            stack_temp.append(")")

        #manejo del operador +
        elif c1 == "+":
            if not stack_temp:
                raise ValueError("operador +, sin operador previo en la posicion: " + str(i))
            t = stack_temp.pop()  # obtiene el ultimo valor ingresado

            #si no es un valor unico, si no algo que esta en parentesis se obtiene todo lo que esta en el parentesis
            if t[0] == ")":
                balanceador_i = 0
                balanceador_d = 1
                while balanceador_i!= balanceador_d and stack_temp:

                    if not stack_temp: #verificar si el stack esta vacio
                        raise ValueError("Parentesis no balanceados")

                    top = stack_temp.pop()
                    if top == ")":
                        balanceador_d += 1
                    if top == "(":
                        balanceador_i += 1
                    t.append(top)

            t.reverse()
            t = "".join(t)
            stack_temp.append(t)
            stack_temp.append(t)
            stack_temp.append("*")  # agrega el *
        else: 
            stack_temp.append(c1)

        i += 1

    regex = "".join(stack_temp)


    if regex and Metachar(regex[-1]).IsBinaryOperator():
        #agregar epsilon si termina con operador binario
        regex += "e"


    #agregar el operador de concatenacion

    result = ""

    for i in range(len(regex)):
        c1 = regex[i]
        result += c1

        if i + 1 < len(regex):
            c2 = regex[i + 1]
            #insertar '.' cuando sea necesario
            if (
                c1 != "(" and c2 != ")" and 
                c1 != "\\" and c1 != "|" and c2 != "|" and
                not Metachar(c2).IsOperator() and
                not Metachar(c1).IsBinaryOperator()
                ):

                result += "."

    return result



# fucncion para convertir una expresion regular de notacion infix a postfix
# aqui es donde se usa shunting yard
def infixToPostfix(regex):

    if not regex:
        return "e" #para el manejo de entrada vacia

    postfix = ""
    stack = []
    regex = formatRegEx(regex)
    print("\nExpresion formateada: \n" + regex)

    i = 0

    while i < (len(regex)):
        c = regex[i]
        #manejo del parentesis
        if c == "(":
            stack.append(c)
        elif c == ")":
            while stack and stack[-1] != "(":
                postfix += stack.pop()

            if not stack or stack[-1] != "(":
                raise ValueError("Parentesis no balanceados")
            
            stack.pop() # quitar el parentesis izquierdo

        #manejo de caracteres de escape

        elif c == "\\" and i + 1 < len(regex):
            postfix += "\\" + regex[i + 1]
            i += 1

        #manejo de operadores
        else:
            
            while stack: 
                peekedChar = stack[-1]

                if peekedChar == "(":
                    break

                peekedCharPrecedence = Metachar(peekedChar).getPrecedence(peekedChar)
                currentCharPrecedence = Metachar(c).getPrecedence(c)

                if peekedCharPrecedence >= currentCharPrecedence:
                    postfix += stack.pop()
                else:
                    break

            stack.append(c)
            
        i += 1

#vaciar los operadores restantes de la pila
    while stack:
        op = stack.pop()
        if op == "(":
            raise ValueError("Parentesis no balanceados")
        
        postfix += op

    #agregar el simbolo # (fin de la cadena) a la expresion postfix
    postfix += "#."
    return postfix
