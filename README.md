# event_management
Desarrolla una aplicación web para la gestión de eventos, donde los usuarios puedan crear, leer, actualizar y eliminar eventos.

## Documentación API

### POST /events
Crea un nuevo evento basado en los datos proporcionados en la solicitud JSON.

#### Request Body (JSON)
- `titulo_evento` (str): El título del evento.
- `fecha_hora_evento` (str): La fecha y hora del evento en formato "YYYY-MM-DD HH:MM:SS".
- `descripcion_evento` (str): La descripción del evento.
- `ubicacion_evento` (int): El ID de la ubicación del evento.

#### Responses
- **200 OK**: `{"mensaje": "Evento creado"}`
- **400 Bad Request**: `{"error": "Faltan campos: {campos_faltantes}"}` ó `{"error": "El campo '{campo}' debe ser de tipo {tipo}"}`
- **500 Internal Server Error**: `{"error": "Mensaje de error"}`

### GET /events
Obtiene todos los eventos registrados en la base de datos.

#### Request Body
None.

#### Responses
- **200 OK**: `{"data": [{"titulo_evento": str, "fecha_hora_evento": str, "descripcion_evento": str, "ubicacion_evento": int, "id_evento": int}]}`
- **500 Internal Server Error**: `{"error": "Mensaje de error"}`

### GET /events/<int:id_evento>
Obtiene un evento específico basado en su ID.

#### Request Body
None.

#### Responses
- **200 OK**: `{"data": {"titulo_evento": str, "fecha_hora_evento": str, "descripcion_evento": str, "ubicacion_evento": int, "id_evento": int}}`
- **500 Internal Server Error**: `{"error": "Mensaje de error"}`

### PUT /events/<int:id_evento>
Actualiza un evento específico basado en su ID y los datos proporcionados en la solicitud JSON.

#### Request Body (JSON)
- `titulo_evento` (str): El título del evento.
- `fecha_hora_evento` (str): La fecha y hora del evento en formato "YYYY-MM-DD HH:MM:SS".
- `descripcion_evento` (str): La descripción del evento.
- `ubicacion_evento` (int): El ID de la ubicación del evento.

#### Responses
- **200 OK**: `{"mensaje": "Evento {titulo_evento} actualizado"}`
- **400 Bad Request**: `{"error": "Faltan campos: {campos_faltantes}"}` ó `{"error": "El campo '{campo}' debe ser de tipo {tipo}"}`
- **500 Internal Server Error**: `{"error": "Mensaje de error"}`

### DELETE /events/<int:id_evento>
Elimina un evento específico basado en su ID.

#### Request Body
None.

#### Responses
- **200 OK**: `{"mensaje": "Evento {titulo_evento} eliminado"}`
- **500 Internal Server Error**: `{"error": "Mensaje de error"}`
