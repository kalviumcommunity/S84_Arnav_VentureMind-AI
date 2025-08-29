import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load evaluation dataset
with open("evaluation_dataset.json", "r") as f:
    dataset = json.load(f)["samples"]

model = genai.GenerativeModel("gemini-1.5-flash")

# Judge prompt template
JUDGE_PROMPT = """
You are an evaluator. Compare the model's response with the expected output.
Task: {task}
Input: {input}
Expected: {expected}
Model Output: {output}

Give a score between 0 and 1:
- 1 if correct/very close
- 0 if wrong
- Between 0 and 1 if partially correct.
Also explain briefly.
"""

def run_evaluation():
    results = []
    for sample in dataset:
        # Generate model response
        response = model.generate_content(sample["input"])
        output_text = response.text.strip()

        # Judge evaluation
        judge = model.generate_content(
            JUDGE_PROMPT.format(
                task=sample["task"],
                input=sample["input"],
                expected=sample["expected_output"],
                output=output_text
            ),
            generation_config={"temperature": 0.0}
        )

        results.append({
            "id": sample["id"],
            "task": sample["task"],
            "input": sample["input"],
            "expected": sample["expected_output"],
            "model_output": output_text,
            "judge_score": judge.text
        })

    # Save results
    with open("evaluation_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("✅ Evaluation complete! Results saved to evaluation_results.json")

if __name__ == "__main__":
    run_evaluation()
