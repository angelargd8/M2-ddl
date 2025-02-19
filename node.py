# from graphviz import Graph


class Node:
    latest_id = 0
    # tree_graph = Graph(format='png')

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.nullable = False
        self.firstpos = set()
        self.lastpos = set()
        self.followpos = set()

        Node.latest_id += 1
        self.id = Node.latest_id
    #imprimir el arbol en formato grafico
    def printTree(self):
        # Node.tree_graph.node(str(self.id), self.value)
        if self.left:
            # Node.tree_graph.edge(str(self.id), str(self.left.id))
            self.left.printTree()
        
        if self.right:
            # Node.tree_graph.edge(str(self.id), str(self.right.id))
            self.right.printTree()

    # renderizr el arbol y guardarlo en un archivo
    def renderTree(self):
        Node.tree_graph.render('arboles', view=True)

    # esta funcion, nos la dio la IA porque no entontraba un error en el arbol sintactico 
    def __str__(self):
        return f"Node(value={self.value}, id={self.id}, nullable={self.nullable}, firstpos={self.firstpos}, lastpos={self.lastpos})"

#la tablita de siguientepos
#en esto tambien nos ayudo la IA para verificar que todo estuviera bien
def calcular_followPos(node, followpos):

    if node is None:
        return
    
    calcular_followPos(node.left, followpos)
    calcular_followPos(node.right, followpos)

    if node.value == '.':
        for pos in node.left.lastpos:
            if pos not in followpos: 
                followpos[pos] = set()

            followpos[pos].update(node.right.firstpos)

    if node.value == '*':
        for pos in node.left.lastpos:
            if pos not in followpos: 
                followpos[pos] = set()

            followpos[pos].update(node.left.firstpos)
