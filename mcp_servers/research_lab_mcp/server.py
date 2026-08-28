"""
Data Profiler & Academic Plotting Engine
"""
from typing import Dict, Any, List
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from fastmcp import FastMCP

mcp = FastMCP("ResearchLabServer")

def profile_dataset(dataset_path: str) -> Dict[str, Any]:
    """Profiles a dataset file (CSV/TSV)."""
    if not os.path.exists(dataset_path):
        return {"error": f"File {dataset_path} not found"}
    try:
        sep = "\t" if dataset_path.endswith(".tsv") else ","
        df = pd.read_csv(dataset_path, sep=sep)
        return {
            "success": True,
            "rows": len(df),
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "summary": df.describe().to_dict()
        }
    except Exception as e:
        return {"error": str(e)}

def generate_publication_plots(results_tsv_path: str, output_figure_dir: str) -> Dict[str, Any]:
    """Reads results.tsv and generates dual-axis publication figures."""
    if not os.path.exists(results_tsv_path):
        return {"error": f"Results file {results_tsv_path} not found"}

    os.makedirs(output_figure_dir, exist_ok=True)
    df = pd.read_csv(results_tsv_path, sep="\t")

    required_columns = {"iteration", "val_loss", "val_acc"}
    if not required_columns.issubset(set(df.columns)):
        return {"error": f"Missing required columns {required_columns - set(df.columns)} in results.tsv"}

    fig, ax1 = plt.subplots(figsize=(8, 5))
    ax1.plot(df['iteration'], df['val_loss'], color='tab:red', marker='o', label='Validation Loss')
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('Validation Loss', color='tab:red')

    ax2 = ax1.twinx()
    ax2.plot(df['iteration'], df['val_acc'], color='tab:blue', marker='s', label='Validation Accuracy')
    ax2.set_ylabel('Validation Accuracy', color='tab:blue')

    plt.title('Convergence Trajectory')
    fig_path1 = os.path.join(output_figure_dir, 'convergence_curves.png')
    fig.tight_layout()
    plt.savefig(fig_path1, dpi=300)
    plt.close()

    fig, ax = plt.subplots(figsize=(8, 5))
    df.plot(kind='bar', x='iteration', y=['train_loss', 'val_loss'], ax=ax)
    plt.title('Train vs Validation Loss')
    fig_path2 = os.path.join(output_figure_dir, 'loss_comparison.png')
    plt.savefig(fig_path2, dpi=300)
    plt.close()

    return {
        "success": True,
        "figures_generated": [fig_path1, fig_path2]
    }


if __name__ == "__main__":
    mcp.run()
