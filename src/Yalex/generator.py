import pickle
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from collections import defaultdict
from typing import Dict, List
from dataclasses import dataclass
from Automata.arboles import construirArbolSintactico
from Automata.Regex import infixToPostfix
from Automata.AFD import AFD, construir_AFD
from Automata.Node import calcular_followPos
from Automata.graficadora import visualize_afd
import logging

# Configurar logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("afd_generation.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Carpeta de salida
OUTPUT_DIR = "./src/Yalex/generatorAFDS"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@dataclass
class LexicalAutomata:
    afd: AFD
    estado_a_token: Dict[int, str]


def generar_afd_unificado(tokens: Dict[str, str]) -> LexicalAutomata:
    expresiones = []
    posicion_a_token = {}
    token_map = {}

    # Generar expresiones con finalizador único (#idx)
    for idx, (nombre_token, expresion) in enumerate(tokens.items()):
        marcador = f"#{idx}"
        expresiones.append(f"({expresion}){marcador}")
        token_map[str(idx)] = nombre_token

    expresion_global = "|".join(expresiones)
    logger.info(f"Expresión global: {expresion_global}")

    postfix = infixToPostfix(expresion_global)
    logger.info(f"POSTFIX global: {postfix}")

    arbol = construirArbolSintactico(postfix)
    followpos = defaultdict(set)
    calcular_followPos(arbol, followpos)

    from Automata.AFD import mapear_posiciones_simbolos

    posicion_a_simbolo = {}
    mapear_posiciones_simbolos(arbol, posicion_a_simbolo)

    # Detectar la posición del símbolo '#' y vincularlo al token real
    for pos, simbolo in posicion_a_simbolo.items():
        if simbolo == "#":
            next_pos = pos + 1
            siguiente_simbolo = posicion_a_simbolo.get(next_pos + 1)
            if siguiente_simbolo and siguiente_simbolo in token_map:
                posicion_a_token[pos] = token_map[siguiente_simbolo]

    afd, estados_dict, estado_id_a_conjunto = construir_AFD(arbol, followpos)

    # Marcar estados finales con token
    estado_a_token = {}
    for estado_id, conjunto_pos in estado_id_a_conjunto.items():
        for pos in conjunto_pos:
            if pos in posicion_a_token:
                estado_a_token[estado_id] = posicion_a_token[pos]
                afd.agregar_estado_final(estado_id)

    afd.mostrar()
    visualize_afd(afd, output_dir=OUTPUT_DIR, file_name="AFD_Unificado")

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
    palabras = texto.split()
    for palabra in palabras:
        estado_actual = automata.afd.estado_inicial
        for c in palabra:
            if c in automata.afd.transiciones[estado_actual]:
                estado_actual = automata.afd.transiciones[estado_actual][c]
            else:
                estado_actual = None
                break

        if estado_actual in automata.afd.estados_finales:
            token = automata.estado_a_token.get(estado_actual, "UNKNOWN")
            resultados.append([palabra, token])
        else:
            resultados.append([palabra, "ERROR"])
    return resultados


# Ejemplo de tokens
tokens = {
    "cond": "if",
    "num": "(0|1|2|3|4|5|6|7|8|9)+",
}

lexical_automata = generar_afd_unificado(tokens)
_serialize_automata(lexical_automata, "lexical_out")

# Simular texto
test_input = "if 3 if 477"
resultado = simular_texto(test_input, lexical_automata)
print(resultado)
