import unittest

dicc = {"delim": " |\t|\n", "id": "a|b|c|d"}
text = "hola 123 3 + 5"

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
