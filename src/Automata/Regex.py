from Automata.metachar import Metachar


def agregarConcatenacion(tokens: list[str]) -> list[str]:
    resultado = []

    for i in range(len(tokens) - 1):
        actual = tokens[i]
        siguiente = tokens[i + 1]
        resultado.append(actual)

        # Evitar concatenacion en casos especificos
        if (
            actual in ["(", "|"]
            or siguiente in [")", "|"]
            or actual in ["ε", "#"]
            or siguiente in ["ε", "#"]
            or actual == "."
            or siguiente == "."
            or (actual == "*" and siguiente == "ε")
            or (actual == "ε" and siguiente in ["|", ".", ")"])
            or (actual == "|" and siguiente == "ε")
            or (actual.startswith("\\") and actual not in ["\\+", "\\-"])
            or (siguiente.startswith("\\") and siguiente not in ["\\+", "\\-"])
        ):
            continue

        es_actual_valido = not Metachar.IsOperator(actual) or actual in [
            ")",
            "*",
            "+",
            "?",
        ]
        es_siguiente_valido = (
            not Metachar.IsOperator(siguiente)
            or siguiente == "("
            or siguiente.startswith("\\")
        )

        if es_actual_valido and es_siguiente_valido:
            resultado.append(".")

    resultado.append(tokens[-1])
    return resultado


# funcion para formatear la expresion regular para que se pueda trabajar con ella
def formatRegEx(regex: str) -> list[str]:
    # verificar que no es una expresion vacia
    if not regex:
        return ["ε"]  # devuelbe epsilon para la expresion vacia

    # si regex empieza con un operador binario, agregar episolon al inicio
    if Metachar.IsBinaryOperator(regex[0]):
        regex = "ε" + regex

    regex_list = list(regex)
    i = 0
    tokens = []

    def find_matching_open(lista, indice_cierre):
        conteo = 1
        k = indice_cierre - 1
        while k >= 0 and conteo > 0:
            if lista[k] == ")":
                conteo += 1
            elif lista[k] == "(":
                conteo -= 1
            k -= 1
        return k + 1

    def find_element_start(lista, pos):
        if lista[pos] == ")":
            return find_matching_open(lista, pos)
        if lista[pos] in ["*", "+", "?"]:
            return find_element_start(lista, pos - 1)
        return pos

    while i < len(regex_list):
        # manejo de comillas
        if Metachar.IsQuoted(regex_list[i]):
            quote_char = regex_list[i]
            literal = regex_list[i]
            i += 1
            while i < len(regex_list):
                literal += regex_list[i]
                if regex_list[i] == quote_char:
                    i += 1
                    break
                i += 1
            tokens.append(literal)  # agregar el literal completo como un solo token

        # manejo de caracteres de escape
        elif regex_list[i] == "\\":
            if i + 1 < len(regex_list):
                escape = regex_list[i] + regex_list[i + 1]
                tokens.append(escape)
                i += 2
            else:
                # agregar el \, de forma normal
                tokens.append("\\")
                i += 1

        # manejo de operadores
        elif regex_list[i] == "?":
            if tokens and not tokens[-1].startswith("\\"):
                fin = len(tokens) - 1
                ini = find_element_start(tokens, fin)
                operando = tokens[ini : fin + 1]
                tokens = tokens[:ini] + ["("] + operando + ["|", "ε", ")"]
                i += 1
            else:
                tokens.append("?")
                i += 1

        # manejo del operador +
        elif regex_list[i] == "+":
            if tokens and not tokens[-1].startswith("\\"):
                fin = len(tokens) - 1
                ini = find_element_start(tokens, fin)
                operando = tokens[ini : fin + 1]
                # tokens = tokens[:ini] + operando + ['.'] + operando + ['*']
                tokens = tokens[:ini] + ["("] + operando + ["."] + operando + ["*", ")"]
                i += 1
            else:
                tokens.append("+")
                i += 1

        else:
            tokens.append(regex_list[i])
            i += 1

    final = agregarConcatenacion(tokens)
    return final


# fucncion para convertir una expresion regular de notacion infix a postfix
# aqui es donde se usa shunting yard
def infixToPostfix(regex: str) -> str:
    if not regex:
        return "ε#."  # para el manejo de entrada vacía

    # Formatear la expresión regular
    tokens = formatRegEx(regex)
    print("Expresion formateada: \n" + regex)

    salida = ""
    stack = []

    for simbolo in tokens:
        # if simbolo == ' ':
        #     continue

        if simbolo.startswith("\\") and len(simbolo) == 2:
            salida += simbolo
            continue

        if simbolo == "(":
            stack.append(simbolo)

        elif simbolo == ")":
            while stack and stack[-1] != "(":
                salida += stack.pop()

            if stack and stack[-1] == "(":
                stack.pop()

        elif simbolo in ["*", "?"]:
            salida += simbolo

        elif Metachar.IsOperator(simbolo):

            while (
                stack
                and stack[-1] != "("
                and Metachar.IsOperator(stack[-1])
                and Metachar.getPrecedence(stack[-1]) >= Metachar.getPrecedence(simbolo)
            ):
                if stack[-1] == "." and salida and salida[-1] == ".":
                    # Evitar agregar un segundo punto
                    stack.pop()
                    continue
                salida += stack.pop()

            stack.append(simbolo)
        else:
            salida += simbolo

    while stack:
        salida += stack.pop()

    # reemplazar puntos consecutivos si existieran
    while ".." in salida:
        salida = salida.replace("..", ".")

    # # asegurar que hay un punto antes de #
    # if not salida.endswith('.'):
    #     salida += '.'
    # if not salida.endswith('#'):
    #     salida += '#'
    # if not salida.endswith('.'):
    #     salida += '.'

    salida += "#."  # --

    if not salida.endswith("#.") and not salida.endswith(".#."):  # --
        salida += "#."

    # if salida.endswith('.#.'):
    #     salida = salida[:-1]
    # elif not salida.endswith('#.'):
    #     salida += '#.'

    # if not salida.endswith('.'):
    #     salida += '.'
    # salida += '#.'

    print("postfix: \n" + salida)
    return salida
