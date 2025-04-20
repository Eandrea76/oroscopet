import os
import replicate
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
client = replicate.Client(api_token=REPLICATE_API_TOKEN)

@app.route('/generate', methods=['POST'])
def generate():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    image_path = os.path.join("uploads", image_file.filename)
    os.makedirs("uploads", exist_ok=True)
    image_file.save(image_path)

    try:
        output_url = client.run(
            "cjwbw/cartoon-ga:fd0c6c57cae46991c1697f0d6a7c8ed93be467be4f6d1f49f6322296ccf27eb8",
            input={"image": open(image_path, "rb")}
        )
        return jsonify({"output_url": output_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

