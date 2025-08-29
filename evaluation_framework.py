import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load dataset
with open("evaluation_dataset.json", "r") as f:
    dataset = json.load(f)["samples"]

model = genai.GenerativeModel("gemini-1.5-flash")

# Judge prompt
JUDGE_PROMPT = """
You are an evaluator. Compare the model's response with the expected output.
Task: {task}
Input: {input}
Expected: {expected}
Model Output: {output}

Scoring Rules:
- 1.0 if correct/very close
- 0.0 if wrong
- Between 0 and 1 if partially correct.

Respond in JSON:
{{
  "score": <float between 0 and 1>,
  "explanation": "<short reasoning>"
}}
"""

def run_evaluation():
    results = []
    total_score = 0

    for sample in dataset:
        # Step 1: Generate model output
        response = model.generate_content(
            sample["input"],
            generation_config={
                "temperature": 0.7,
                "top_p": 0.9,
                "max_output_tokens": 150
            }
        )
        output_text = response.text.strip()

        # Step 2: Judge evaluation
        judge = model.generate_content(
            JUDGE_PROMPT.format(
                task=sample["task"],
                input=sample["input"],
                expected=sample["expected_output"],
                output=output_text
            ),
            generation_config={"temperature": 0.0}
        )

        try:
            judge_result = json.loads(judge.text)
            score = judge_result.get("score", 0)
        except:
            score = 0
            judge_result = {"score": 0, "explanation": "Judge parsing failed."}

        total_score += score

        results.append({
            "id": sample["id"],
            "task": sample["task"],
            "input": sample["input"],
            "expected": sample["expected_output"],
            "model_output": output_text,
            "judge_score": score,
            "judge_explanation": judge_result.get("explanation", "N/A")
        })

    # Save results
    with open("evaluation_results.json", "w") as f:
        json.dump(results, f, indent=2)

    avg_score = total_score / len(dataset)
    print(f"\n📊 Average Score: {avg_score:.2f}")
    print("✅ Evaluation complete! Results saved to evaluation_results.json")

if __name__ == "__main__":
    run_evaluation()
