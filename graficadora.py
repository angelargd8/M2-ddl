import os
import re
from graphviz import Digraph


def graficar_afd(afd, i):
    """
    Genera un diagrama del AFD utilizando Graphviz y lo guarda en la carpeta Visual_AFD.

    Parámetros:
    - afd: objeto AFD con atributos 'estados', 'estado_inicial', 'estados_finales' y 'transiciones'
    - nombre_archivo: nombre base para el archivo (se sanitizará para quitar caracteres inválidos)
    """
    # Crear la carpeta Visual_AFD si no existe
    output_dir = "Visual_AFD"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Sanitizar el nombre del archivo (reemplazar caracteres no válidos)
    # Los caracteres no permitidos en Windows son: \ / : * ? " < > |

    # Crear el grafo dirigido
    dot = Digraph(comment="AFD", format="png")

    # Agregar los nodos correspondientes a cada estado del AFD
    for estado in afd.estados:
        # Si el estado es de aceptación se marca con doble círculo
        if estado in afd.estados_finales:
            dot.node(str(estado), label=str(estado), shape="doublecircle")
        else:
            dot.node(str(estado), label=str(estado))

    # Nodo invisible de inicio para indicar el estado inicial
    dot.node("start", label="", shape="none")
    dot.edge("start", str(afd.estado_inicial), label="Inicio")

    # Agregar las transiciones
    for origen, trans in afd.transiciones.items():
        for simbolo, destinos in trans.items():
            # En un AFD se espera que 'destinos' sea un conjunto con un único elemento
            for destino in destinos:
                dot.edge(str(origen), str(destino), label=simbolo)

    # Renderizar y guardar el diagrama en la carpeta Visual_AFD
    file_path = os.path.join(output_dir, i)
    dot.render(file_path, view=False, cleanup=True)
