"""
[MUTABLE] Research Playground File
This is the ONLY file the agent modifies to test research hypotheses.
Contains model definition, hyperparameter schedule, and evaluation outputs.
"""
import os
import json
import pandas as pd
from sklearn.metrics import accuracy_score, log_loss, f1_score, roc_auc_score
from sklearn.ensemble import RandomForestClassifier

EXP_DIR = os.path.dirname(os.path.abspath(__file__))
TRAIN_FILE = os.path.join(EXP_DIR, "train.csv")
VAL_FILE = os.path.join(EXP_DIR, "val.csv")

def train_and_eval():
    if not os.path.exists(TRAIN_FILE):
        raise FileNotFoundError("Run prepare.py first.")
        
    train_df = pd.read_csv(TRAIN_FILE)
    val_df = pd.read_csv(VAL_FILE)
    
    X_train, y_train = train_df.drop(columns=["target"]), train_df["target"]
    X_val, y_val = val_df.drop(columns=["target"]), val_df["target"]
    
    # --- MODEL & HYPERPARAMETERS (Agent modifies this block) ---
    model = RandomForestClassifier(
        n_estimators=50,
        max_depth=6,
        min_samples_split=4,
        random_state=42
    )
    # -----------------------------------------------------------
    
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_val)
    y_prob = model.predict_proba(X_val)
    
    acc = accuracy_score(y_val, y_pred) * 100.0
    loss = log_loss(y_val, y_prob)
    f1 = f1_score(y_val, y_pred)
    auc = roc_auc_score(y_val, y_prob[:, 1])
    
    metrics = {
        "val_loss": round(loss, 4),
        "val_acc": round(acc, 2),
        "val_f1": round(f1, 4),
        "val_auc": round(auc, 4)
    }
    
    print(json.dumps(metrics))
    return metrics

if __name__ == "__main__":
    train_and_eval()
