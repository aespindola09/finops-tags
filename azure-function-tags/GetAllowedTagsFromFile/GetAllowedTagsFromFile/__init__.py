import logging
import azure.functions as func
import json
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Solicitud recibida para obtener el diccionario de tags")

    tags_file = os.path.join(os.path.dirname(__file__), "tags.json")
    try:
        with open(tags_file, "r", encoding="utf-8") as f:
            tags = json.load(f)
        return func.HttpResponse(
            json.dumps(tags, indent=2),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error al leer el archivo de tags: {e}")
        return func.HttpResponse(
            "Error interno al leer los tags",
            status_code=500
        )