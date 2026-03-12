import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("GOOGLE_API_KEY not found in .env")
else:
    genai.configure(api_key=api_key)
    print("Checking models...")
    try:
        models = [m.name for m in genai.list_models()]
        print("Available models:")
        for model in models:
            print(f" - {model}")
    except Exception as e:
        print(f"Error: {e}")
