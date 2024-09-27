import os
import uuid
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from utils.text_recognition import TextRecognizer
from utils.barcode_detection import BarcodeDetector
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def process_file(file, processor_func):
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        log_id = str(uuid.uuid4().int)
        filename = secure_filename(f"{log_id}.png")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        results = processor_func(file_path)

        response = {
            "log_id": log_id,
            "result_num": len(results),
            "results": results
        }

        json_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{log_id}.json")
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(response, json_file, ensure_ascii=False, indent=4)

        return jsonify(response)

    return jsonify({"error": "File type not allowed"}), 400


@app.route('/ocr', methods=['POST'])
def ocr():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    def process_ocr(file_path):
        recognizer = TextRecognizer()
        ocr_results = recognizer.recognize_text_from_image(file_path)
        return [
            {
                "words": text,
                "location": {
                    "top": bbox[1],
                    "left": bbox[0],
                    "width": bbox[2],
                    "height": bbox[3]
                }
            }
            for text, bbox in ocr_results
        ]

    return process_file(file, process_ocr)


@app.route('/barcode', methods=['POST'])
def barcode():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    def process_barcode(file_path):
        detector = BarcodeDetector()
        barcode_results = detector.detect_barcodes_from_image(file_path)
        return [
            {
                "value": value,
                "symbology": symbology,
                "location": {
                    "top": bbox[1],
                    "left": bbox[0],
                    "width": bbox[2],
                    "height": bbox[3]
                }
            }
            for value, symbology, bbox in barcode_results
        ]

    return process_file(file, process_barcode)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=False)
