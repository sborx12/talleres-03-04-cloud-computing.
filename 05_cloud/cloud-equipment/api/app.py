
import os
import uuid
from pathlib import Path

import boto3
import psycopg2
from botocore.exceptions import BotoCoreError, ClientError
from flask import Flask, jsonify, request
from psycopg2.extras import RealDictCursor
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}


# CONEXIÓN A POSTGRESQL

def connect_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "equipment"),
        user=os.getenv("DB_USER", "equipment"),
        password=os.environ["DB_PASSWORD"]
    )


def query_all(sql, params=()):
    with connect_db() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params)
            return [dict(row) for row in cursor.fetchall()]


def query_one(sql, params=()):
    with connect_db() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params)
            row = cursor.fetchone()
            return dict(row) if row else None


def payload():
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else None


def validation_error(message):
    return jsonify({"error": message}), 400


def database_error(label, error):
    app.logger.error("%s: %s", label, type(error).__name__)
    return jsonify({"error": "Error de base de datos"}), 500


# HEALTH CHECK

@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "equipment-api",
        "version": "3.0"
    })


# EMPLEADOS

@app.get("/empleados")
def employees():
    try:
        rows = query_all("""
            SELECT id,
                   name AS nombre,
                   email AS correo,
                   department AS departamento
            FROM employees
            ORDER BY id
        """)
        return jsonify(rows)

    except psycopg2.Error as error:
        return database_error("Listar empleados", error)


@app.get("/empleados/<int:employee_id>")
def employee(employee_id):
    try:
        row = query_one("""
            SELECT id,
                   name AS nombre,
                   email AS correo,
                   department AS departamento
            FROM employees
            WHERE id = %s
        """, (employee_id,))

        if row is None:
            return jsonify({"error": "Empleado no encontrado"}), 404

        return jsonify(row)

    except psycopg2.Error as error:
        return database_error("Consultar empleado", error)


@app.post("/empleados")
def add_employee():
    data = payload()

    if data is None:
        return validation_error("Se requiere un objeto JSON")

    name = data.get("nombre")
    email = data.get("correo")
    department = data.get("departamento")

    if not isinstance(name, str) or not name.strip() or len(name.strip()) > 100:
        return validation_error("Nombre obligatorio (máximo 100 caracteres)")

    if not isinstance(email, str) or "@" not in email or len(email.strip()) > 150:
        return validation_error("Correo inválido")

    if department is not None and (
        not isinstance(department, str) or len(department) > 100
    ):
        return validation_error("Departamento inválido")

    try:
        with connect_db() as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO employees (name, email, department)
                    VALUES (%s, %s, %s)
                    RETURNING id,
                              name AS nombre,
                              email AS correo,
                              department AS departamento
                """, (name.strip(), email.strip(), department))

                row = dict(cursor.fetchone())

        return jsonify(row), 201

    except psycopg2.errors.UniqueViolation:
        return jsonify({"error": "Correo duplicado"}), 409

    except psycopg2.Error as error:
        return database_error("Crear empleado", error)


# EQUIPOS

EQUIPMENT_SELECT = """
    SELECT id,
           internal_code AS codigo_interno,
           type AS tipo,
           brand AS marca,
           model AS modelo,
           serial_number AS numero_serie,
           status AS estado,
           acquisition_date AS fecha_adquisicion,
           employee_id AS empleado_id
    FROM equipment
"""


@app.get("/equipos")
def equipment_list():
    try:
        return jsonify(query_all(EQUIPMENT_SELECT + " ORDER BY id"))

    except psycopg2.Error as error:
        return database_error("Listar equipos", error)


@app.get("/equipos/<int:equipment_id>")
def equipment_detail(equipment_id):
    try:
        row = query_one(
            EQUIPMENT_SELECT + " WHERE id = %s",
            (equipment_id,)
        )

        if row is None:
            return jsonify({"error": "Equipo no encontrado"}), 404

        return jsonify(row)

    except psycopg2.Error as error:
        return database_error("Consultar equipo", error)


@app.post("/equipos")
def add_equipment():
    data = payload()

    if data is None:
        return validation_error("Se requiere un objeto JSON")

    code = data.get("codigo_interno")
    item_type = data.get("tipo")

    if not isinstance(code, str) or not code.strip() or len(code) > 50:
        return validation_error("Código interno obligatorio, máximo 50 caracteres")

    if not isinstance(item_type, str) or not item_type.strip() or len(item_type) > 50:
        return validation_error("Tipo obligatorio, máximo 50 caracteres")

    state = data.get("estado", "DISPONIBLE")

    if state != "DISPONIBLE":
        return validation_error("Los equipos nuevos deben registrarse como DISPONIBLE")

    for key, limit in [
        ("marca", 80),
        ("modelo", 80),
        ("numero_serie", 100)
    ]:
        if data.get(key) is not None and (
            not isinstance(data[key], str) or len(data[key]) > limit
        ):
            return validation_error(f"{key} inválido")

    try:
        with connect_db() as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO equipment (
                        internal_code,
                        type,
                        brand,
                        model,
                        serial_number,
                        status
                    )
                    VALUES (%s, %s, %s, %s, %s, 'DISPONIBLE')
                    RETURNING id
                """, (
                    code.strip(),
                    item_type.strip(),
                    data.get("marca"),
                    data.get("modelo"),
                    data.get("numero_serie")
                ))

                item_id = cursor.fetchone()["id"]

        return jsonify({
            "id": item_id,
            "codigo_interno": code.strip(),
            "estado": "DISPONIBLE"
        }), 201

    except psycopg2.errors.UniqueViolation:
        return jsonify({
            "error": "Código interno o número de serie duplicado"
        }), 409

    except psycopg2.Error as error:
        return database_error("Crear equipo", error)


