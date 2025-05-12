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
    ruta = os.path.join("src//Yalex//yalDocs//", archivo_yal)
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

        texto_prueba = leerArchivo("./Test.txt")
        if texto_prueba:
            print("\nContenido de Test.txt:")
            print(texto_prueba)

            resultados = simular_texto(texto_prueba, automata_lexico)

            print("\nResultados de la simulación:")
            for palabra, token in resultados:
                print(f"{palabra} -> {token}")

            guardar_resultado_en_txt(resultados, "src/Yalex/Out/TokensRead.txt")
            print("\nResultados guardados en src/Yalex/Out/TokensRead.txt")


tokens = {
    "WHITESPACE": "( |\t|\n)+",
    "ID": "(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)((A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)|((_))|(0|1|2|3|4|5|6|7|8|9))",
    "NUMBER": "((0|1|2|3|4|5|6|7|8|9)+)(ε|(\\.(0|1|2|3|4|5|6|7|8|9)+))(ε|(E(ε|(\\+|-))(0|1|2|3|4|5|6|7|8|9)+))",
    "SEMICOLON": ";",
    "ASSIGNOP": ":=",
    "LT": "<",
    "EQ": "=",
    "PLUS": "\\+",
    "MINUS": "-",
    "TIMES": "\\*",
    "DIV": "/",
    "LPAREN": "\\(",
    "RPAREN": "\\)",
}
