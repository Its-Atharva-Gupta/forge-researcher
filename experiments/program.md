# Research Directive: Automated Algorithmic Exploration

## Goal
Iteratively optimize validation accuracy and validation log-loss on the binary classification benchmark.

## Rules & Constraints
1. **Never edit `prepare.py`**: All dataset generation and validation splits are fixed.
2. **Only edit `train.py`**: Modify model families (e.g., `HistGradientBoostingClassifier`, `GradientBoostingClassifier`, `ExtraTreesClassifier`, `MLPClassifier`), hyperparameter spaces, feature scaling, or ensembling.
3. **Execution Time Budget**: Each training run must complete within 15 seconds.
4. **Retention Policy**:
   - If `val_acc` improves or `val_loss` decreases without sacrificing accuracy, **keep the change**.
   - If performance degrades or raises runtime exceptions, **revert the change** and record the hypothesis failure in `results.tsv`.
