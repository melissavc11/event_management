
import unittest
from modelo import GestionEventos


class TestGestorEventos(unittest.TestCase):

    def setUp(self):
        self.gestion_eventos = GestionEventos()

    def test_post_events(self):
        result = self.gestion_eventos.post_events(
            "Evento de Prueba", "2023-10-15 15:00:00", "Descripción de prueba", 1)
        self.assertIsNotNone(result)
        self.assertIn("mensaje", result)

    def test_get_events(self):
        result = self.gestion_eventos.get_events()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    def test_get_event_by_id(self):
        result = self.gestion_eventos.get_event_by_id(1)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    def test_put_event_by_id(self):
        result = self.gestion_eventos.put_event_by_id(
            1, "Evento Actualizado", "2023-10-15 18:00:00", "Descripción actualizada", 1)
        self.assertIsNotNone(result)
        self.assertIn("mensaje", result)

    def test_delete_event_by_id(self):
        result = self.gestion_eventos.delete_event_by_id(1)
        self.assertIsNotNone(result)
        self.assertIn("mensaje", result)


if __name__ == '__main__':
    unittest.main()