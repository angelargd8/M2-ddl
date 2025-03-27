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
    """Genera un AFD unificado a partir de múltiples tokens."""
    expresiones = []
    for nombre_token, expresion in tokens.items():
        expresiones.append(f"({expresion})#{nombre_token}")

    expresion_global = "|".join(expresiones)
    logger.info(f"Expresión global: {expresion_global}")

    postfix = infixToPostfix(expresion_global)
    logger.info(f"POSTFIX global: {postfix}")

    arbol = construirArbolSintactico(postfix)
    followpos = defaultdict(set)
    calcular_followPos(arbol, followpos)

    afd = construir_AFD(arbol, followpos)

    estado_a_token = {}
    for estado in afd.estados_finales:
        for trans in afd.transiciones.get(estado, {}).items():
            simbolo = trans[0]
            if isinstance(simbolo, str) and simbolo.startswith("#"):
                estado_a_token[estado] = simbolo[1:]

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
