---
name: plot-worker
description: Publication visualizer turning results.tsv into dual-axis learning curves and comparison bar charts.
---

# Plot Worker Skill

## Input Contract
- Path to `workspace/results.tsv`.

## Execution Protocol
1. Call MCP tool `generate_publication_plots(results_tsv_path, "workspace/figures/")`.
2. Output 2 publication-ready PNG artifacts:
   - `workspace/figures/learning_curve.png`
   - `workspace/figures/benchmark_comparison.png`
