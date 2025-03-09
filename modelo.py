import json
from datetime import datetime, timedelta


class GestionEventos:
    def __init__(self):
        self.gestor_json = GestorJson()
        self.gestor_ubicacion = GestorUbicacion()
        self.tabla = "eventos"

    def post_events(self, titulo_evento: str, fecha_hora_evento: datetime, descripcion_evento: str,
                    ubicacion_evento: int) -> dict:
        """
        Crear un evento.
        Si la fecha viene en formato de str hay que parsearla a datetime con datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S").

        Args:
            titulo_evento (str): Título del evento.
            fecha_hora_evento (datetime): Fecha y hora del evento, datetime viene de la librería datetime.
            descripcion_evento (str): Descripción del evento.
            ubicacion_evento (int): Ubicación del evento.

        Returns:
            dict: Mensaje de éxito o error.
            {"mensaje": "Evento creado", "codigo": 200} o
            {"mensaje": "Mensaje de error", "codigo": 500}

        Example:
        >>> gestion = GestionEventos()
        >>> fecha = datetime.strptime("2021-10-10 08:00:00", "%Y-%m-%d %H:%M:%S")
        >>> respuesta = gestion.post_events("Evento 1", fecha, "Descripción del evento 1", 1)
        """
        try:
            # Validacion de valores vacios
            titulo_evento = titulo_evento.replace("\n", "")
            if titulo_evento.strip() == "" or descripcion_evento.strip() == "":
                raise ValueError("Los campos no pueden estar vacíos")

            # Validacion de fecha y hora
            maximo_tiempo_Y = 2
            fecha_actual = datetime.now()
            if fecha_hora_evento < fecha_actual:
                raise ValueError(
                    "La fecha y hora del evento no puede ser menor a la fecha y hora actual")

            fecha_maxima = fecha_actual + \
                timedelta(days=(365*maximo_tiempo_Y))
            if fecha_hora_evento > fecha_maxima:
                raise ValueError(
                    "La fecha y hora del evento no puede ser mayor a dos años desde la fecha y hora actual")

            hora_minima = datetime.time(8, 0, 0)
            hora_maxima = datetime.time(22, 0, 0)
            if fecha_hora_evento.time() < hora_minima or fecha_hora_evento.time() > hora_maxima:
                raise ValueError(
                    "La hora del evento debe ser entre las 8:00 am y las 10:00 pm")

            if fecha_hora_evento.hour % 2 != 0 or fecha_hora_evento.minute != 0 or fecha_hora_evento.second != 0:
                raise ValueError(
                    "La hora del evento debe ser múltiplo de 2, y los minutos y segundos deben ser ceros")

            # Validacion de ubicacion
            ubicaciones = self.gestor_ubicacion.get_ubicaciones()
            if ubicaciones["codigo"] == 500:
                raise ValueError(ubicaciones["mensaje"])

            if ubicacion_evento < 0 or ubicacion_evento >= len(ubicaciones["registro"]):
                raise ValueError("La ubicación del evento no existe")

            eventos = self.gestor_json.buscar(self.tabla)
            if eventos["codigo"] == 500:
                raise ValueError(eventos["mensaje"])

            for evento in eventos["registro"]:
                if evento["ubicacion_evento"] == ubicacion_evento and evento["fecha_hora_evento"] == fecha_hora_evento.strftime("%Y-%m-%d %H:%M:%S"):
                    raise ValueError(
                        "La ubicación y fecha del evento ya están ocupadas por otro evento")

            respuesta = self.gestor_json.crear(self.tabla,
                                               ["titulo_evento", "fecha_hora_evento",
                                                   "descripcion_evento", "ubicacion_evento"],
                                               [titulo_evento, fecha_hora_evento.strftime("%Y-%m-%d %H:%M:%S"), descripcion_evento, ubicacion_evento])
            return respuesta
        except Exception as e:
            return {"mensaje": str(e), "codigo": 500}

    def get_events(self) -> dict:
        """
        Obtener todos los eventos.

        Returns:
            dict: Registro con mensaje de éxito o mensaje de error.
            {"registro": [{"campo1": "valor1", "campo2": "valor2", ...}, ...], "mensaje": "Registros encontrados", "codigo": 200} o
            {"mensaje": "Mensaje de error", "codigo": 500}

        Example:
        >>> gestion = GestionEventos()
        >>> respuesta = gestion.get_events()
        """
        try:
            respuesta = self.gestor_json.buscar(self.tabla)
            if respuesta["codigo"] == 500:
                raise ValueError(respuesta["mensaje"])
            ubicaciones = self.gestor_ubicacion.get_ubicaciones()
            if ubicaciones["codigo"] == 500:
                raise ValueError(ubicaciones["mensaje"])
            for evento in respuesta["registro"]:
                evento["ubicacion_evento"] = ubicaciones["registro"][evento["ubicacion_evento"]]
            return respuesta
        except Exception as e:
            return {"mensaje": str(e), "codigo": 500}

    def get_event_by_id(self, id_evento: int) -> dict:
        """
        Buscar un evento por su ID.

        Args:
            id_evento (int): ID del evento a buscar.

        Returns:
            dict: Registro con mensaje de éxito o mensaje de error.
            {"registro": {"campo1": "valor1", "campo2": "valor2", ...}, "mensaje": "Registro encontrado", "codigo": 200} o
            {"mensaje": "Mensaje de error", "codigo": 500}

        Example:
        >>> gestion = GestionEventos()
        >>> respuesta = gestion.get_event_by_id(1)
        """
        try:
            respuesta = self.gestor_json.buscar(self.tabla, id_evento)
            if respuesta["codigo"] == 500:
                raise ValueError(respuesta["mensaje"])
            ubicaciones = self.gestor_ubicacion.get_ubicaciones()
            if ubicaciones["codigo"] == 500:
                raise ValueError(ubicaciones["mensaje"])
            respuesta["registro"][0]["ubicacion_evento"] = ubicaciones["registro"][respuesta["registro"][0]["ubicacion_evento"]]
            return respuesta
        except Exception as e:
            return {"mensaje": str(e), "codigo": 500}

    def put_event_by_id(self, titulo_evento: str, fecha_hora_evento: datetime,
                        descripcion_evento: str, ubicacion_evento: str, id_evento: int) -> dict:
        """
        Actualizar un evento por su ID.
        Si la fecha viene en formato de str hay que parsearla a datetime con datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S").

        Args:
            titulo_evento (str): Título del evento.
            fecha_hora_evento (datetime): Fecha y hora del evento.
            descripcion_evento (str): Descripción del evento.
            ubicacion_evento (int): Ubicación del evento.
            id_evento (int): ID del evento a actualizar.

        Returns:
            dict: Mensaje de éxito o error.
            {"mensaje": "Evento actualizado", "codigo": 200} o
            {"mensaje": "Mensaje de error", "codigo": 500}

        Example:
        >>> gestion = GestionEventos()
        >>> fecha = datetime.strptime("2021-11-10 08:00:00", "%Y-%m-%d %H:%M:%S")
        >>> respuesta = gestion.put_event_by_id("Evento 1", fecha, "Descripción del evento 1", 1, 1)
        """
        try:
            # Validacion de existencia
            eventos = self.gestor_json.buscar(self.tabla, id_evento)
            if eventos["codigo"] in [404, 500]:
                raise ValueError(eventos["mensaje"])

            # Validacion de valores vacios
            titulo_evento = titulo_evento.replace("\n", "")
            if titulo_evento.strip() == "" or descripcion_evento.strip() == "":
                raise ValueError("Los campos no pueden estar vacíos")

            # Validacion de fecha y hora
            maximo_tiempo_Y = 2
            fecha_actual = datetime.now()
            if fecha_hora_evento < fecha_actual:
                raise ValueError(
                    "La fecha y hora del evento no puede ser menor a la fecha y hora actual")

            fecha_maxima = fecha_actual + \
                timedelta(days=(365*maximo_tiempo_Y))
            if fecha_hora_evento > fecha_maxima:
                raise ValueError(
                    "La fecha y hora del evento no puede ser mayor a dos años desde la fecha y hora actual")

            hora_minima = datetime.time(8, 0, 0)
            hora_maxima = datetime.time(22, 0, 0)
            if fecha_hora_evento.time() < hora_minima or fecha_hora_evento.time() > hora_maxima:
                raise ValueError(
                    "La hora del evento debe ser entre las 8:00 am y las 10:00 pm")

            if fecha_hora_evento.hour % 2 != 0 or fecha_hora_evento.minute != 0 or fecha_hora_evento.second != 0:
                raise ValueError(
                    "La hora del evento debe ser múltiplo de 2, y los minutos y segundos deben ser ceros")

            # Validacion de ubicacion
            ubicaciones = self.gestor_ubicacion.get_ubicaciones()
            if ubicaciones["codigo"] == 500:
                raise ValueError(ubicaciones["mensaje"])

            if ubicacion_evento < 0 or ubicacion_evento >= len(ubicaciones["registro"]):
                raise ValueError("La ubicación del evento no existe")

            eventos = self.gestor_json.buscar(self.tabla)
            if eventos["codigo"] == 500:
                raise ValueError(eventos["mensaje"])

            for evento in eventos["registro"]:
                if evento["ubicacion_evento"] == ubicacion_evento and evento["fecha_hora_evento"] == fecha_hora_evento.strftime("%Y-%m-%d %H:%M:%S"):
                    raise ValueError(
                        "La ubicación y fecha del evento ya están ocupadas por otro evento")

            respuesta = self.gestor_json.actualizar(self.tabla,
                        ["titulo_evento", "fecha_hora_evento","descripcion_evento", "ubicacion_evento"],
                        [titulo_evento, fecha_hora_evento.strftime("%Y-%m-%d %H:%M:%S"), descripcion_evento, ubicacion_evento], id_evento)
            return respuesta

        except Exception as e:
            return {"mensaje": str(e), "codigo": 500}

    def delete_event_by_id(self, id_evento: int) -> dict:
        """
        Eliminar un evento por su ID.

        Args:
            id_evento (int): ID del evento a eliminar.

        Returns:
            dict: Mensaje de éxito o error.
            {data: {"campo1": "valor1", "campo2": "valor2", ...}, "codigo": 200} o
            {"mensaje": "Mensaje de error", "codigo": 500}

        Example:
        >>> gestion = GestionEventos()
        >>> respuesta = gestion.delete_event_by_id(1)
        """
        try:
            respuesta = self.gestor_json.borrar(self.tabla, id_evento)
            if respuesta["codigo"] == 500:
                raise ValueError(respuesta["mensaje"])
            
            return respuesta
        except Exception as e:
            return {"mensaje": str(e), "codigo": 500}


