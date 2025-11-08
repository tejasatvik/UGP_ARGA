from task import *
import sys
import json


def solve_task_id(task_file, task_type="training", abstractions=None):
    """
    solves a given task and saves the solution to a file
    """
    if task_type == "training":
        data_path = "dataset/training/"
    else:
        data_path = "dataset/evaluation/"
    # allow passing a subset of abstractions (labels) to restrict search
    task = Task(data_path + task_file, allowed_abs=abstractions)

    abstraction, solution_apply_call, error, train_error, solving_time, nodes_explored = task.solve(
        shared_frontier=True, time_limit=30, do_constraint_acquisition=True, save_images=False)

    solution = {"abstraction": abstraction, "apply_call": solution_apply_call, "train_error": train_error,
                "test_error": error, "time": solving_time, "nodes_explored": nodes_explored}
    if error == 0:
        with open('solutions/correct/solutions_{}'.format(task_file), 'w') as fp:
            json.dump(solution, fp)
    else:
        with open('solutions/incorrect/solutions_{}'.format(task_file), 'w') as fp:
            json.dump(solution, fp)
    print(solution)


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Solve one ARC task with optional abstraction subset.")
    parser.add_argument("task_file", help="Task filename, e.g. 00d62c1b.json")
    parser.add_argument("--type", choices=["training", "evaluation"], help="Dataset split. If omitted, auto-detect.")
    parser.add_argument("--abs", nargs="+", metavar="LABEL",
                        help="Subset of abstractions to use, e.g. --abs ccg nbccg lrg")
    args = parser.parse_args()

    # Auto-detect split if not provided
    split = args.type
    if split is None:
        tr = os.path.join("dataset", "training", args.task_file)
        ev = os.path.join("dataset", "evaluation", args.task_file)
        if os.path.exists(tr):
            split = "training"
        elif os.path.exists(ev):
            split = "evaluation"
        else:
            raise FileNotFoundError(f"{args.task_file} not found in dataset/training or dataset/evaluation")

    solve_task_id(args.task_file, task_type=split, abstractions=args.abs)


