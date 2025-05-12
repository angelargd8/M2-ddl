import pickle
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.constructor import leerArchivo

from collections import defaultdict
from typing import Dict, List
from dataclasses import dataclass
from Automata.arboles import construirArbolSintactico
from Automata.Regex import infixToPostfix
from Automata.AFD import AFD, construir_AFD
from Automata.Node import calcular_followPos
from Automata.graficadora import visualize_afd
from Automata.AFD import mapear_posiciones_simbolos

import logging

# Configurar logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("afd_generation.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Carpeta de salida
OUTPUT_DIR = "../src/Yalex/generatorAFDS"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@dataclass
class LexicalAutomata:
    afd: AFD
    estado_a_token: Dict[int, str]

def normalizar_expresion(expr: str) -> str:
    i = 0
    resultado = ""

    while i < len(expr):
        if expr[i] == "\\" and i + 1 < len(expr):
            siguiente = expr[i + 1]

            if siguiente == "n":
                resultado += "\n"
            elif siguiente == "t":
                resultado += "\t"
            elif siguiente == "s":
                resultado += " "
            else:
                # cualquier otro escape como \+ \* \( \)
                resultado += siguiente
            i += 2
        else:
            resultado += expr[i]
            i += 1

    return resultado

def generar_afd_unificado(tokens: Dict[str, str]) -> LexicalAutomata:
    expresiones = []
    posicion_a_token = {}
    token_map = {}

    # Generar expresiones con finalizador único usando @idx@
    for idx, (nombre_token, expresion) in enumerate(tokens.items()):
        #esto lo cambie por la funcion que esta arriba de normalizar expresion
        # expresion = expresion.replace("\\n", "\n")
        # expresion = expresion.replace("\\t", "\t")
        # expresion = expresion.replace("\\s", " ") #interpretando s como espacio

        expresion = normalizar_expresion(expresion)

        marcador = f"@{idx}@"
        expresiones.append(f"({expresion}){marcador}")

        token_map[str(idx)] = nombre_token


    expresion_global = "|".join(expresiones)
    logger.info(f"Expresión global: {expresion_global}")


    postfix = infixToPostfix(expresion_global)
    print("\n--- POSTFIX TOKENS ---")
    # for t in postfix:
    #     print(t)
    print(f"Postfix: {postfix}")

    logger.info(f"POSTFIX global: {postfix}")

    arbol = construirArbolSintactico(postfix)
    followpos = defaultdict(set)
    calcular_followPos(arbol, followpos)

    posicion_a_simbolo = {}
    mapear_posiciones_simbolos(arbol, posicion_a_simbolo)

    # Detectar fragmentos @idx@ en la secuencia de símbolos
    sorted_positions = sorted(posicion_a_simbolo.keys())
    i = 0
    while i < len(sorted_positions):
        pos = sorted_positions[i]
        simbolo = posicion_a_simbolo[pos]


        if simbolo == "@":
            num_str = ""
            j = i + 1
            while j < len(sorted_positions):
                next_pos = sorted_positions[j]
                next_char = posicion_a_simbolo[next_pos]
                if next_char.isdigit():
                    num_str += next_char
                    j += 1
                elif next_char == "@":
                    idx = num_str
                    if idx in token_map:
                        # Mapear el primer '@' a su token
                        posicion_a_token[pos] = token_map[idx]
                    i = j  # saltar al segundo '@'
                    break
                else:
                    break  # No es un marcador válido
        i += 1

    afd, estados_dict, estado_id_a_conjunto = construir_AFD(arbol, followpos)

    # Marcar estados finales con token
    estado_a_token = {}
    for estado_id, conjunto_pos in estado_id_a_conjunto.items():
        for pos in conjunto_pos:
            if pos in posicion_a_token:
                estado_a_token[estado_id] = posicion_a_token[pos]
                afd.agregar_estado_final(estado_id)

    # afd.mostrar()
    visualize_afd(afd, output_dir=OUTPUT_DIR, file_name="AFD_Unificado")

    print("\nSímbolos en transiciones del AFD:")
    for origen, trans in afd.transiciones.items():
        for simbolo in trans:
            print(f"  {origen} -- {repr(simbolo)} --> {trans[simbolo]}")

    # return LexicalAutomata(afd=afd, estado_a_token=estado_a_token)

    return LexicalAutomata(afd=afd, estado_a_token=estado_a_token)


