# LLM-Guided Abstraction Selection for the ARGA Framework

This repository implements a neuro-symbolic approach to solving the Abstraction and Reasoning Corpus (ARC). By integrating Large Language Models (LLMs) as high-level "structural intuition" providers, we optimize the Abstract Reasoning with Graph Abstractions (ARGA) framework.

The core of this research demonstrates that LLMs can accurately predict which graph-based abstraction (e.g., nbccg, ccgbr, mcccg) is most likely to solve a specific ARC task, significantly pruning the search space for symbolic solvers.

## Key Research Findings

Based on an empirical study of 54 ARC tasks and 9 distinct abstraction schemas:

* **State-of-the-Art Priors:** GPT-5's Top-3 abstraction predictions achieve a success rate of **88.89%**, significantly outperforming the solver's historically strongest static heuristics (**79.63%**).
* **Strong Statistical Correlation:** There is a significant correlation between LLM intuition and solver performance (Spearman $\rho \approx 0.27, p < 10^{-9}$), suggesting that LLMs encode structural priors similar to human reasoning.
* **Search Space Reduction:** By utilizing LLM-predicted priors, the ARGA solver can prioritize the most promising structural hypotheses, leading to faster convergence and shorter program lengths.

---

## Performance Comparison

| Metric | Accuracy / Success Rate |
| :--- | :--- |
| Top-1 LLM Prediction | $57.43\%$ |
| Top-2 LLM Prediction | $83.33\%$ |
| Top-3 LLM Prediction | $88.89\%$ |
| Top-3 Static Baseline | $79.63\%$ |

---

## Repository Structure

* **data/**:
    * Dataset A: Empirical solver metrics (success, time, program length) across 9 abstractions.
    * Dataset B: LLM-generated predictions, confidence scores, and qualitative rationales.
* **src/**: Source code for the modified ARGA solver, graph extraction logic, and LLM inference pipeline.
* **notebooks/**: Jupyter notebooks for statistical analysis and visualization.
* **docs/**: Technical documentation and the full project report (UGP_REPORT.pdf).

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tejasatvik/UGP_ARGA.git
   cd UGP_ARGA
   ```

2. **Set up the environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure API Keys:**
   Create a `.env` file or export your key:
   ```bash
   export OPENAI_API_KEY='your-api-key'
   ```

---

## Usage

### Generate Solver Metrics
To run the ARGA solver independently across all nine abstractions for benchmarking:
```bash
python src/generate_dataset_a.py --tasks_dir ./data/tasks
```

### Predict Abstraction Priors
To use the LLM to predict the optimal abstraction for new ARC tasks:
```bash
python src/predict_abstractions.py --input ./data/new_tasks.json
```

### Evaluate Results
To compute the Spearman correlation and accuracy metrics:
```bash
python src/evaluate.py --dataset_a data/dataset_a.csv --dataset_b data/dataset_b.json
```
