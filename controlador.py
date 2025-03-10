from flask import Flask, request, jsonify
from datetime import datetime
from modelo import gestor_eventos
import flask_cors

app = Flask(__name__)
flask_cors.CORS(app)

@app.route("/events", methods=["POST"])
def post_events():
    """
    Crea un nuevo evento basado en los datos proporcionados en la solicitud JSON.

    Returns:
        Response: Un objeto JSON con un mensaje de éxito o un error y el código de estado HTTP correspondiente.

    JSON Request Body:
        titulo_evento (str): El título del evento.
        fecha_hora_evento (str): La fecha y hora del evento en formato "YYYY-MM-DD HH:MM:SS".
        descripcion_evento (str): La descripción del evento.
        ubicacion_evento (int): El ID de la ubicación del evento.
    JSON Response:
    >>> 200 OK:
    >>>     {"mensaje": "Evento creado"}
    >>> 400 Bad Request:
    >>>     {"error": "Faltan campos: {campos_faltantes}"}
    >>>     ó
    >>>     {"error": "El campo '{campo}' debe ser de tipo {tipo}"}
    >>> 500 Internal Server Error:
    >>>     {"error": "Mensaje de error"}
    """

    try:
        data = request.json
        campos = {"titulo_evento": str, "fecha_hora_evento": str,
                  "descripcion_evento": str, "ubicacion_evento": int}
        data_faltantes = set(campos.keys()) - set(data.keys())
        if data_faltantes:
            return jsonify({"error": f"Faltan campos: {data_faltantes}"}), 400
        for campo, tipo in campos.items():
            if not isinstance(data[campo], tipo):
                return jsonify({"error": f"El campo '{campo}' debe ser de tipo {tipo.__name__}"}), 400
        data["fecha_hora_evento"] = datetime.strptime(
            data["fecha_hora_evento"], "%Y-%m-%d %H:%M:%S")
        respuesta = gestor_eventos.post_events(data["titulo_evento"], data["fecha_hora_evento"],
                                               data["descripcion_evento"], data["ubicacion_evento"])
        if respuesta["codigo"] == 500:
            return jsonify({"error": respuesta["mensaje"]}), 500
        return jsonify({"mensaje": "Evento creado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/events", methods=["GET"])
def get_events():
    """
    Obtiene todos los eventos registrados en la base de datos.

    Returns:
        Response: Un objeto JSON con los eventos registrados en la base de datos y el código de estado HTTP correspondiente.

    JSON Request Body:
        None.
    JSON Response:
    >>> 200 OK:
    >>>     {"data": [
    >>>         {
    >>>             "titulo_evento": str,
    >>>             "fecha_hora_evento": str,
    >>>             "descripcion_evento": str,
    >>>             "ubicacion_evento": int
    >>>         }
    >>>     ]}
    >>> 500 Internal Server Error:
    >>>     {"error": "Mensaje de error"}
    """
    try:
        respuesta = gestor_eventos.get_events()
        if respuesta["codigo"] == 500:
            return jsonify({"error": respuesta["mensaje"]}), 500
        return jsonify({"data": respuesta["registro"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/events/<int:id_evento>", methods=["GET"])
def get_event_by_id(id_evento):
    """
    Obtiene un evento específico basado en su ID.

    Returns:
        Response: Un objeto JSON con el evento solicitado y el código de estado HTTP correspondiente.

    JSON Request Body:
        None.
    JSON Response:
    >>> 200 OK:
    >>>     {"data": {
    >>>         "titulo_evento": str,
    >>>         "fecha_hora_evento": str,
    >>>         "descripcion_evento": str,
    >>>         "ubicacion_evento": int
    >>>     }}
    >>> 500 Internal Server Error:
    >>>     {"error": "Mensaje de error"}   
    """
    try:
        respuesta = gestor_eventos.get_event_by_id(id_evento)
        if respuesta["codigo"] == 500:
            return jsonify({"error": respuesta["mensaje"]}), 500
        return jsonify({"data": respuesta["registro"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/events/<int:id_evento>", methods=["PUT"])
def put_event_by_id(id_evento):
    """
    Actualiza un evento específico basado en su ID y los datos proporcionados en la solicitud JSON.

    Returns:
        Response: Un objeto JSON con un mensaje de éxito o un error y el código de estado HTTP correspondiente.

    JSON Request Body:
        titulo_evento (str): El título del evento.
        fecha_hora_evento (str): La fecha y hora del evento en formato "YYYY-MM-DD HH:MM:SS".
        descripcion_evento (str): La descripción del evento.
        ubicacion_evento (int): El ID de la ubicación del evento.
    JSON Response:
    >>> 200 OK:
    >>>     {"mensaje": "Evento {titulo_evento} actualizado"}
    >>> 400 Bad Request:
    >>>     {"error": "Faltan campos: {campos_faltantes}"}
    >>>     ó
    >>>     {"error": "El campo '{campo}' debe ser de tipo {tipo}"}
    >>> 500 Internal Server Error:
    >>>     {"error": "Mensaje de error"}
    """
    try:
        data = request.json
        campos = {"titulo_evento": str, "fecha_hora_evento": str,
                  "descripcion_evento": str, "ubicacion_evento": int}
        data_faltantes = set(campos.keys()) - set(data.keys())
        if data_faltantes:
            return jsonify({"error": f"Faltan campos: {data_faltantes}"}), 400
        for campo, tipo in campos.items():
            if not isinstance(data[campo], tipo):
                return jsonify({"error": f"El campo '{campo}' debe ser de tipo {tipo.__name__}"}), 400
        data["fecha_hora_evento"] = datetime.strptime(
            data["fecha_hora_evento"], "%Y-%m-%d %H:%M:%S")
        respuesta = gestor_eventos.put_event_by_id(data["titulo_evento"], data["fecha_hora_evento"],
                                                   data["descripcion_evento"], data["ubicacion_evento"], id_evento)
        if respuesta["codigo"] == 500:
            return jsonify({"error": respuesta["mensaje"]}), 500
        return jsonify({"mensaje": f"Evento ({data['titulo_evento']}) actualizado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/events/<int:id_evento>", methods=["DELETE"])
def delete_event_by_id(id_evento):
    """
    Elimina un evento específico basado en su ID.

    Returns:
        Response: Un objeto JSON con un mensaje de éxito o un error y el código de estado HTTP correspondiente.

    JSON Request Body:
        None.
    JSON Response:
    >>> 200 OK:
    >>>     {"mensaje": "Evento {titulo_evento} eliminado"}
    >>> 500 Internal Server Error:
    >>>     {"error": "Mensaje de error"}
    """
    try:
        respuesta = gestor_eventos.delete_event_by_id(id_evento)
        if respuesta["codigo"] == 500:
            return jsonify({"error": respuesta["mensaje"]}), 500
        return jsonify({"mensaje": f"Evento ({respuesta['data']['titulo_evento']}) eliminado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/locations", methods=["GET"])
def get_locations():
    """
    Obtenemos todas las ubicaciones registradas en la base de datos.

    Returns:
        Response: Un objeto JSON con las ubicaciones registradas en la base de datos y el código de estado HTTP correspondiente.

    JSON Request Body:
        None.
    JSON Response:
    >>> 200 OK:
    >>>     {"data": [
    >>>         {
    >>>             "nombre_ubicacion": str,
    >>>             "direccion_ubicacion": str,
    >>>         }
    >>>     ]}
    >>> 500 Internal Server Error:
    >>>     {"error": "Mensaje de error"}
    """
    try:
        respuesta = gestor_eventos.gestor_ubicacion.get_ubicaciones()
        if respuesta["codigo"] == 500:
            return jsonify({"error": respuesta["mensaje"]}), 500
        return jsonify({"data": respuesta["registro"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
