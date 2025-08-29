import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def test_gemini():
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = "Suggest 5 startup ideas in the health tech domain."

    # Low Top P (more focused, deterministic)
    low = model.generate_content(
        prompt,
        generation_config={"temperature": 0.7, "top_p": 0.2, "max_output_tokens": 150}
    )

    # High Top P (more diverse, creative)
    high = model.generate_content(
        prompt,
        generation_config={"temperature": 0.7, "top_p": 0.9, "max_output_tokens": 150}
    )

    print("\n=== Gemini Results ===")
    print("\n--- Top P = 0.2 (focused) ---")
    print(low.text)
    print("\n--- Top P = 0.9 (diverse) ---")
    print(high.text)

if __name__ == "__main__":
    print("🔍 Running Gemini Top P Demo...\n")
    test_gemini()
