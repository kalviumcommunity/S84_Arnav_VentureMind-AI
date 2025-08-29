import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def test_gemini():
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = "Suggest 5 startup ideas in the health tech domain."

    # Top K = 1 (very deterministic)
    topk_low = model.generate_content(
        prompt,
        generation_config={"temperature": 0.7, "top_k": 1, "max_output_tokens": 150}
    )

    # Top K = 40 (more diverse)
    topk_high = model.generate_content(
        prompt,
        generation_config={"temperature": 0.7, "top_k": 40, "max_output_tokens": 150}
    )

    print("\n=== Gemini Results with Top K ===")
    print("\n--- Top K = 1 (deterministic) ---")
    print(topk_low.text)
    print("\n--- Top K = 40 (more diverse) ---")
    print(topk_high.text)

if __name__ == "__main__":
    print("🔍 Running Gemini Top K Demo...\n")
    test_gemini()
