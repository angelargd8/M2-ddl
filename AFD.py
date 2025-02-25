from collections import deque, defaultdict


class AFD:
    def __init__(self):
        self.estados = []
        self.alfabeto = set()
        self.estado_inicial = None
        self.estados_finales = set()
        self.transiciones = defaultdict(dict)

    def agregar_transiciones(self, estado_origen, simbolo, estado_destino):
        self.transiciones[estado_origen][simbolo] = estado_destino

    def agregar_estado_inicial(self, estado):
        self.estado_inicial = estado

    def agregar_estado_final(self, estado):
        self.estados_finales.add(estado)

    def mostrar(self):
        print("Estados:", self.estados)
        print("Alfabeto:", self.alfabeto)
        print("Estado inicial:", self.estado_inicial)
        print("Estados finales:", self.estados_finales)
        print("Transiciones:")
        for estado_origen in self.transiciones:
            for simbolo in self.transiciones[estado_origen]:
                estado_destino = self.transiciones[estado_origen][simbolo]
                print(f"{estado_origen} -> {estado_destino} [simbolo: {simbolo}]")
        print("---" * 15)

    def __str__(self):
        return f"AFD(estados={self.estados}, alfabeto={self.alfabeto}, estado_inicial={self.estado_inicial}, estados_finales={self.estados_finales}, transiciones={self.transiciones})"


def buscar_raiz(followpos):
    nodos = set(followpos.keys())
    nodos2=  set(followpos.keys())
    valores = set()

    for conjunto in followpos.values():
        # print(conjunto)
        valores.update(conjunto)

    diferencia = nodos - valores
    # print(f"Nodos: {nodos}")
    # print(f"Valores: {valores}")
    # print(f"Diferencia (Raiz): {diferencia}")
    # print(f"\n ")

    if len(diferencia) != 0:
        raiz = list(diferencia)
        raiz = raiz[0]
        # print(raiz)

    # elif len(nodos) != 0:
    #     raiz = list(nodos)
    #     raiz = nodos[0]

    elif len(diferencia) ==0: 
        raiz = list(nodos2)[0]

    #     raiz = list(nodos)[0]
    # else:
    #     raise ValueError("No se pudo encontrar la raíz porque 'nodos' está vacío.")

    # print(f"Raiz final: {raiz}")
    return raiz


def construir_tabla_transicion(afd, followpos, alfabeto):
     # recorrer los estados y el follow pos
    for estado, posiciones in followpos.items():
        afd.transiciones[estado] = {}  
        
        # recorrer las posiciones
        for pos in posiciones:
            # recorrer el alfabeto
            for simbolo in alfabeto:
                if simbolo not in afd.transiciones[estado]:
                    afd.transiciones[estado][simbolo] = set()
                afd.transiciones[estado][simbolo].add(pos)
    return  afd.transiciones

def definir_estados_aceptacion(afd, posicion_aceptacion):
    for estado in afd.estados:
        if posicion_aceptacion == estado:
            afd.agregar_estado_final(estado)
    return afd.estados_finales


def construir_AFD(arbolSintactico, followpos):
    
    # instanciar afd
    afd = AFD()
    # 1. definir el estado inicial
    # buscar la raiz del nodo
    raiz = buscar_raiz(followpos)
    afd.agregar_estado_inicial(raiz)

    # 2. identificar los estados del AFD
    # estados
    for estados in followpos:
        # print(estados)
        afd.estados.append(estados)

    # crear el alfabeto recorriendo el arbol
    nodos = [arbolSintactico]
    while nodos:
        nodo = nodos.pop()
        if (nodo.value.isalnum() and nodo.value != "ε") or (
            nodo.value.isalnum() and nodo.value != "e"
        ):
            afd.alfabeto.add(nodo.value)
        if nodo.left:
            nodos.append(nodo.left)
        if nodo.right:
            nodos.append(nodo.right)

    # 3. construir la tabla de transicion  con el follow pos
    construir_tabla_transicion(afd, followpos, afd.alfabeto)

    # 4. definir los estados de aceptacion
    # identificar la posicion de aceptacion
    posicion_aceptacion = max(followpos.keys())

    # buscar los estados que tengan la posicion de aceptacion
    definir_estados_aceptacion(afd, posicion_aceptacion)

    return afd


def minimizar_afd(afd):
    # Paso 1: Inicializar la partición con dos grupos: estados finales y no finales
    particion = [set(afd.estados_finales), set(afd.estados) - set(afd.estados_finales)]

    # Paso 2: Refinar la partición hasta que no haya cambios
    while True:
        nueva_particion = []
        for grupo in particion:
            if len(grupo) <= 1:
                nueva_particion.append(grupo)
                continue

            # Crear un diccionario para almacenar las transiciones de cada estado en el grupo
            transiciones_grupo = {}
            for estado in grupo:
                transiciones_grupo[estado] = {}
                for simbolo in afd.alfabeto:
                    estado_destino = afd.transiciones[estado].get(simbolo, None)
                    transiciones_grupo[estado][simbolo] = estado_destino

            # Crear un diccionario para agrupar estados con las mismas transiciones
            grupos_transiciones = defaultdict(list)
            for estado, transiciones in transiciones_grupo.items():
                grupos_transiciones[tuple((k, tuple(sorted(v))) for k, v in transiciones.items())].append(estado)


            # Agregar los nuevos grupos a la nueva partición
            for nuevo_grupo in grupos_transiciones.values():
                nueva_particion.append(set(nuevo_grupo))

        # Si la partición no cambia, terminamos
        if nueva_particion == particion:
            break
        particion = nueva_particion

    # Paso 3: Crear el AFD minimizado
    afd_minimizado = AFD()
    afd_minimizado.alfabeto = afd.alfabeto

    # Mapear cada estado original a su representante en el AFD minimizado
    mapeo_estados = {}
    for grupo in particion:
        representante = min(grupo)  # Elegir el estado con el menor valor como representante
        for estado in grupo:
            mapeo_estados[estado] = representante

    # Agregar los estados al AFD minimizado
    afd_minimizado.estados = list(set(mapeo_estados.values()))

    # Agregar el estado inicial
    afd_minimizado.agregar_estado_inicial(mapeo_estados[afd.estado_inicial])

    # Agregar los estados finales
    for estado_final in afd.estados_finales:
        afd_minimizado.agregar_estado_final(mapeo_estados[estado_final])

    # Agregar las transiciones
    for estado in afd_minimizado.estados:
        for simbolo in afd_minimizado.alfabeto:
            estado_destino = afd.transiciones[estado].get(simbolo, None)
            if estado_destino is not None:
                if isinstance(estado_destino, set) and estado_destino:
                    estado_destino = min(estado_destino)  # Elegir un estado representativo
                afd_minimizado.agregar_transiciones(estado, simbolo, mapeo_estados.get(estado_destino, None))

    return afd_minimizado