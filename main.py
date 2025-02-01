import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

bool = False
while bool == False:
    filename = "street_sign.jpg"
    try:
        with open(filename, "rb") as image_file:
            image_data = image_file.read()
            bool = True
    except:
        print ("file not found. try again")

# Replace with your image path

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
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

