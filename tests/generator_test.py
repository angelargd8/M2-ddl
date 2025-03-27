import unittest
import os
import sys


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "Yalex"))
)

from src.Yalex.generator import generar_afds


class TestGenerator(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para los tests"""
        self.tokens = {
            "delim": " |\t|\n",  # Espacios, tabulaciones y saltos de línea
            "ws": "( |\t|\n)+",  # Uno o más delimitadores
            "letter": "(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)",
            "digit": "(0|1|2|3|4|5|6|7|8|9)",
            "id": "(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)((A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|)|(0|1|2|3|4|5|6|7|8|9))*",
            "PLUS": r"\+",  # Literal "+"
            "TIMES": r"\*",  # Literal "*"
            "LPAREN": r"\(",  # Literal "("
            "RPAREN": r"\)",  # Literal ")"
        }

        self.output_dir = "generatorAFDS"

    def test_afds_generation(self):
        """Verifica que los AFDs se generen correctamente"""
        afds = generar_afds(self.tokens)

        # Comprobar que se crearon AFDs para cada token
        self.assertIn("delim", afds)
        # self.assertIn("id", afds)
        self.assertIsNotNone(afds["delim"])
        # self.assertIsNotNone(afds["id"])

    def test_afds_structure(self):
        """Verifica que los AFDs tengan la estructura esperada"""
        afds = generar_afds(self.tokens)
        delim_afd = afds["delim"]
        # id_afd = afds["id"]

        self.assertTrue(hasattr(delim_afd, "estados"))
        # self.assertTrue(hasattr(id_afd, "estados"))
        self.assertTrue(hasattr(delim_afd, "alfabeto"))
        # self.assertTrue(hasattr(id_afd, "alfabeto"))

    def test_graphical_output(self):
        """Verifica que las imágenes de los AFDs se generen en generatorAFDS"""
        generar_afds(self.tokens)  # Generar los AFDs y graficarlos

        # Revisar si los archivos PNG existen
        for token in self.tokens:
            file_path = os.path.join(self.output_dir, f"AFD_{token}.png")
            self.assertTrue(
                os.path.exists(file_path), f"El archivo {file_path} no fue generado."
            )

    def tearDown(self):
        """Limpieza: Opcional, eliminar imágenes generadas tras la prueba"""
        for token in self.tokens:
            file_path = os.path.join(self.output_dir, f"AFD_{token}.png")
            if os.path.exists(file_path):
                os.remove(file_path)


if __name__ == "__main__":
    unittest.main()
