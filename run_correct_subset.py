import os, argparse
from main import solve_task_id  

DATASET      = "dataset"
CORRECT_LIST = os.path.join(DATASET, "subset", "correct.txt")
SOL_DIR      = "solutions"             
LABELS       = ["nbccg", "na", "ccgbr"]  

def load_task_ids(txt_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip().endswith(".json")]

def already_solved(task_file):
    solved_name = f"solutions_{task_file}"
    return os.path.exists(os.path.join(SOL_DIR, "correct",   solved_name)) or \
           os.path.exists(os.path.join(SOL_DIR, "incorrect", solved_name))

def find_split(task_file):
    """Return 'training' or 'evaluation' based on where the JSON lives."""
    if os.path.exists(os.path.join(DATASET, "training", task_file)):
        return "training"
    if os.path.exists(os.path.join(DATASET, "evaluation", task_file)):
        return "evaluation"
    return None

def main(run_label):
    tasks = load_task_ids(CORRECT_LIST)
    print(f" Running {len(tasks)} tasks with abstraction '{run_label}'")

    for task_file in tasks:
        if already_solved(task_file):
            print(f" {task_file} already solved – skipping")
            continue

        split = find_split(task_file)
        if split is None:
            print(f" {task_file} not found in dataset/; skipping")
            continue

        print(f"\n [{split.upper()}] {task_file} with {run_label}")
        solve_task_id(task_file, task_type=split, abstractions=[run_label])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run tasks from subset/correct.txt with one abstraction.")
    parser.add_argument(
        "--label", required=True, choices=LABELS,
        help="Which abstraction to use (nbccg, na, or ccgbr)")
    args = parser.parse_args()
    main(args.label)
