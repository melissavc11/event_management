class GestionEventos:
    def __init__(self):
        self.gestor = GestorJson()

    def post_events(self, titulo_evento, fecha_hora_evento, descripcion_evento,
                     ubicacion_evento):
        pass

    def get_events(self):
        pass

    def get_event_by_id(self, id_evento):
        pass

    def put_event_by_id(self, id_evento, titulo_evento, fecha_hora_evento,
                         descripcion_evento, ubicacion_evento):
        pass

    def delete_event_by_id(self, id_evento):
        pass

class GestorJson:
    def __init__(self):
        pass