@app.put("/equipos/<int:equipment_id>")
def update_equipment(equipment_id):
    data = payload()

    if data is None:
        return validation_error("Se requiere un objeto JSON")

    field_map = {
        "codigo_interno": "internal_code",
        "tipo": "type",
        "marca": "brand",
        "modelo": "model",
        "numero_serie": "serial_number"
    }

    values = {
        key: value
        for key, value in data.items()
        if key in field_map
    }

    if not values:
        return validation_error(
            "Incluye un campo editable: codigo_interno, tipo, marca, modelo o numero_serie"
        )

    limits = {
        "codigo_interno": 50,
        "tipo": 50,
        "marca": 80,
        "modelo": 80,
        "numero_serie": 100
    }

    for key, value in values.items():
        if value is not None and (
            not isinstance(value, str)
            or not value.strip()
            or len(value) > limits[key]
        ):
            return validation_error(f"{key} inválido")

        if key in ("codigo_interno", "tipo") and value is None:
            return validation_error(f"{key} obligatorio")

    clause = ", ".join(
        f"{field_map[key]} = %s"
        for key in values
    )

    try:
        with connect_db() as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    f"UPDATE equipment SET {clause} WHERE id = %s RETURNING id",
                    (*values.values(), equipment_id)
                )

                row = cursor.fetchone()

        if not row:
            return jsonify({"error": "Equipo no encontrado"}), 404

        return equipment_detail(equipment_id)

    except psycopg2.errors.UniqueViolation:
        return jsonify({
            "error": "Código interno o número de serie duplicado"
        }), 409

    except psycopg2.Error as error:
        return database_error("Actualizar equipo", error)


# ASIGNACIÓN DE EQUIPOS

