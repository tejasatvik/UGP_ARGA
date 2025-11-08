import os, pandas as pd
SOLUTIONS_ROOT = "solutions"
AB_FOLDERS = {
    "nbccg": "llm_cross_check_solutions_nbccg",
    "na"   : "llm_cross_check_solutions_na",
    "ccgbr": "llm_cross_check_solutions_ccgbr",
}
CSV_OUT   = "llm_cross_check_report.csv"
XLSX_OUT  = "llm_cross_check_report.xlsx"

table = {}  # task_id -> {nbccg:Yes/No, na:Yes/No, ccgbr:Yes/No}

for label, subdir in AB_FOLDERS.items():
    base = os.path.join(SOLUTIONS_ROOT, subdir)
    for verdict in ("correct", "incorrect"):
        folder = os.path.join(base, verdict)
        if not os.path.isdir(folder):
            continue
        for fname in os.listdir(folder):
            if not fname.endswith(".json"):
                continue
            # strip "solutions_" prefix and ".json" suffix
            task_id = fname.removeprefix("solutions_").removesuffix(".json")
            table.setdefault(task_id, {k: "No" for k in AB_FOLDERS})
            table[task_id][label] = "Yes" if verdict == "correct" else "No"

df = (
    pd.DataFrame.from_dict(table, orient="index")
      .reset_index()
      .rename(columns={"index": "task_id"})
      .sort_values("task_id")
)

df.to_csv(CSV_OUT, index=False)
df.to_excel(XLSX_OUT, index=False)

print(f" Wrote {CSV_OUT} and {XLSX_OUT}  ({len(df)} tasks)")
