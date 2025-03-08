from flask import Flask, request, jsonify
from datetime import date

app = Flask(__name__)

@app.route("/events", methods=["POST"])
def post_events():
    try:
        data = request.json
        campos = {"titulo_evento": str, "fecha_hora_evento": date,
               "descripcion_evento": str, "ubicacion_evento": str}
        data_faltantes = set(campos.keys()) - set(data.keys()) 
        if data_faltantes:
            return jsonify({"error": f"Faltan campos: {data_faltantes}"}), 400
        for campo, tipo in campos.items():
            if not isinstance(data[campo], tipo):
                return jsonify({"error": f"El campo '{campo}' debe ser de tipo {tipo.__name__}"}), 400
        return jsonify({"mensaje": "Evento creado"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/events", methods=["GET"])
def get_events():
    try:
        return jsonify({"mensaje": "Eventos obtenidos"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/events/<int:id_evento>", methods=["GET"])
def get_event_by_id(id_evento):
    try:
        return jsonify({"mensaje": f"Evento {id_evento} obtenido"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/events/<int:id_evento>", methods=["PUT"])
def put_event_by_id(id_evento):
    try:
        data = request.json
        campos = {"titulo_evento": str, "fecha_hora_evento": date,
               "descripcion_evento": str, "ubicacion_evento": str}
        data_faltantes = set(campos.keys()) - set(data.keys())
        if data_faltantes:
            return jsonify({"error": f"Faltan campos: {data_faltantes}"}), 400
        for campo, tipo in campos.items():
            if not isinstance(data[campo], tipo):
                return jsonify({"error": f"El campo '{campo}' debe ser de tipo {tipo.__name__}"}), 400
        return jsonify({"mensaje": f"Evento {id_evento} actualizado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/events/<int:id_evento>", methods=["DELETE"])
def delete_event_by_id(id_evento):
    try:
        return jsonify({"mensaje": f"Evento {id_evento} eliminado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)