@app.post("/equipos/<int:equipment_id>/asignar")
def assign_equipment(equipment_id):
    data = payload()

    if (
        data is None
        or type(data.get("empleado_id")) is not int
        or data["empleado_id"] < 1
    ):
        return validation_error(
            "empleado_id debe ser un entero positivo"
        )

    employee_id = data["empleado_id"]

    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT status
                    FROM equipment
                    WHERE id = %s
                    FOR UPDATE
                """, (equipment_id,))

                row = cursor.fetchone()

                if row is None:
                    return jsonify({
                        "error": "Equipo no encontrado"
                    }), 404

                if row[0] != "DISPONIBLE":
                    return jsonify({
                        "error": "Equipo no disponible"
                    }), 409

                cursor.execute("""
                    SELECT 1
                    FROM employees
                    WHERE id = %s
                """, (employee_id,))

                if cursor.fetchone() is None:
                    return jsonify({
                        "error": "Empleado no encontrado"
                    }), 404

                cursor.execute("""
                    UPDATE equipment
                    SET employee_id = %s,
                        status = 'ASIGNADO'
                    WHERE id = %s
                """, (employee_id, equipment_id))

                cursor.execute("""
                    INSERT INTO assignments (
                        equipment_id,
                        employee_id
                    )
                    VALUES (%s, %s)
                """, (equipment_id, employee_id))

        return jsonify({
            "equipo_id": equipment_id,
            "empleado_id": employee_id,
            "estado": "ASIGNADO"
        }), 200

    except psycopg2.Error as error:
        return database_error("Asignar equipo", error)


# MANTENIMIENTOS

@app.post("/equipos/<int:equipment_id>/mantenimientos")
def add_maintenance(equipment_id):
    data = payload()

    if data is None:
        return validation_error("Se requiere un objeto JSON")

    kind = data.get("tipo")
    description = data.get("descripcion")
    cost = data.get("costo", 0)

    if not isinstance(kind, str) or not kind.strip() or len(kind) > 50:
        return validation_error("Tipo de mantenimiento obligatorio")

    if not isinstance(description, str) or not description.strip():
        return validation_error("Descripción obligatoria")

    try:
        cost_number = float(cost)

        if not (0 <= cost_number <= 9999999999):
            return validation_error("Costo fuera de rango")

    except (TypeError, ValueError):
        return validation_error("Costo numérico inválido")

    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 1 FROM equipment WHERE id = %s
                """, (equipment_id,))

                if cursor.fetchone() is None:
                    return jsonify({
                        "error": "Equipo no encontrado"
                    }), 404

                cursor.execute("""
                    INSERT INTO maintenance (
                        equipment_id,
                        type,
                        description,
                        cost
                    )
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (
                    equipment_id,
                    kind.strip(),
                    description.strip(),
                    cost_number
                ))

                maintenance_id = cursor.fetchone()[0]

        return jsonify({
            "id": maintenance_id,
            "equipo_id": equipment_id,
            "tipo": kind.strip(),
            "descripcion": description.strip(),
            "costo": cost_number
        }), 201

    except psycopg2.Error as error:
        return database_error("Registrar mantenimiento", error)


# HISTORIAL DE EQUIPOS

@app.get("/equipos/<int:equipment_id>/historial")
def equipment_history(equipment_id):
    try:
        item = query_one("""
            SELECT internal_code
            FROM equipment
            WHERE id = %s
        """, (equipment_id,))

        if item is None:
            return jsonify({
                "error": "Equipo no encontrado"
            }), 404

        events = query_all("""
            SELECT a.assigned_at AS fecha,
                   'Asignación' AS evento,
                   e.name AS detalle
            FROM assignments a
            JOIN employees e
                ON e.id = a.employee_id
            WHERE a.equipment_id = %s

            UNION ALL

            SELECT m.maintenance_date AS fecha,
                   'Mantenimiento' AS evento,
                   concat(
                       coalesce(m.type, ''),
                       ': ',
                       coalesce(m.description, '')
                   ) AS detalle
            FROM maintenance m
            WHERE m.equipment_id = %s

            ORDER BY fecha, evento
        """, (equipment_id, equipment_id))

        return jsonify({
            "equipo": item["internal_code"],
            "historial": events
        })

    except psycopg2.Error as error:
        return database_error("Consultar historial", error)


# DOCUMENTOS EN AMAZON S3

@app.post("/equipos/<int:equipment_id>/documentos")
def add_document(equipment_id):
    uploaded = request.files.get("file")

    if not uploaded or not uploaded.filename:
        return validation_error(
            "Adjunta un archivo en el campo file"
        )

    original_name = secure_filename(uploaded.filename)
    extension = Path(original_name).suffix.lower()

    if not original_name or extension not in ALLOWED_EXTENSIONS:
        return validation_error(
            "Solo se permiten PDF, PNG y JPG"
        )

    bucket = os.getenv("S3_BUCKET")

    if not bucket:
        return jsonify({
            "error": "S3 no configurado"
        }), 500

    key = (
        f"equipos/{equipment_id}/"
        f"{uuid.uuid4().hex}{extension}"
    )

    try:
        exists = query_one("""
            SELECT id
            FROM equipment
            WHERE id = %s
        """, (equipment_id,))

        if exists is None:
            return jsonify({
                "error": "Equipo no encontrado"
            }), 404

        s3 = boto3.client(
            "s3",
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )

        s3.upload_fileobj(
            uploaded.stream,
            bucket,
            key,
            ExtraArgs={
                "ContentType": (
                    uploaded.mimetype
                    or "application/octet-stream"
                )
            }
        )

    except (BotoCoreError, ClientError):
        app.logger.exception("Error al subir archivo a S3")

        return jsonify({
            "error": "No se pudo cargar el archivo a S3"
        }), 502

    except psycopg2.Error as error:
        return database_error("Validar equipo", error)

    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO documents (
                        equipment_id,
                        file_name,
                        s3_key
                    )
                    VALUES (%s, %s, %s)
                    RETURNING id
                """, (
                    equipment_id,
                    original_name,
                    key
                ))

                document_id = cursor.fetchone()[0]

        return jsonify({
            "id": document_id,
            "equipo_id": equipment_id,
            "archivo": original_name,
            "s3_key": key
        }), 201

    except psycopg2.Error as error:
        app.logger.exception(
            "Error al registrar documento; objeto S3 sin metadatos: %s",
            key
        )

        return database_error("Registrar documento", error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
