import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env (GEMINI_API_KEY or GOOGLE_API_KEY)
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("⚠️ No API key found. Set GEMINI_API_KEY (or GOOGLE_API_KEY) in your .env")

genai.configure(api_key=api_key)
MODEL = "gemini-1.5-flash"

def ask(prompt, max_tokens=200):
    model = genai.GenerativeModel(MODEL)
    resp = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.4,
            "top_p": 0.9,
            "max_output_tokens": max_tokens
        }
    )
    return resp.text

def solve_math_problem():
    # Example reasoning task (average speed)
    question = "A train travels 120 km at 60 km/h, then 60 km at 30 km/h. What is the average speed for the whole trip?"
    instruction = (
        "You are a careful problem solver. Work the problem privately. "
        "Return ONLY a JSON object with keys: "
        "'final_answer' (string with unit) and 'concise_explanation' (<= 25 words). "
        "Do not include your reasoning steps."
    )
    prompt = f"{instruction}\n\nQuestion: {question}"
    print("=== Math (reasoning-safe) ===")
    print(ask(prompt, max_tokens=120))

def classify_feedback():
    # Example analysis/classification task
    feedback = "The UI looks clean but the signup is slow on 3G."
    instruction = (
        "Classify the feedback. Think privately; do not show your reasoning. "
        "Return ONLY JSON with keys: 'categories' (array from ['UI','Performance','Bugs','Feature Request']), "
        "'priority' ('High'|'Medium'|'Low'), and 'concise_explanation' (<= 20 words)."
    )
    prompt = f"{instruction}\n\nFeedback: {feedback}"
    print("\n=== Classification (reasoning-safe) ===")
    print(ask(prompt, max_tokens=120))

if __name__ == "__main__":
    print("🔍 Running reasoning-safe prompting demo...\n")
    solve_math_problem()
    classify_feedback()
