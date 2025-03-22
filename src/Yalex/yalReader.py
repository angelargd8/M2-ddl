
# parseo del yalex
class yalReader:
    def __init__(self, text):
        self.text = text
        self.list = [] # para llevar el orden / es necesario cuidar la precedencia
        self.dicc = {}  # diccionario para las definiciones
        self.rules_tokens = []
        self.header = ""
        self.trailer = ""
        self.simbols = "+*|()[]-?'"

        # self.remove_comments()
        # self.read_yalex()
        # self.parse()

    # recolectar el header y trailer y guardarlos
    def header_trailer(self):
        pass


    # en el caso de expresiones como [a-z] nos apoyamos del orden ascii y de las funciones de ord y chr
    # parsea las expresiones regulares a algo que podamos reconocer
    def parse(self):
        for n in self.list:
            expresion = self.dicc[n]
            i = 0
            new_exp = ""
            while i < len(expresion):
                if expresion[i] == "[": # significa que es una expresión regular y hay que parsearla
                    cadena = True
                    while cadena:
                        i += 1
                        if expresion[i] == "'": # si empieza con comillas simples cada caracter está en comillas simples y se debe de separar por ellas
                            new_exp += expresion[i+1]
                            i += 2
                            while expresion[i] != "'":
                                new_exp += expresion[i]
                                i += 1
                            if expresion[i+1] == "-": # expresiones que sean de 'a'-'z'
                                new_exp += "|"
                                new_exp += self.get_ascii(expresion[i-1], expresion[i+3])
                                i += 5 # se salta hasta la siguiente expresion porque ya validó el rango
                            if i+2 < len(expresion):
                                new_exp += "|"
                        if expresion[i] == "\"": # si la expresion empieza con " comillas dobles, significa que la separacion es diferente
                            i += 1
                            while expresion[i] != "\"":
                                new_exp += expresion[i]
                                i += 1
                                if i + 2 < len(expresion):
                                    new_exp += "|"

                        if expresion[i] == "]": # termina la cadena dentro de []
                            cadena = False
                            i += 1

                else: # significa que hace referencia a otra variable y hay que remplazarla
                    # leemos letra por letra hasta encontrar un simbolo
                    temp = ""
                    # se guarda en un temp para evaluar si existe en el diccionario
                    # si existen se remplaza por el valor que ya tenia
                    pass


            self.dicc[n] = new_exp # se remplaza la expresion ya formateada en regex para su uso mas adelante
            return new_exp


    # lee el archivo para colocarlo en los diccionarios y
    def read_yalex(self):
        i = 0
        while i < len(self.text):
            if self.text[i:i + 4] == "let ":
                i += 4  # Avanzamos después de "let "

                # Obtener nombre de la variable
                # sabemos que despues de let viene inmediatamente el nombre de la variable
                nombre = ""
                while i < len(self.text) and self.text[i].isalnum():
                    nombre += self.text[i]
                    i += 1

                # Saltar espacios en blanco y encontrar el '='
                while i < len(self.text) and self.text[i] in " \t":
                    i += 1

                if i < len(self.text) and self.text[i] == "=":
                    i += 1  # Saltar '='

                # Obtener valor (hasta encontrar un salto de línea que no esté dentro de [])
                # También lee lo que no este dentro de [] y termina cuando encuentra \n
                valor = ""
                dentro_corchetes = False
                while i < len(self.text):
                    if self.text[i] == "[":
                        dentro_corchetes = True
                    elif self.text[i] == "]":
                        dentro_corchetes = False
                    elif self.text[i] == "\n" and not dentro_corchetes:
                        break  # Fin del valor

                    valor += self.text[i]
                    i += 1

                self.list.append(nombre.strip()) # agrega el nombre a la lista para saber el orden en el que aparecieron
                self.dicc[nombre.strip()] = valor.strip() # agrega el nombre y expresión al diccionario

            # rules tokens
            if self.text[i:i + 4] == "rule":
                pass
            i += 1  # Avanzar en el código

        #print(self.dicc)
        # return True # para el módulo de pruebas

    # elimina los comentarios del texto
    def remove_comments(self):
        result = []
        i = 0
        inside_comment = False

        while i < len(self.text):
            if self.text[i:i + 2] == "(*":
                inside_comment = True
                i += 2  # Saltar el inicio del comentario
            elif self.text[i:i + 2] == "*)" and inside_comment:
                inside_comment = False
                i += 2  # Saltar el final del comentario
            elif not inside_comment:
                result.append(self.text[i])
                i += 1
            else:
                i += 1  # Ignorar caracteres dentro del comentario

        # sustituye el texto ya sin los comentarios, strip quita los espacios
        self.text = "".join(result).strip()


    # regresar el rango de caracteres con ayuda de ascii
    # regresa toda la expresión a excepción del primero
    def get_ascii(self, inicio, fin)-> str:
        return '|'.join(chr(i) for i in range(ord(inicio) + 1, ord(fin) + 1))






