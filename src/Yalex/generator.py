import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from collections import defaultdict
from Automata.arboles import construirArbolSintactico
from Automata.Regex import infixToPostfix
from Automata.AFD import construir_AFD
from Automata.Node import calcular_followPos
from Automata.graficadora import visualize_afd
from Automata.AFN import Afn
import logging

# Configurar logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("afd_generation.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Carpeta para almacenar los AFDs generados
OUTPUT_DIR = "generatorAFDS"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


def generar_afds(tokens):
    """
    Genera un AFD para cada expresión regular en el diccionario tokens y los grafica.
    """
    afds = {}

    for nombre_token, expresion in tokens.items():
        logger.info(f"Generando AFD para el token: {nombre_token}")

        # Convertir la expresión a notación postfix
        postfix = infixToPostfix(expresion)
        logger.info(f"Expresión POSTFIX para {nombre_token}: {postfix}")

        # Construir el árbol sintáctico
        arbolSintactico = construirArbolSintactico(postfix)
        if not arbolSintactico:
            logger.error(f"Error al construir el árbol sintáctico para {nombre_token}")
            continue

        # Calcular followpos
        followpos = defaultdict(set)
        calcular_followPos(arbolSintactico, followpos)

        # Construir el AFD
        afd = construir_AFD(arbolSintactico, followpos)
        afds[nombre_token] = afd

        # Graficar el AFD en la carpeta generatorAFDS
        visualize_afd(afd, output_dir=OUTPUT_DIR, file_name=f"AFD_{nombre_token}")
        logger.info(f"Imagen del AFD generada en {OUTPUT_DIR}/AFD_{nombre_token}.png")

    return afds


def construir_afn_desde_afds(afds):
    """
    Construye un AFN con transiciones épsilon hacia cada AFD generado.
    """
    afn = Afn()

    estado_inicial = afn.crearNodo()
    afn.inicio = estado_inicial

    for nombre_token, afd in afds.items():
        nodo_afn = afn.crearNodo()
        estado_inicial.hijos.append(("ε", nodo_afn))
        nodo_afn.hijos.append(("ε", afd.estado_inicial))

        for estado_final in afd.estados_finales:
            estado_final.hijos.append(("ε", afn.final))

    return afn


def analizar_texto_con_afn(afn, texto):
    """
    Analiza un texto de entrada y devuelve los tokens reconocidos con sus valores.
    """
    tokens_identificados = []
    i = 0
    while i < len(texto):
        estado_actual = afn.inicio
        token_actual = ""
        mejor_token = None
        mejor_match = ""

        for j in range(i, len(texto)):
            token_actual += texto[j]

            for transicion, siguiente_estado in estado_actual.hijos:
                if transicion == "ε" or (
                    token_actual and token_actual[-1] == transicion
                ):
                    estado_actual = siguiente_estado

                    if estado_actual in afn.final:
                        mejor_token = estado_actual
                        mejor_match = token_actual

        if mejor_token:
            tokens_identificados.append((mejor_token.nombre, mejor_match))
            i += len(mejor_match)
        else:
            i += 1  # Avanzar en caso de no encontrar coincidencia

    return tokens_identificados


tokens = {
    "id": "(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)((A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|0|1|2|3|4|5|6|7|8|9))*",
    "cond": "if",
    "num": "(0|1|2|3|4|5|6|7|8|9)+",
}
construir_afn_desde_afds(generar_afds(tokens=tokens))
