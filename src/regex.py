from Metachar import Metachar


# funcion para formatear la expresion regular para que se pueda trabajar con ella
def formatRegEx(regex):
    res = ""
    regex = regex.replace(" ", "")

    stack_temp = []

    for i in range(0, len(regex)):
        c1 = regex[i]
        if c1 == "?":  # quitar el ? si encuentra uno
            t = [stack_temp.pop()]  # obtiene el ultimo valor ingresado
            if (
                t[0] == ")"
            ):  # si no es un valor unico, si no algo que esta en parentesis se obtiene todo lo que esta en el parentesis
                balanceador_i = 0
                balanceador_d = 1
                while balanceador_i != balanceador_d:
                    if stack_temp[-1] == ")":
                        balanceador_d += 1
                    if stack_temp[-1] == "(":
                        balanceador_i += 1
                    t.append(stack_temp.pop())
            t.reverse()
            t = "".join(t)
            stack_temp.append("(")
            stack_temp.append("e")
            stack_temp.append("|")
            stack_temp.append(t)
            stack_temp.append(")")
        elif c1 == "+":
            t = [stack_temp.pop()]  # quita el +
            if (
                t[0] == ")"
            ):  # si no es un valor unico, si no algo que esta en parentesis se obtiene todo lo que esta en el parentesis
                balanceador_i = 0
                balanceador_d = 1
                while balanceador_i != balanceador_d:
                    if stack_temp[-1] == ")":
                        balanceador_d += 1
                    if stack_temp[-1] == "(":
                        balanceador_i += 1
                    t.append(stack_temp.pop())
                t.reverse()
                t = "".join(t)
                stack_temp.append(t)
                stack_temp.append(t)
                stack_temp.append("*")  # agrega el *
            else:
                t = "".join(t)
                stack_temp.append(t)
                stack_temp.append(t)
                stack_temp.append("*")  # agregar el *

        else:
            stack_temp.append(c1)

    regex = "".join(stack_temp)

    for i in range(0, len(regex)):
        c1 = regex[i]
        if i + 1 < len(regex):  # verifica que se haga hasta los ultimos 2
            c2 = regex[i + 1]
            res += c1
            if (
                c1 != "("
                and c2 != ")"
                and c1 != "\\"
                and not Metachar(c2).IsOperator()
                and not Metachar(c1).IsBinaryOperator()
            ):
                res += "."

    return res if len(regex) == 1 else res + regex[-1]


# fucncion para convertir una expresion regular de notacion infix a postfix
# aqui es donde se usa shunting yard
def infixToPostfix(regex):
    postfix = ""
    stack = []
    regex = formatRegEx(regex)
    print("\nExpresion formateada: \n" + regex)

    i = 0

    while i < (len(regex)):
        c = regex[i]
        if c == "(":
            stack.append(c)
        elif c == ")":
            while stack[-1] != "(":
                postfix += stack.pop()
            stack.pop()

        else:
            if c == "\\":
                postfix += "\\" + regex[i + 1]
                i += 1
            while len(stack) > 0:
                peekedChar = stack[-1]
                peekedCharPrecedence = Metachar(peekedChar).getPrecedence(peekedChar)
                currentCharPrecedence = Metachar(c).getPrecedence(c)

                if peekedCharPrecedence >= currentCharPrecedence:
                    # concatenate stack.pop() to postfix
                    postfix += stack.pop()
                else:
                    break
            if c != "\\":
                stack.append(c)
        i += 1
    while len(stack) > 0:
        postfix += stack.pop()

    postfix += "#"
    return postfix
