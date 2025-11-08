import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_df(path: str) -> pd.DataFrame:
    df = pd.read_excel(path)
    for col in ['run_test', 'run_test.1', 'run_test.2']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().str.strip()
    return df

def build_confusion_df(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, r in df.iterrows():
        for pcol, rcol in zip(['predicted_1','predicted_2','predicted_3'],
                              ['run_test','run_test.1','run_test.2']):
            if r.get(rcol, 'no') == 'no':  # only mismatches
                rows.append((r.get(pcol, None), r.get('solved', None)))
    return pd.DataFrame(rows, columns=['Predicted','Solved'])

def plot_confusion_heatmap(conf_df: pd.DataFrame, out_png: str = "confusion_heatmap_colored.png"):
    # create pivot table (true labels = rows, predicted = columns)
    mat = conf_df.value_counts().reset_index(name='Count')
    pivot = mat.pivot(index='Solved', columns='Predicted', values='Count').fillna(0)

    plt.figure(figsize=(10, 7))
    sns.heatmap(
        pivot, annot=True, fmt=".0f",
        cmap="Blues",  # same palette as used earlier
        cbar=True
    )
    plt.title("Confusion Matrix Heatmap (Predicted vs. True Abstractions)", fontsize=14)
    plt.xlabel("Predicted Abstraction", fontsize=12)
    plt.ylabel("True (Solved) Abstraction", fontsize=12)
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.show()
    print(f"Saved heatmap to {out_png}")

def main():
    ap = argparse.ArgumentParser(description="Plot confusion heatmap (colored) from Excel.")
    ap.add_argument("--file", "-f", default="Correct_Predictions.xlsx", help="Path to Excel file")
    ap.add_argument("--out", "-o", default="confusion_heatmap_colored.png", help="Output PNG path")
    args = ap.parse_args()

    df = load_df(args.file)
    conf_df = build_confusion_df(df)
    plot_confusion_heatmap(conf_df, args.out)

if __name__ == "__main__":
    main()
