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


archivos = ["slr-2.yal"]  # Lista de archivos YAL

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

        lexical_automata = generar_afd_unificado(tokens)
        _serialize_automata(lexical_automata, "lexical_out")

        print("\nContenido de Test.txt: \n")
        print(texto_prueba)

        print("\n--- SIMULANDO texto ---")
        resultado = simular_texto(texto_prueba, lexical_automata)
        print(resultado)


