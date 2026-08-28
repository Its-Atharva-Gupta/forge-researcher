---
name: eval-worker
description: Dynamic sandboxed experiment executor. Writes ML training scripts and logs to results.tsv.
---

# Eval Worker Skill

## Input Contract
- Hypothesis specification & dataset target.
- Time budget (≤ 2 minutes total).

## Execution Protocol
1. Dynamically write training & evaluation code inside `workspace/experiment_{trial_id}.py`.
2. Execute the script inside TrueForge's isolated container sandbox.
3. Parse metrics (`val_loss`, `val_acc`, `val_f1`, `val_auc`).
4. Append row to `workspace/results.tsv`:
   ```tsv
   iteration	description	val_loss	val_acc	val_f1	val_auc	status
   ```
5. If trial improves SOTA, retain the checkpoint; if it regresses, log `status=DISCARDED`.
