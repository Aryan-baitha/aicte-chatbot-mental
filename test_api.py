import google.generativeai as genai
import os

API_KEY = "AIzaSyBOAp3QikfWYZw3rRmTloZ1053sdIwDUgA"

try:
    print(f"Configuring API with key: {API_KEY[:5]}...{API_KEY[-3:]}")
    genai.configure(api_key=API_KEY)
            
    print("\nAttempting to generate content with 'gemini-flash-latest'...")
    model = genai.GenerativeModel('gemini-flash-latest')
    response = model.generate_content("Hello, are you working?")
    print(f"\nSUCCESS! Response: {response.text}")
    
except Exception as e:
    print(f"\nFAILURE: {e}")
