import unittest
from modelo import GestorJson
class TestGestorJson(unittest.TestCase):

    def setUp(self):
        self.gestor_json = GestorJson()

    def test_leer_archivo(self):
        data = self.gestor_json.leer_archivo()
        self.assertIsNotNone(data)
        self.assertIsInstance(data, dict)
