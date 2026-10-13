
import os

from flask import request

from app import app


@app.before_request
def verificar_origen():
    if request.path != "/api/investigar":
        return None

    origen = request.headers.get("Origin")
    origen_permitido = os.getenv("FRONTEND_ORIGIN", "")

    if origen and origen != origen_permitido:
        return {"error": "Origen no permitido"}, 403

    if request.method == "OPTIONS":
        return "", 204

    return None


@app.after_request
def configurar_cors(respuesta):
    origen = request.headers.get("Origin")
    origen_permitido = os.getenv("FRONTEND_ORIGIN", "")

    if origen and origen == origen_permitido:
        respuesta.headers["Access-Control-Allow-Origin"] = origen
        respuesta.headers["Vary"] = "Origin"
        respuesta.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        respuesta.headers["Access-Control-Allow-Headers"] = "Content-Type"

    return respuesta
