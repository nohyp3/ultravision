import os
import google.generativeai as genai
from dotenv import load_dotenv
import pyttsx3
import base64


# Configure Gemini API
#GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key="GEMINI_API_KEY")

mp3_file_path = "assets/textToVoice.mp3"

def process_image_with_gemini(image_data):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        [
            "Describe the image to a blind person for safety, from their perspective. Be specific with directions and the distance for where objects are. Avoid unnecessary details. Tell the person if it is safe or not to proceed forward. This needs to be a maximum of 20 words.",
            {"mime_type": "image/jpeg", "data": image_data},
        ]
    )
    return response.text


#voice module configuring. Saves mp3.
def voice_module(description):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 210)
    engine.say(description)
    engine.runAndWait()
    engine.save_to_file(description, mp3_file_path)



#main driver function. receives image data.
def test(image_data):

    try:
        description = process_image_with_gemini(image_data)
        print(description)

        voice_module(description)

    except Exception as e:
        print(f"An error occurred: {e}")



# Load environment variables from .env file
load_dotenv()

#test image file. All images are in assets folder.
image_path = "assets/lecturehall.jpg"


#turns image file into binary so that API can properly use it
with open(image_path, "rb") as imgfile:
    image_data = imgfile.read()


test (image_data)
