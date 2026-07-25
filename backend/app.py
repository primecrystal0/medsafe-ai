"""
Flask API — single endpoint that ties OCR, LLM advice, and DB storage together.
"""
import logging
import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from config import config
from db_service import save_scan, get_recent_scans
from llm_service import LLMError, get_advice
from ocr_service import OCRError, extract_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)


@app.route("/api/scan", methods=["POST"])
def scan():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files["image"]
    age = request.form.get("age", type=int, default=0)
    conditions = request.form.get("conditions", default="")

    image_bytes = image_file.read()

    try:
        label_text = extract_text(image_bytes)
    except OCRError as exc:
        return jsonify({"error": str(exc)}), 422

    try:
        advice = get_advice(label_text, age, conditions)
    except LLMError as exc:
        return jsonify({"error": str(exc)}), 502

    scan_id = save_scan(
        label_text=label_text,
        advice=advice,
        source="upload",
        age=age,
        conditions=conditions,
    )

    return jsonify({
        "id": scan_id,
        "label_text": label_text,
        "advice": advice,
    })


@app.route("/api/history", methods=["GET"])
def history():
    limit = request.args.get("limit", type=int, default=20)
    return jsonify(get_recent_scans(limit))


if __name__ == "__main__":
    port = int(os.getenv("PORT", config.BACKEND_PORT))
    app.run(host="0.0.0.0", port=port, debug=config.DEBUG)