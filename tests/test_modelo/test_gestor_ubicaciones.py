import unittest
from modelo import GestorUbicacion

class TestGestorUbicacion(unittest.TestCase):

    def setUp(self):
        self.gestor_ubicacion = GestorUbicacion()

    def test_get_ubicaciones(self):
        ubicaciones = self.gestor_ubicacion.get_ubicaciones()
        self.assertIsNotNone(ubicaciones)
        self.assertIsInstance(ubicaciones, dict)
        self.assertIn("registro", ubicaciones)


if __name__ == '__main__':
    unittest.main()
