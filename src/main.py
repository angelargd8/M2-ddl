from Automata.constructor import leerArchivo
from Automata.arboles import construirArbolSintactico, imprimirArbolSintactico
from Automata.Regex import infixToPostfix
from Automata.AFD import *
from Automata.Node import *
from collections import defaultdict
from Automata.graficadora import visualize_afd
import logging
from Yalex.yalReader import yalReader
import os

import os

def leerArchivo(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return archivo.read()
    except Exception as e:
        print(f"Error al leer {ruta}: {e}")
        return None

# Lista de archivos con extensión .yal en la carpeta yalDocs
# archivos = ["slr-1.yal", "slr-2.yal", "slr-3.yal", "slr-4.yal"]  # Asegúrate de que los nombres sean correctos
archivos = ["slr-4.yal"]  # Asegúrate de que los nombres sean correctos


for i in archivos:
    ruta = os.path.join("Yalex/yalDocs", i)  # Construye la ruta
    text = leerArchivo(ruta)
    if text is not None:
        print(f"Archivo {i} leido correctamente")
        # parseamos el doc y obtenemos los tokens
        yal = yalReader(text)
        print(yal.get_tokens())




