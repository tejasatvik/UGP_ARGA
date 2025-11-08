import os
from main import solve_task_id  

# Load filenames from the dataset/subset/*.txt category files
def load_task_list(filename):
    full_path = os.path.join("dataset", "subset", filename)
    with open(full_path, 'r') as f:
        return [line.strip() for line in f if line.strip().endswith('.json')]

# Combine all listed .json filenames from the three categories
all_tasks = set()
for category_file in ["augmentation.txt", "movement.txt", "recolor.txt"]:
    all_tasks.update(load_task_list(category_file))

# Run each task and auto-detect whether it's in training or evaluation
for task_filename in sorted(all_tasks):
    found = False
    for split in ["training", "evaluation"]:
        task_path = os.path.join("dataset", split, task_filename)
        if os.path.exists(task_path):
            print(f"\n [{split.upper()}] {task_filename} — solving …")
            # Skip if task already solved
            correct_name = f"solutions_{task_filename}"
            correct_path = os.path.join("solutions", "correct", correct_name)
            incorrect_path = os.path.join("solutions", "incorrect", correct_name)
            if os.path.exists(correct_path) or os.path.exists(incorrect_path):
                print(f" Skipping {task_filename} — already solved.")
                continue
            solve_task_id(task_filename, task_type=split)  # Pass filename and dataset type
            found = True
            break
    if not found:
        print(f" {task_filename} not found in dataset/training or evaluation")
