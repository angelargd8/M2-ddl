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
        print("---"*7)

    def __str__(self):
        return f"AFD(estados={self.estados}, alfabeto={self.alfabeto}, estado_inicial={self.estado_inicial}, estados_finales={self.estados_finales}, transiciones={self.transiciones})"



def construir_AFD(raiz, followpos):
    afd = AFD()
    #1. identificar los estados del AFD
    print(raiz)
    return afd


