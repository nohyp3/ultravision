🔍 UltraVision

UltraVision is a robotic assistant designed to help the visually impaired navigate their surroundings. The system integrates an ESP32-CAM, ultrasonic sensors, and Google Gemini AI to provide real-time scene descriptions and obstacle detection via a Flask web server.

🚀 Features

✅ Live video streaming from the ESP32-CAM
✅ AI-powered scene descriptions using Google Gemini API
✅ Ultrasonic sensor-based obstacle detection
✅ Real-time text-to-speech (TTS) using pyttsx3
✅ Web-based interface for image and audio playback

🛠️ Requirements

Hardware:

ESP32-CAM module

Ultrasonic sensors (HC-SR04 or similar)

Speaker (optional for voice output)

Power supply

Software:

Python 3.7+

Flask

Google Generative AI

pyttsx3 (TTS engine)

dotenv (for managing API keys)

🔧 Installation & Setup

1️⃣ ESP32-CAM Setup

Open cameraWebServer.ino in Arduino IDE.

Update Wi-Fi credentials:

const char* ssid     = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverUrl = "http://YOUR_PC_IP:5000/upload";

Select AI Thinker ESP32-CAM as the board and upload the code.

Open the Serial Monitor to verify the connection.

2️⃣ Flask Server Setup

Clone the repository:

git clone https://github.com/yourusername/VisionAssist.git
cd VisionAssist/server

Set up the Python virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install dependencies:

pip install -r requirements.txt

Create a .env file in the server directory and add your Google Gemini API key:

GEMINI_API_KEY=your_gemini_api_key

Run the Flask server:

python main.py

3️⃣ Accessing the System

Navigate to http://<your_server_ip>:5000 in a web browser to view the live stream and interact with the system.

The Flask server processes images and provides audio descriptions for users.

📂 File Structure

esp32/cameraWebServer.ino → ESP32-CAM sketch for image capture & upload.

server/main.py → Flask server for image processing and audio generation.

server/.env → API keys (ignored by Git).

server/requirements.txt → Python dependencies.

🔌 API Endpoints

/upload → Upload an image from ESP32-CAM.

/stream → Live video feed.

/ → Web UI for live streaming & audio playback.

/audio → Serve the generated audio file.

/process-image → AI-powered image processing and voice description.

🔮 Future Enhancements

🚀 Voice command support for hands-free interaction🚀 Improved AI accuracy with fine-tuned models🚀 GPS integration for enhanced navigation
