import pickle

from Yalex.generator import LexicalAutomata
from typing import Dict, List

def get_pickle_automata():
    with open("./lexicalAutomata.pkl", "rb") as file:
        automata = pickle.load(file)
    return automata

def simular_texto(texto: str, automata: LexicalAutomata) -> List[List[str]]:
    resultados = []
    i = 0
    while i < len(texto):
        estado_actual = automata.afd.estado_inicial
        j = i
        ultimo_estado_final = None
        ultima_pos_final = i

        while j < len(texto):
            c = texto[j]
            transiciones = automata.afd.transiciones.get(estado_actual, {})

            if c == "+" or c == "(" or c == ")" or c == "*":
                c = "\\" + c
            if c in transiciones:
                estado_actual = transiciones[c]
                j += 1
                if estado_actual in automata.afd.estados_finales:
                    ultimo_estado_final = estado_actual
                    ultima_pos_final = j
            else:
                break

        if ultimo_estado_final is not None:
            lexema = texto[i:ultima_pos_final]
            token = automata.estado_a_token.get(ultimo_estado_final, "UNKNOWN")
            resultados.append([lexema, token])
            i = ultima_pos_final
        else:
            resultados.append([texto[i], "ERROR"])
            i += 1

    return resultados

def run():
    automata = get_pickle_automata()
