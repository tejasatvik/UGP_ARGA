import os, json, argparse, requests
import sys
from main import solve_task_id       # ARGA entry point

# Increase limit for integer string conversion to handle large token strings
sys.set_int_max_str_digits(10000)  # Set higher than the 5882 digits seen in error

DATASET_PATH = os.path.join("dataset")
SUBSET_PATH  = os.path.join(DATASET_PATH, "subset")
SOL_DIR      = os.path.join("solutions")          # for skip-check

def load_task_ids(txt_name):
    txt_path = os.path.join(SUBSET_PATH, txt_name)
    with open(txt_path, "r", encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip().endswith(".json")]

def task_already_solved(task_file):
    fn = f"solutions_{task_file}"
    return (
        os.path.exists(os.path.join(SOL_DIR, "correct",   fn)) or
        os.path.exists(os.path.join(SOL_DIR, "incorrect", fn))
    )

def main(category):
    task_list = load_task_ids(f"{category}.txt")
    for task_file in task_list:
        if task_already_solved(task_file):
            print(f" {task_file} already solved.")
            continue

        for split in ("training", "evaluation"):
            path = os.path.join(DATASET_PATH, split, task_file)
            if os.path.exists(path):
                print(f"\n [{split.upper()}] {task_file} — solving …")
                solve_task_id(task_file, task_type=split)   
                break
        else:
            print(f" {task_file} not found in dataset/")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run ARGA on one category (augmentation / movement / recolor).")
    parser.add_argument("--category", required=True,
                        choices=["augmentation", "movement", "recolor"])
    main(parser.parse_args().category)
