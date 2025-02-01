import os
from flask import Flask, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)

def process_image_with_gemini(image_data):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        [
            "Describe the image to a blind person for safety. Avoid unnecessary details. This needs to be a maximum of 20 words.",
            {"mime_type": "image/jpeg", "data": image_data},
        ]
    )
    return response.text

@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    image_data = image_file.read()

    try:
        description = process_image_with_gemini(image_data)
        return jsonify({"description": description}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)