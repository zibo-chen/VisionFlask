import os
import uuid
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from utils.text_recognition import TextRecognizer
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/ocr', methods=['POST'])
def ocr():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        log_id = str(uuid.uuid4().int)
        filename = secure_filename(f"{log_id}.png")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        recognizer = TextRecognizer()
        results = recognizer.recognize_text_from_image(file_path)

        response = {
            "log_id": log_id,
            "words_result_num": len(results),
            "words_result": []
        }

        for text, bbox in results:
            response["words_result"].append(
                {
                    "words": text,
                    "location": {
                        "top": bbox[1],
                        "left": bbox[0],
                        "width": bbox[2],
                        "height": bbox[3]
                    }
                }
            )

        json_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{log_id}.json")
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(response, json_file, ensure_ascii=False, indent=4)

        return jsonify(response)

    return jsonify({"error": "File type not allowed"}), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=False)
