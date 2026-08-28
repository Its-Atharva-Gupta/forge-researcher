"""
[IMMUTABLE] Data Preparation & Ground Truth Evaluation Harness
This script downloads/generates the benchmark dataset and establishes fixed train/val/test splits and evaluation metrics.
THE AGENT IS NOT ALLOWED TO MODIFY THIS FILE TO PREVENT DATA LEAKAGE OR METRIC TAMPERING.
"""
import os
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(DATA_DIR, "benchmark_data.csv")

def prepare_benchmark():
    print("Preparing deterministic tabular ML benchmark dataset...")
    X, y = make_classification(
        n_samples=2500,
        n_features=20,
        n_informative=12,
        n_redundant=4,
        n_classes=2,
        weights=[0.6, 0.4],
        flip_y=0.03,
        random_state=42
    )
    
    df = pd.DataFrame(X, columns=[f"feat_{i}" for i in range(20)])
    df["target"] = y
    
    train_df, val_df = train_test_split(df, test_size=0.3, random_state=42, stratify=df["target"])
    
    train_df.to_csv(os.path.join(DATA_DIR, "train.csv"), index=False)
    val_df.to_csv(os.path.join(DATA_DIR, "val.csv"), index=False)
    df.to_csv(DATA_FILE, index=False)
    print(f"Benchmark ready. Train samples: {len(train_df)}, Val samples: {len(val_df)}")

if __name__ == "__main__":
    prepare_benchmark()
