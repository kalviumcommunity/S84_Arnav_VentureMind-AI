import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def test_gemini_stop():
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = "Write a short story about a robot exploring space. End the story with the word END."

    # With stop sequence
    with_stop = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.7,
            "max_output_tokens": 150,
            "stop_sequences": ["END"]   # 🚨 will stop generation when "END" appears
        }
    )

    # Without stop sequence
    without_stop = model.generate_content(
        prompt,
        generation_config={"temperature": 0.7, "max_output_tokens": 150}
    )

    print("\n=== Gemini Stop Sequence Demo ===")
    print("\n--- With Stop Sequence (cuts off at 'END') ---")
    print(with_stop.text)
    print("\n--- Without Stop Sequence (keeps going) ---")
    print(without_stop.text)

if __name__ == "__main__":
    print("🔍 Running Gemini Stop Sequence Demo...\n")
    test_gemini_stop()
