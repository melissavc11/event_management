import unittest
from controlador import app

class TestApi(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_1_get_events(self):
        response = self.app.get('/events')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json)

    def test_2_create_event_invalid_date(self):
        event_data = {
            "titulo_evento": "Evento de Prueba",
            "fecha_hora_evento": "2023-10-15 15:00:00",
            "descripcion_evento": "Descripción del evento de prueba",
            "ubicacion_evento": 1
        }
        response = self.app.post('/events', json=event_data)
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.json)

    def test_3_create_event(self):
        event_data = {
            "titulo_evento": "Evento de Prueba",
            "fecha_hora_evento": "2025-10-15 16:00:00",
            "descripcion_evento": "Descripción del evento de prueba",
            "ubicacion_evento": 1
        }
        response = self.app.post('/events', json=event_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('mensaje', response.json)

    def test_3_create_event_sin_disponibilidad(self):
        event_data = {
            "titulo_evento": "Evento de Prueba",
            "fecha_hora_evento": "2025-10-15 16:00:00",
            "descripcion_evento": "Descripción del evento de prueba",
            "ubicacion_evento": 1
        }
        response = self.app.post('/events', json=event_data)
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.json)

    def test_4_get_event_by_invalid_id_type(self):
        response = self.app.get('/events/s')
        self.assertEqual(response.status_code, 404)

    def test_5_get_event_by_invalid_id_value(self):
        response = self.app.get('/events/0')
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.json)

    def test_6_get_event_by_id(self):
        response = self.app.get('/events/4')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json)

    def test_7_update_event(self):
        event_data = {
            "titulo_evento": "Evento Actualizado",
            "fecha_hora_evento": "2026-10-15 18:00:00",
            "descripcion_evento": "Descripción actualizada",
            "ubicacion_evento": 1
        }
        response = self.app.put('/events/5', json=event_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('mensaje', response.json)

    def test_8_delete_invalid_event(self):
        response = self.app.delete('/events/1')
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.json)

    def test_9_delete_invalid_event_id_type(self):
        response = self.app.delete('/events/s')
        self.assertEqual(response.status_code, 404)
    

    def test_10_delete_event(self):
        response = self.app.delete('/events/5')
        self.assertIn('mensaje', response.json)
        self.assertEqual(response.status_code, 200)


    def test_11_get_locations(self):
        response = self.app.get('/locations')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json)

if __name__ == '__main__':
    unittest.main()
