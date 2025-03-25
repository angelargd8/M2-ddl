# visualizador.py
import os
from graphviz import Digraph

def escaped_symbol(symbol):
    if symbol.startswith("\\"):
        special_chars = {'t', 'n', 'r', 'v', '\\', '0'}
        if symbol[1] not in special_chars:
            return symbol[1]
        return '\\\\' + symbol[1:]
    
    return symbol


def visualize_afd(afd, output_dir, file_name):
    """

    Parámetros:
    - afd: Objeto AFD que contiene los atributos:
        - estados (lista de identificadores)
        - estado_inicial (identificador del estado inicial)
        - estados_finales (conjunto de identificadores de estados de aceptación)
        - transiciones (diccionario de transiciones)
    - output_dir: Carpeta de salida donde se guardará el diagrama.
    - file_name: Nombre del archivo para guardar la imagen (sin extensión).
    """
    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    graph = Digraph()
    graph.attr(rankdir="LR")

    # Agregar nodos para cada estado
    for state in afd.estados:
        shape = "doublecircle" if state in afd.estados_finales else "circle"
        graph.node(str(state), shape=shape, label=str(state))

    # Nodo invisible de inicio que apunta al estado inicial
    graph.node("start", label="", shape="none", width="0", height="0")
    graph.edge("start", str(afd.estado_inicial), label="START", style="bold")

    # Agregar las transiciones
    for origen, trans in afd.transiciones.items():
        for symbol, destinos in trans.items():

            #procesar correctamente los caracteres escapados para la visualizacion
            display_symbol  = escaped_symbol(symbol)
            
            # Asegurarse de que destinos sea iterable
            if isinstance(destinos, int):  # Si es un solo entero
                destinos = [destinos]  # Convertirlo en lista

            for destino in destinos:
                graph.edge(str(origen), str(destino), label=display_symbol)


    output_path = os.path.join(output_dir, file_name)
    graph.render(output_path, format="png", cleanup=True)
    print(f"Se creó la imagen del AFD en {output_path}.png")
