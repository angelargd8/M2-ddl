from graphviz import Graph

class Estado:
   
    def __init__(self, number, trans = None):
        self.number = number
        self.transicion = trans
        self.hijo1 = None
        self.hijo2 = None
        self.final = None

       

        
