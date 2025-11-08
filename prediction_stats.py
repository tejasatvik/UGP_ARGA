
import argparse
import pandas as pd
import numpy as np

def load_df(path: str) -> pd.DataFrame:
    df = pd.read_excel(path)
    # normalize yes/no columns safely
    for col in ['run_test', 'run_test.1', 'run_test.2']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().str.strip()
    return df

def overall_accuracy(df: pd.DataFrame) -> pd.DataFrame:
    acc = {
        'top1_correct': (df['run_test'] == 'yes').mean(),
        'top2_correct': (df['run_test.1'] == 'yes').mean(),
        'top3_correct': (df['run_test.2'] == 'yes').mean(),
        'any_correct': ((df[['run_test','run_test.1','run_test.2']] == 'yes').any(axis=1)).mean(),
    }
    out = pd.DataFrame([acc])
    return out

def abstraction_wise(df: pd.DataFrame) -> pd.DataFrame:
    # Collect all abstraction labels that appear anywhere
    abstractions = sorted(set(df.get('predicted_1', [])) | set(df.get('predicted_2', [])) | set(df.get('predicted_3', [])) | set(df.get('solved', [])))
    rows = []
    for abs_name in abstractions:
        subset = df[
            (df['predicted_1'] == abs_name) |
            (df['predicted_2'] == abs_name) |
            (df['predicted_3'] == abs_name)
        ]
        if len(subset) == 0:
            continue
        correct_mask = (
            ((subset['predicted_1'] == abs_name) & (subset['run_test'] == 'yes')) |
            ((subset['predicted_2'] == abs_name) & (subset['run_test.1'] == 'yes')) |
            ((subset['predicted_3'] == abs_name) & (subset['run_test.2'] == 'yes'))
        )
        correct = correct_mask.sum()
        rows.append({
            'abstraction': abs_name,
            'count': len(subset),
            'correct': int(correct),
            'accuracy': (correct / len(subset)) if len(subset) else np.nan
        })
    out = pd.DataFrame(rows).sort_values(['accuracy','count'], ascending=[False, False]).reset_index(drop=True)
    return out

def overlap_stats(df: pd.DataFrame) -> pd.DataFrame:
    unique_frac = (df[['predicted_1','predicted_2','predicted_3']].nunique(axis=1) == 3).mean()
    top3_only = (((df['run_test'] != 'yes') & (df['run_test.1'] != 'yes') & (df['run_test.2'] == 'yes')).sum()) / len(df)
    top2_only = (((df['run_test'] != 'yes') & (df['run_test.1'] == 'yes')).sum()) / len(df)
    top1_only = ((df['run_test'] == 'yes').sum()) / len(df)
    out = pd.DataFrame([{
        'all_unique_preds': unique_frac,
        'correct_in_top1_only': top1_only,
        'correct_in_top2_only': top2_only,
        'correct_in_top3_only': top3_only
    }])
    return out

def confusion_summary(df: pd.DataFrame, top_k: int = 10) -> pd.DataFrame:
    # Count mispredictions: predicted vs solved when run_test == "no" on that slot
    rows = []
    for _, row in df.iterrows():
        for pcol, rcol in zip(['predicted_1','predicted_2','predicted_3'], ['run_test','run_test.1','run_test.2']):
            if row.get(rcol, 'no') == 'no':
                rows.append((row.get(pcol, None), row.get('solved', None)))
    conf_df = pd.DataFrame(rows, columns=['predicted','solved'])
    if conf_df.empty:
        return pd.DataFrame(columns=['predicted','solved','count'])
    out = conf_df.value_counts().reset_index(name='count').head(top_k)
    return out

def format_pct(x: float) -> str:
    if pd.isna(x):
        return "NaN"
    return f"{100.0 * x:.1f}%"

def main():
    ap = argparse.ArgumentParser(description="Compute prediction statistics (1–4).")
    ap.add_argument("--file", "-f", type=str, default="Correct_Predictions.xlsx", help="Path to Excel file")
    ap.add_argument("--topk", type=int, default=10, help="Top-K mispredictions to show")
    args = ap.parse_args()

    df = load_df(args.file)

    # 1) Overall accuracy
    overall = overall_accuracy(df)
    # 2) Abstraction-wise
    per_abs = abstraction_wise(df)
    # 3) Overlap/order stats
    overlap = overlap_stats(df)
    # 4) Confusion summary
    conf = confusion_summary(df, top_k=args.topk)

    print("\n=== 1) Overall Prediction Accuracy ===")
    for col in overall.columns:
        print(f"{col}: {format_pct(overall[col].iloc[0])}")

    print("\n=== 2) Abstraction-wise Performance ===")
    if not per_abs.empty:
        print(per_abs.to_string(index=False))
    else:
        print("No abstraction-wise stats available.")

    print("\n=== 3) Prediction Overlap & Ordering ===")
    for col in overlap.columns:
        print(f"{col}: {format_pct(overlap[col].iloc[0])}")

    print("\n=== 4) Confusion Patterns (Most Common Mispredictions) ===")
    if not conf.empty:
        print(conf.to_string(index=False))
    else:
        print("No mispredictions found.")

    # Save CSV artifacts
    overall.to_csv("overall_accuracy.csv", index=False)
    per_abs.to_csv("abstraction_wise.csv", index=False)
    overlap.to_csv("overlap_stats.csv", index=False)
    conf.to_csv("confusion_summary.csv", index=False)

    print("\nArtifacts written: overall_accuracy.csv, abstraction_wise.csv, overlap_stats.csv, confusion_summary.csv")

if __name__ == "__main__":
    main()
