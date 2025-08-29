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

def token_demo():
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Example prompt
    prompt = "Explain tokenization in simple words with an example."

    # Count tokens used in input prompt
    token_info = model.count_tokens(prompt)
    print("🔢 Token count for prompt:")
    print(token_info, "\n")

    # Generate response with a token limit
    response = model.generate_content(
        prompt,
        generation_config={
            "max_output_tokens": 50  # limit output length
        }
    )

    print("📝 Model Response:")
    print(response.text)

if __name__ == "__main__":
    print("🚀 Running Gemini Tokenization Demo...\n")
    token_demo()
