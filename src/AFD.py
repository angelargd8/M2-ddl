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
    # return minimizar_AFD(afd)


def minimizar_AFD(afd):
    particion = [set(afd.estados_finales), set(afd.estados) - set(afd.estados_finales)]
    nueva_particion = []
    
    while nueva_particion != particion:
        if nueva_particion:
            particion = nueva_particion
        nueva_particion = []
        
        for grupo in particion:
            subgrupos = defaultdict(set)
            for estado in grupo:
                clave = tuple((simbolo, encontrar_grupo(afd.transiciones.get(estado, {}).get(simbolo), particion)) for simbolo in afd.alfabeto)
                subgrupos[clave].add(estado)
            nueva_particion.extend(subgrupos.values())
    
    nuevo_afd = AFD()
    representantes = {next(iter(grupo)): grupo for grupo in nueva_particion if grupo}
    
    for representante, grupo in representantes.items():
        nuevo_afd.estados.append(representante)
        if representante in afd.estados_finales:
            nuevo_afd.agregar_estado_final(representante)
        if representante == afd.estado_inicial:
            nuevo_afd.agregar_estado_inicial(representante)
        
        for simbolo in afd.alfabeto:
            destino = afd.transiciones.get(representante, {}).get(simbolo)
            if destino is not None:
                grupo_destino = encontrar_grupo(destino, nueva_particion)
                if grupo_destino:
                    destino_representante = next(iter(grupo_destino), None)
                    if destino_representante is not None:
                        nuevo_afd.agregar_transiciones(representante, simbolo, destino_representante)
    
    nuevo_afd.alfabeto = afd.alfabeto
    return nuevo_afd

def encontrar_grupo(estado, particion):
    if estado is None:
        return None
    for grupo in particion:
        if estado in grupo:
            return grupo
    return None
