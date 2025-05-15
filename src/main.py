import sys

from constructor import leerArchivo, guardar_resultado_en_txt
from Automata.arboles import construirArbolSintactico, imprimirArbolSintactico
from Automata.Regex import infixToPostfix
from Automata.AFD import *
from Automata.Node import *
from collections import defaultdict
from Automata.graficadora import visualize_afd
from Yalex.yalReader import yalReader
from Yalex.generator import generar_afd_unificado, simular_texto, _serialize_automata
import os


archivos = ["slr-4.yal"]  # Lista de archivos YAL

for archivo_yal in archivos:
    ruta = os.path.join("./Yalex/yalDocs/", archivo_yal)
    contenido_yal = leerArchivo(ruta)

    if contenido_yal:
        print(f"\nArchivo {archivo_yal} leído correctamente\n")

        yal = yalReader(contenido_yal)
        tokens = yal.get_tokens()
        texto_prueba = leerArchivo("./Test.txt")

        print("Tokens detectados:")
        for nombre, expr in tokens.items():
            print(f"  {nombre}: {expr}")


        if texto_prueba is None:
            print(f"Error al leer el archivo {ruta}. Asegúrate de que existe y es accesible.")
            sys.exit(1)

        lexical_automata = generar_afd_unificado(tokens)
        _serialize_automata(lexical_automata, "lexical_out")


        print("\n--- SIMULANDO texto ---")
        resultado = simular_texto(texto_prueba, lexical_automata)
        ruta_salida = "./out/resultado.txt"  # Puedes cambiar esta ruta
        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
        with open(ruta_salida, "w", encoding="utf-8") as archivo:
            for i in resultado:
                archivo.write(str(i) + "\n")  # Asegura que cada resultado esté en una línea

        print(f"\nResultado guardado correctamente en: {ruta_salida}")




