---
name: autoresearch-loop
description: Iterative sandboxed empirical optimization loop inspired by Karpathy's autoresearch.
---

# AutoResearch Experimentation Skill

## Loop Execution Steps
1. **Hypothesis Formulation**: Formulate an algorithmic hypothesis (e.g., hyperparameter tuning, feature engineering, ensembling).
2. **Approval Gate Check**: Before launching a batch of compute trials, request explicit user authorization via the TrueForge harness.
3. **Safety Audit**: Run `validate_sandbox_code` on the proposed `train.py` changes.
4. **Sandbox Execution**: Execute `train.py` inside the isolated sandbox container.
5. **Metric Evaluation**:
   - Parse `val_loss`, `val_acc`, and `val_auc`.
   - If performance improves, commit the change and log `status=KEPT` in `results.tsv`.
   - If performance regresses or fails, revert the file and log `status=DISCARDED`.
