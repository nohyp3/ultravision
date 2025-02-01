import os
from flask import Flask, request, Response, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import os
import pyttsx3

bool = False
while bool == False:
    filename = "dog.jpg"
    try:
        with open(filename, "rb") as image_file:
            image_data = image_file.read()
            bool = True
    except:
        print ("file not found. try again")

# Replace with your image path

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)


def voiceModule (description):

    engine = pyttsx3.init()

    voices = engine.getProperty('voices')

    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 210)
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    engine.say(description.text)
    engine.runAndWait()
    engine.save_to_file(description.text, 'textToVoice.mp3')


#engine.say(response.text)



app = Flask(__name__)

# Store the latest frame
latest_frame = None

def process_image_with_gemini(image_data):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        [
            "Describe the image to a blind person for safety. Avoid unnecessary details. This needs to be a maximum of 20 words.",
            {"mime_type": "image/jpeg", "data": image_data},
        ]
    )
    return response.text

@app.route('/upload', methods=['POST'])
def upload_image():
    global latest_frame
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    latest_frame = image_file.read()
    return jsonify({"status": "Image received"}), 200

@app.route('/stream')
def stream():
    def generate():
        global latest_frame
        while True:
            if latest_frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + latest_frame + b'\r\n\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '<html><body><h1>ESP32 Camera Stream</h1><img src="/stream" /></body></html>'

@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    image_data = image_file.read()

    try:
        description = process_image_with_gemini(image_data)
        voiceModule(description)

        return jsonify({"description": description}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)