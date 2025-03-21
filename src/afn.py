# from graphviz import Graph
from src.estados import Estado

class Afn:
    def __init__(self):
        # self.diagram = Graph(format="png")
        self.inicio = None
        self.final = None
        self.cont = 1
        self.stack = [] #para la concatenacion

    def crearNodo(self, trans= None):
        estado = Estado(self.cont, trans)
        self.cont += 1
        return estado
    
    #renderizar el automata 
    # def render(self, cont):
    #     self.diagram.edge("start", str(self.inicio.number), "e",dir = "forward")
    #     self.diagram.node(str(self.final.number), shape="doublecircle")
    #     self.diagram.render(f'AutomataNFA/NFA{cont}', format='png', cleanup=False)
    #     print("creado afn", str(self.final.number))

        
def crearAFN(tree, afn):
    
    # Procesar el hijo izquierdo
    if tree.left:
        crearAFN(tree.left, afn)
    
    # Procesar el hijo derecho
    if tree.right:
        crearAFN(tree.right, afn)

    # Procesar el nodo actual
    if tree.value: #si encuentra un valor llama a la funcion de thompson
        thompson(tree.value, afn)
        print(tree.value)
    
    return afn


def thompson(value, afn):
    operators = {'|':2 , '.':2, '*':1}
    if value not in operators:
        # print("creado", value)

        nodo = afn.crearNodo(value) # creo el primer nodo, mandando como parametro value, que es la transicion
        nodo2 = afn.crearNodo() # creo el segundo nodo 
        nodo.hijo1 = nodo2 # hago el link del primer nodo con el segundo 
        nodo.final = nodo2

        if not afn.stack:
            afn.inicio = nodo # por el momento mi afn tiene por inicio el nodo creado
        afn.final = nodo2 # por el momento mi afn tiene por final el nodo creado 


        afn.stack.append(nodo) # agrego al stack para seguir evaluando 

        # # ir armando el afn visual 
        # afn.diagram.node(str(nodo.number), str(nodo.number), shape = "circle")
        # afn.diagram.node(str(nodo2.number), str(nodo2.number), shape = "circle")
        # afn.diagram.edge(str(nodo.number), str(nodo2.number), value, dir = "forward", labeldistance="1.5") #edge es la fechita
        # print(afn.final.number)
    else:
        if value == ".":
            nodob = afn.stack.pop()       
            nodoa = afn.stack.pop()

            #nuevo inicio y final
            afn.final = nodob.final
            afn.inicio = nodoa
            afn.stack.append(nodoa)
            
            # # diagrama
            # afn.diagram.edge(str(nodoa.final.number), str(nodob.number),"e",dir = "forward", shape = "circle")
        
            nodoa.final.hijo1 = nodob
            nodoa.final = nodob.final
            


        if value == "*":
            # crear un primer nodo 
            nodo = afn.crearNodo()
            # crear el nodo final 
            nodo2 = afn.crearNodo()

            # obtener el hijo al que se le aplica el * 
            hijo1 = afn.stack.pop()
            temp = afn.final

            # hacer las relaciones del * 
            nodo.hijo1 = hijo1 
            nodo.hijo2 = nodo2
            afn.final.hijo1 = hijo1
            afn.final.hijo1 = nodo2

            # modificar inicio y final 
            afn.inicio = nodo
            afn.final = nodo2

            # agregar al stack 
            nodo.final = nodo2
            afn.stack.append(nodo)

            # # se dibuja el diagrama
            # afn.diagram.node(str(nodo.number), str(nodo.number), shape = "circle")
            # afn.diagram.node(str(nodo2.number), str(nodo2.number), shape = "circle")

            # afn.diagram.edge(str(nodo.number), str(hijo1.number), "e", dir = "forward", labeldistance="1.5")
            # afn.diagram.edge(str(nodo.number), str(nodo2.number), "e", dir = "forward", labeldistance="1.5")
            
            # afn.diagram.edge(str(temp.number), str(hijo1.number), "e", dir = "forward", labeldistance="1.5")
            # afn.diagram.edge(str(temp.number), str(nodo2.number), "e", dir = "forward", labeldistance="1.5")
        

        if value == "|":
            # print("creado", value)
            nodo = afn.crearNodo() # se crea el nodo para unir

            hijo1 = afn.stack.pop() # se obtiene el nodo del hijo 1
            hijo2 = afn.stack.pop() # se obtiene el nodo del hijo 2 
            
            # asigno los hijos al nuevo nodo inicial 
            nodo.hijo1 = hijo1
            nodo.hijo2 = hijo2

            # asigno al afn su nuevo inicio 
            afn.inicio = nodo

            # creo el nodo final 
            nodof = afn.crearNodo()
            afn.final = nodof

            # agregar al stack
            nodo.final = afn.final
            afn.stack.append(nodo)

            # # se dibuja el diagrama

            # afn.diagram.node(str(nodo.number), str(nodo.number), shape = "circle")
            # afn.diagram.node(str(nodof.number), str(nodof.number), shape = "circle")

            # afn.diagram.edge(str(nodo.number), str(hijo1.number), "e", dir = "forward", labeldistance="1.5")
            # afn.diagram.edge(str(nodo.number), str(hijo2.number), "e", dir = "forward", labeldistance="1.5")
            
            # afn.diagram.edge(str(hijo1.final.number), str(nodof.number), "e", dir = "forward", labeldistance="1.5")
            # afn.diagram.edge(str(hijo2.final.number), str(nodof.number), "e", dir = "forward", labeldistance="1.5")
        