def _serialize_automata(automata: LexicalAutomata, output_name: str):
    new_dir = os.path.join(OUTPUT_DIR, output_name)
    os.makedirs(new_dir, exist_ok=True)
    pickle_file_path = os.path.join(new_dir, "lexicalAutomata.pkl")
    with open(pickle_file_path, "wb") as f:
        pickle.dump(automata, f)
    logger.info(f"Automata serializado en {pickle_file_path}")


def simular_texto(texto: str, automata: LexicalAutomata) -> List[List[str]]:
    resultados = []
    i = 0
    while i < len(texto):
        estado_actual = automata.afd.estado_inicial
        j = i
        ultimo_estado_final = None
        ultima_pos_final = i
        token_encontrado = None

        while j < len(texto):
            c = texto[j]
            transiciones = automata.afd.transiciones.get(estado_actual, {})
            # if c in {"+", "*", "(", ")", ".", "\\", "?", "-", "[", "]", "{", "}", "^", "$"}:
            #     c = "\\" + c
            if c in transiciones:
                estado_actual = transiciones[c]
                j += 1
                if estado_actual in automata.afd.estados_finales:
                    ultimo_estado_final = estado_actual
                    ultima_pos_final = j
                    token_encontrado = automata.estado_a_token.get(estado_actual)
            else:
                break

        if ultimo_estado_final is not None:
            lexema = texto[i:ultima_pos_final]
            if token_encontrado != "WHITESPACE":
                resultados.append([lexema, token_encontrado])
            i = ultima_pos_final
        else:
            resultados.append([texto[i], "ERROR"])
            i += 1

    return resultados


ruta = "./Test.txt"

texto_prueba = leerArchivo(ruta)

if texto_prueba is None:
    print(f"Error al leer el archivo {ruta}. Asegúrate de que existe y es accesible.")
    sys.exit(1)

# "NUMBER": "((0|1|2|3|4|5|6|7|8|9)+)(.((ε|(0|1|2|3|4|5|6|7|8|9)+)))(E(ε|(\\+|-))((ε|(0|1|2|3|4|5|6|7|8|9)+)))",
# ((A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)|(0|1|2|3|4|5|6|7|8|9))*a
tokens = {
    "WHITESPACE": "( |\\t|\\n)+",
    # "ID": "([a-zA-Z])([a-zA-Z0-9_])*",
    "ID": "(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)((A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)|(0|1|2|3|4|5|6|7|8|9))*",
    # "NUMBER": "([0-9])+((\\.([0-9])+)?)(E((\\+|-)?([0-9])+))?",
    "NUMBER": "((0|1|2|3|4|5|6|7|8|9)+)(\\.((ε|(0|1|2|3|4|5|6|7|8|9)+)))(E(ε|(\\+|-))((ε|(0|1|2|3|4|5|6|7|8|9)+)))",
    "ASSIGNOP": ":=",
    "PLUS": "\\+",
    "MINUS": "-",
    "TIMES": "\\*",
    "DIV": "/",
    "LT": "<",
    "EQ": "=",
    "SEMICOLON": ";",
    "LPAREN": "\\(",
    "RPAREN": "\\)"
}

lexical_automata = generar_afd_unificado(tokens)
_serialize_automata(lexical_automata, "lexical_out")

print("\nContenido de Test.txt: \n")
print(texto_prueba)


resultado = simular_texto(texto_prueba, lexical_automata)
print(resultado)
