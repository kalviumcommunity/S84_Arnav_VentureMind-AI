import os, json
from dotenv import load_dotenv
import google.generativeai as genai

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("⚠️ No API key found in .env file")
genai.configure(api_key=api_key)

MODEL = "gemini-1.5-flash"

# Load dataset
with open("eval_dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

def run_eval():
    model = genai.GenerativeModel(MODEL)
    results = []
    correct = 0

    for item in dataset:
        prompt = item["prompt"]
        expected = item.get("expected")

        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.3, "max_output_tokens": 100}
        )

        output = response.text.strip()
        result = {
            "id": item["id"],
            "task": item["task"],
            "prompt": prompt,
            "output": output,
            "expected": expected
        }

        # simple scoring: exact match
        if expected and output == expected:
            result["score"] = 1
            correct += 1
        else:
            result["score"] = 0

        results.append(result)

    # Final report
    accuracy = correct / len(dataset)
    print(f"\n✅ Evaluation complete! Accuracy: {accuracy:.2%}\n")

    # Save results
    with open("eval_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    print("🔍 Running evaluation framework...\n")
    run_eval()
