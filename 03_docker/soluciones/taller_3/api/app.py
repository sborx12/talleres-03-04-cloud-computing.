
import os
from flask import Flask, jsonify
import psycopg
from psycopg.rows import dict_row

app = Flask(__name__)

INSTANCE = os.getenv("INSTANCE", "api-local")

def conectar_db():
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        row_factory=dict_row
    )

@app.get("/products")
def obtener_productos():
    with conectar_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, price FROM products ORDER BY id"
            )
            productos = cursor.fetchall()

    return jsonify({
        "served_by": INSTANCE,
        "products": [
            {
                "id": producto["id"],
                "name": producto["name"],
                "price": float(producto["price"])
            }
            for producto in productos
        ]
    })

@app.get("/products/<int:id>")
def obtener_producto(id):
    with conectar_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, price FROM products WHERE id = %s",
                (id,)
            )
            producto = cursor.fetchone()

    if producto is None:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify({
        "served_by": INSTANCE,
        "product": {
            "id": producto["id"],
            "name": producto["name"],
            "price": float(producto["price"])
        }
    })

from flask import request

@app.post("/products")
def crear_producto():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({"error": "Se requiere un JSON valido"}), 400

    nombre = datos.get("name")
    precio = datos.get("price")

    if not isinstance(nombre, str) or not nombre.strip():
        return jsonify({"error": "Nombre invalido"}), 400

    try:
        from decimal import Decimal
        precio = Decimal(str(precio))

        if not precio.is_finite() or precio < 0:
            raise ValueError()
    except (ValueError, TypeError, ArithmeticError):
        return jsonify({"error": "Precio invalido"}), 400

    with conectar_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO products (name, price)
                VALUES (%s, %s)
                RETURNING id, name, price
                """,
                (nombre.strip(), precio)
            )
            producto = cursor.fetchone()

    return jsonify({
        "served_by": INSTANCE,
        "product": {
            "id": producto["id"],
            "name": producto["name"],
            "price": float(producto["price"])
        }
    }), 201


@app.put("/products/<int:id>")
def actualizar_producto(id):
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({"error": "JSON invalido"}), 400

    nombre = datos.get("name")
    precio = datos.get("price")

    if not isinstance(nombre, str) or not nombre.strip():
        return jsonify({"error": "Nombre invalido"}), 400

    try:
        from decimal import Decimal
        precio = Decimal(str(precio))

        if not precio.is_finite() or precio < 0:
            raise ValueError()
    except (ValueError, TypeError, ArithmeticError):
        return jsonify({"error": "Precio invalido"}), 400

    with conectar_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE products
                SET name = %s, price = %s
                WHERE id = %s
                RETURNING id, name, price
                """,
                (nombre.strip(), precio, id)
            )
            producto = cursor.fetchone()

    if producto is None:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify({
        "served_by": INSTANCE,
        "product": {
            "id": producto["id"],
            "name": producto["name"],
            "price": float(producto["price"])
        }
    })


@app.delete("/products/<int:id>")
def eliminar_producto(id):
    with conectar_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM products
                WHERE id = %s
                RETURNING id, name
                """,
                (id,)
            )
            producto = cursor.fetchone()

    if producto is None:
        return jsonify({
            "error": "Producto no encontrado"
        }), 404

    return jsonify({
        "served_by": INSTANCE,
        "message": "Producto eliminado correctamente",
        "deleted_product": producto
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
