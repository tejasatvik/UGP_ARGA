import os
import json
import requests

# LLM_ENDPOINT
LLM_MODEL = "llama3.1:8b"
PROMPT_FILE = "prompt.txt"
SUBSET_PATH = os.path.join("dataset", "subset")
DATASET_PATH = os.path.join("dataset")
OUTPUT_JSON = "llm_predictions.json"

# Load base prompt
with open(PROMPT_FILE, "r", encoding="utf-8") as f:
    base_prompt = f.read().strip()

# Load task filenames from all subset categories
def load_task_ids():
    task_ids = set()
    for name in ["augmentation.txt", "movement.txt", "recolor.txt"]:
        with open(os.path.join(SUBSET_PATH, name), "r", encoding="utf-8") as f:
            for line in f:
                task = line.strip()
                if task.endswith(".json"):
                    task_ids.add(task)
    return sorted(task_ids)

def find_task_path(task_file):
    for split in ["training", "evaluation"]:
        path = os.path.join(DATASET_PATH, split, task_file)
        if os.path.exists(path):
            return path, split
    return None, None

def query_llm(full_prompt):
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful reasoning assistant. Please answer based on the instructions and the ARC task provided."},
            {"role": "user", "content": full_prompt}
        ],
        "stream": False
    }
    response = requests.post(LLM_ENDPOINT, json=payload)
    response.raise_for_status()
    return response.json()["message"]["content"]

def main():
    results = {}
    task_ids = load_task_ids()

    for task_file in task_ids:
        print(f"\n Sending {task_file} to LLM...")
        path, split = find_task_path(task_file)
        if not path:
            print(f" Task file {task_file} not found in dataset/")
            continue

        with open(path, "r", encoding="utf-8") as f:
            task_json = json.load(f)

        full_prompt = f"""{base_prompt}

Here is an ARC task in JSON format:

{json.dumps(task_json, indent=2)}"""
        
        print(f"\n--- Prompt Length for {task_file}: {len(full_prompt)} characters ---\n")

        print(f"\n--- Prompt sent to LLM for {task_file} ---\n{full_prompt}\n")

        try:
            response = query_llm(full_prompt)
            results[task_file] = {
                "response": response,
                "split": split
            }
        except Exception as e:
            print(f" Error calling LLM for {task_file}: {e}")
            results[task_file] = {
                "response": None,
                "error": str(e),
                "split": split
            }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n All predictions saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
