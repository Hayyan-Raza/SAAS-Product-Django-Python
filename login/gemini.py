from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def generate_resume():  
    key = GEMINI_API_KEY

    client = genai.Client(api_key=key)

    response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Generate a Detailed Example Resume For An Game Developer Dont include any instructions just want an resume")
    print(response.text)
    

if __name__ == "__main__":
    result = generate_resume()
    print(result)
