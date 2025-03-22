
# parseo del yalex
class yalReader:
    def __init__(self, file):
        self.file = file

    # parsea las expresiones regulares a algo que podamos reconocer
    # en el caso de expresiones como [a-z] nos apoyamos del orden ascii y de las funciones de ord y chr
    def parse(self, string):
        pass

    # elimina los comentarios del texto
    def remove_comments(text):
        result = []
        i = 0
        inside_comment = False

        while i < len(text):
            if text[i:i + 2] == "(*":
                inside_comment = True
                i += 2  # Saltar el inicio del comentario
            elif text[i:i + 2] == "*)" and inside_comment:
                inside_comment = False
                i += 2  # Saltar el final del comentario
            elif not inside_comment:
                result.append(text[i])
                i += 1
            else:
                i += 1  # Ignorar caracteres dentro del comentario

        return "".join(result).strip()