class GestorJson:
    def __init__(self):
        self.nombre_archivo = "data_base.json"
        self.archivo_json = self.leer_archivo()

    def leer_archivo(self) -> dict:
        """
        Lee el archivo JSON y lo convierte en un diccionario.

        Returns:
            dict: Diccionario con el contenido del archivo JSON.

        Example:
        >>> gestor = GestorJson()
        >>> archivo = gestor.leer_archivo()
        """
        with open(self.nombre_archivo, "r", encoding="utf-8") as archivo:
            archivo_leido = archivo.read()

        archivo_json = eval(archivo_leido)
        return archivo_json

    def escribir_archivo(self) -> None:
        """
        Escribir el atributo que contiene el JSON en el archivo.

        Returns:
            None

        Example:
        >>> gestor = GestorJson()
        >>> gestor.escribir_archivo()
        """
        with open(self.nombre_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(json.dumps(self.archivo_json, indent=4))

    def crear(self, tabla: str, campos: list[str], valores: list[str]) -> dict:
        """
        Crear un registro en la base de datos (JSON).

        Args:
            tabla (str): Nombre de la tabla.
            campos (list[str]): Lista con los nombres de los campos.
            valores (list[str]): Lista con los valores de los campos.

        Returns:
            dict: Mensaje de éxito o error.
            {"mensaje": "Registro creado", "codigo": 200} o
            {"mensaje": "Mensaje de error", "codigo": 500}

        Example:
        >>> gestor = GestorJson()
        >>> gestor.crear("eventos", 
        >>> ["titulo_evento", "fecha_hora_evento", "descripcion_evento", "ubicacion_evento"],
        >>> ["Evento 1", "2021-10-10", "Descripción del evento 1", "Ubicación del evento 1"])
        """
        try:
            dict_temporal = dict(zip(campos, valores))
            self.archivo_json[tabla].append(dict_temporal)
            self.escribir_archivo()
            return {"mensaje": "Registro creado", "codigo": 200}
        except Exception as e:
            return {"mensaje": str(e), "codigo": 500}

    def buscar(self, tabla: str, id: int = None) -> dict:
        """
        Buscar un registro específico en la base de datos (JSON).
        Si no se especifica un ID, se toma como None y se devuelven todos los registros.

        Args:
            tabla (str): Nombre de la tabla en la base de datos.
            id (int): ID del registro a buscar.

        Returns:
            dict: Registro con mensaje de éxito o mensaje de error.
            {"registro": {"campo1": "valor1", "campo2": "valor2", ...}, "mensaje": "Registro encontrado", "codigo": 200} o
            {"mensaje": "Mensaje de error", "codigo": 500}

        Example:
        >>> gestor = GestorJson()
        """
        try:
            if id is None:
                return {"registro": self.archivo_json[tabla], "mensaje": "Registros encontrados", "codigo": 200}
            elif 0 < id < len(self.archivo_json[tabla]):
                return {"registro": [self.archivo_json[tabla][id]], "mensaje": "Registro encontrado", "codigo": 200}
            else:
                return {"registro": [], "mensaje": "Registro no encontrado", "codigo": 404}
        except Exception as e:
            return {"mensaje": str(e), "codigo": 500}

    def actualizar(self, tabla: str, campos: list[str], valores: list[str], id: int) -> dict:
        """
        Actualizar un registro específico en la base de datos (JSON).

        Args:
            tabla (str): Nombre de la tabla.
            campos (list[str]): Lista con los nombres de los campos.
            valores (list[str]): Lista con los valores de los campos.
            id (int): ID del registro a actualizar.

        Returns:
            dict: Mensaje de éxito o error.
            {"mensaje": "Registro actualizado", "codigo": 200} o
            {"mensaje": "Mensaje de error", "codigo": 500}

        Example:
        >>> gestor = GestorJson()
        >>> gestor.actualizar("eventos", 
        >>> ["titulo_evento", "fecha_hora_evento", "descripcion_evento", "ubicacion_evento"],
        >>> ["Evento 1", "2021-11-10", "Descripción del evento 1", "Ubicación del evento 1"],
        >>> 1)
        """
        try:
            dict_temporal = dict(zip(campos, valores))
            self.archivo_json[tabla][id] = dict_temporal
            self.escribir_archivo()
            return {"mensaje": "Registro actualizado", "codigo": 200}
        except Exception as e:
            return {"mensaje": str(e), "codigo": 500}

    def borrar(self, tabla: str, id: int) -> dict:
        """
        Eliminar un registro específico en la base de datos (JSON).

        Args:
            tabla (str): Nombre de la tabla en la base de datos.
            id (int): ID del registro a eliminar.

        Returns:
            dict: Mensaje de éxito o error.
            {"data": {"campo1": "valor1", "campo2": "valor2", ...}, "codigo": 200} o
            {"mensaje": "Mensaje de error", "codigo": 500}

        Example:
        >>> gestor = GestorJson()
        >>> gestor.borrar("eventos", 1)
        """
        try:
            data_eliminada = self.archivo_json[tabla].pop(id)
            self.escribir_archivo()
            return {"data": data_eliminada, "codigo": 200}
        except Exception as e:
            return {"mensaje": str(e), "codigo": 500}


class GestorUbicacion:
    def __init__(self):
        self.gestor = GestorJson()
        self.tabla = "ubicaciones"

    def get_ubicaciones(self):
        """
        Obtener todas las ubicaciones.

        Returns:
            dict: Registro con mensaje de éxito o mensaje de error.
            {"registro": [{"campo1": "valor1", "campo2": "valor2", ...}, ...], "mensaje": "Registros encontrados", "codigo": 200} o
            {"mensaje": "Mensaje de error", "codigo": 500}
        """
        try:
            respuesta = self.gestor.buscar(self.tabla)
            return respuesta
        except Exception as e:
            return {"mensaje": str(e), "codigo": 500}
        
gestor_eventos = GestionEventos()