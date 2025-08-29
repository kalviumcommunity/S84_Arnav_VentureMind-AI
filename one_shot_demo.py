# filename: one_shot_demo.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("⚠️ GEMINI_API_KEY not found. Please set it in your .env file.")

# Configure Gemini
genai.configure(api_key=api_key)

def one_shot_prompting():
    model = genai.GenerativeModel("gemini-1.5-flash")

    # One-shot prompt: give 1 example + new task
    prompt = """
You are an assistant that answers in JSON format.

Example:
Q: "What is the capital of France?"
A: {"answer": "Paris"}

Now follow the same format:

Q: "What is the capital of Japan?"
A:
"""

    response = model.generate_content(
        prompt,
        generation_config={"max_output_tokens": 50}
    )

    print("=== One-Shot Prompting Demo ===")
    print(response.text)

if __name__ == "__main__":
    print("🚀 Running One-Shot Prompting Demo...\n")
    one_shot_prompting()
