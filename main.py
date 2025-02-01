import google.generativeai as genai
from dotenv import load_dotenv
import os
import pyttsx3
load_dotenv()

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

GEMINI_API_KEY = os.getenv("AIzaSyAn-jNSjSLioNp4ykAry6QTIypZzKPUb_M")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(
    [
        "Describe the image to a blind person for safety, from their perspective. Be specific with directions and the distance for where objects are. Avoid unneccessary details. This needs to be a maximum of 20 words.",
        {"mime_type": "image/jpeg", "data": image_data
    }
    ]
)
print(response.text)

engine = pyttsx3.init()

voices = engine.getProperty('voices')

engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 210)
rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)
#engine.say(response.text)

engine.save_to_file(response.text , 'textToVoice.mp3')
engine.runAndWait()

