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




def mapear_posiciones_simbolos(nodo, posicion_a_simbolo):
    # si el nodo es None, terminar la función y retornar
    if nodo is None:
        return
    
    #verificar si el nodo es una hoja o un simbolo, este tiene un id unico
    if (nodo.left is None and nodo.right is None) or nodo.value not in ['.', '*', '+', '|', '^']:
        posicion_a_simbolo[nodo.id] = nodo.value
    
    # recorrer subarboles
    mapear_posiciones_simbolos(nodo.left, posicion_a_simbolo)
    mapear_posiciones_simbolos(nodo.right, posicion_a_simbolo)


def construir_AFD(arbolSintactico, followpos):
    #1 . instanciar AFD
    afd = AFD()
    
    #2. mapear posiciones a simbolos
    posicion_a_simbolo = {}
    mapear_posiciones_simbolos(arbolSintactico, posicion_a_simbolo)
    
    #3. Obtener el alfabeto sin tomar en cuenta los caracteres especiales y operadores
    alfabeto = set()
    for pos, simbolo in posicion_a_simbolo.items():
        if simbolo not in ['*', '+', '.', '|', '#', '^', 'ε', 'e']:
            alfabeto.add(simbolo)
    afd.alfabeto = alfabeto
    
    # 4. definir el estado inicial como el conjunto firstpos de la raiz del arbol
    estado_inicial = frozenset(arbolSintactico.firstpos)
    
    # 5. iniciar diccionario de estados y la  lista de estados del AFD
    estados_dict = {estado_inicial: 0}
    afd.estados = [0]
    afd.estado_inicial = 0
    
    # 6. iniciar la lista de estados no marcados, estos son los que estan pendientes de procesar
    no_marcados = [estado_inicial]
    
    # 7. encontrar la posicion del simbolo # (fin de la cadena)
    posicion_fin = None
    for pos, simbolo in posicion_a_simbolo.items():
        if simbolo == '#':
            posicion_fin = pos
            break
    
    #8. procesar los estados no marcados
    while no_marcados:
        # 8.1 sacar el estado no marcado
        estado_actual = no_marcados.pop(0)
        id_estado_actual = estados_dict[estado_actual]
        
        # 8.2  recorrer cada simbolo del alfabeto
        for simbolo in alfabeto:
            #encontrar todas las posiciones que tienen este simbolo
            posiciones_simbolo = set() 
            for pos in estado_actual:
                if pos in posicion_a_simbolo and posicion_a_simbolo[pos] == simbolo:
                    posiciones_simbolo.add(pos)
            
        # 8.3. si hay posiciones con el simbolo, caulcular el nuevo estado segun el followpos
            if posiciones_simbolo:
                nuevo_estado = set()
                # recorrer las posiciones del simbolo
                for pos in posiciones_simbolo:
                    if pos in followpos:
                        nuevo_estado.update(followpos[pos])
                
                nuevo_estado = frozenset(nuevo_estado)
                
        # 8.4 si es un nuevo estado, añadirlo
                if nuevo_estado and nuevo_estado not in estados_dict:
                    estados_dict[nuevo_estado] = len(afd.estados)
                    afd.estados.append(len(afd.estados))
                    no_marcados.append(nuevo_estado)
                
        # 8.5 añadir la transicion
                if nuevo_estado:
                    afd.agregar_transiciones(id_estado_actual, simbolo, estados_dict[nuevo_estado])
        
        # 9. marcar el estado como final si el estado tiene la posicion de #, xq es estado final
        if posicion_fin in estado_actual:
            afd.agregar_estado_final(id_estado_actual)

    return afd
    # return minimizar_AFD(afd)


def minimizar_AFD(afd):
    # 1. Inicializar partición con estados finales y no finales
    particion = [set(afd.estados_finales), set(afd.estados) - set(afd.estados_finales)]
    nueva_particion = []

    while nueva_particion != particion:
        if nueva_particion:
            particion = nueva_particion
        nueva_particion = []

        for grupo in particion:
            subgrupos = defaultdict(set)

            for estado in grupo:
                # Clave única para identificar cómo el estado se comporta con cada símbolo
                clave = tuple(
                    (simbolo, frozenset(encontrar_grupo(afd.transiciones.get(estado, {}).get(simbolo), particion) or {}))
                    for simbolo in afd.alfabeto
                )
                subgrupos[clave].add(estado)

            nueva_particion.extend(subgrupos.values())

    # 2. Crear nuevo AFD minimizado
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
    """ Encuentra a qué grupo pertenece un estado en la partición """
    if estado is None:
        return None
    for grupo in particion:
        if estado in grupo:
            return grupo
    return None
