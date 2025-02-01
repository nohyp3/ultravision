import google.generativeai as genai

bool = False
while bool == False:
    filename = input("input image file name:")
    try:
        with open(filename, "rb") as image_file:
            image_data = image_file.read()
            bool = True
    except:
        print ("file not found. try again")

# Replace with your image path

genai.configure(api_key="AIzaSyAn-jNSjSLioNp4ykAry6QTIypZzKPUb_M")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(
    [
        "Describe the image to a blind person for safety, from their perspective. Be specific with directions and the distance for where objects are. Avoid unneccessary details. This needs to be a maximum of 20 words.",
        {"mime_type": "image/jpeg", "data": image_data
    }
    ]
)
print(response.text)

