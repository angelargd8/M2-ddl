from Automata.constructor import leerArchivo
from Automata.arboles import construirArbolSintactico, imprimirArbolSintactico
from Automata.Regex import infixToPostfix
from Automata.AFD import *
from Automata.Node import *
from collections import defaultdict
from Automata.graficadora import visualize_afd
from Yalex.yalReader import yalReader
from Yalex.generator import generar_afd_unificado, simular_texto, _serialize_automata
import os


def leerArchivo(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return archivo.read()
    except Exception as e:
        print(f"Error al leer {ruta}: {e}")
        return None


def guardar_resultado_en_txt(resultados, archivo_salida):
    os.makedirs(os.path.dirname(archivo_salida), exist_ok=True)
    with open(archivo_salida, "w", encoding="utf-8") as f:
        for palabra, token in resultados:
            f.write(f"{palabra} -> {token}\n")


archivos = ["slr-4.yal"]  # Lista de archivos YAL

for archivo_yal in archivos:
    ruta = os.path.join("yalDocs", archivo_yal)
    contenido_yal = leerArchivo(ruta)

    if contenido_yal:
        print(f"\nArchivo {archivo_yal} leído correctamente\n")

        yal = yalReader(contenido_yal)
        tokens = yal.get_tokens()

        print("Tokens detectados:")
        for nombre, expr in tokens.items():
            print(f"  {nombre}: {expr}")

        automata_lexico = generar_afd_unificado(tokens)
        _serialize_automata(automata_lexico, "lexical_out")

        texto_prueba = leerArchivo("Yalex/Test.txt")
        if texto_prueba:
            print("\nContenido de Test.txt:")
            print(texto_prueba)

            resultados = simular_texto(texto_prueba, automata_lexico)

            print("\nResultados de la simulación:")
            for palabra, token in resultados:
                print(f"{palabra} -> {token}")

            guardar_resultado_en_txt(resultados, "Yalex/Out/TokensRead.txt")
            print("\nResultados guardados en Yalex/Out/TokensRead.txt")
