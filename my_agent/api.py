import google.generativeai as genai
from google.api_core import exceptions
import os
from dotenv import load_dotenv

load_dotenv()

# Collect keys from .env
API_KEYS = [
    os.getenv('GOOGLE_API_KEY'),
    os.getenv('GOOGLE_API_KEY2'),
    os.getenv('GOOGLE_API_KEY3'),
    os.getenv('GOOGLE_API_KEY4'),
    os.getenv('GOOGLE_API_KEY5')
]

class GeminiRotator:
    def __init__(self, keys):
        # Filter out None values in case some .env keys are missing
        self.keys = [k for k in keys if k]
        self.current_index = 0
        self.model_name = 'gemini-2.5-flash-lite'
        self._configure()

    def _configure(self):
        if self.current_index < len(self.keys):
            genai.configure(api_key=self.keys[self.current_index])
            self.model = genai.GenerativeModel(self.model_name)

    def chat(self, prompt):
        """The single method you will call from outside"""
        while self.current_index < len(self.keys):
            try:
                response = self.model.generate_content(prompt)
                return response.text
            
            except exceptions.ResourceExhausted:
                print(f"Key #{self.current_index + 1} exhausted. Rotating...")
                self.current_index += 1
                if self.current_index < len(self.keys):
                    self._configure()
                else:
                    return "ERROR: All API keys exhausted."
            except Exception as e:
                return f"ERROR: {str(e)}"
        return "ERROR: No valid API keys available."

# Initialize once as a singleton
rotator = GeminiRotator(API_KEYS)

def get_gemini_response(prompt):
    return rotator.chat(prompt)