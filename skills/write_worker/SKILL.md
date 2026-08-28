---
name: write-worker
description: Academic LaTeX author synthesizing research goals, ArXiv citations, results, and figures into a 2-column paper.
---

# Write Worker Skill

## Input Contract
- Research hypothesis & problem statement.
- ArXiv literature citations.
- `workspace/results.tsv` empirical numbers.
- Generated figure paths from `workspace/figures/`.

## Execution Protocol
1. Format a structured LaTeX manuscript with standard sections:
   - Abstract
   - Introduction
   - Related Work
   - Empirical Methodology
   - Results & Discussion
2. Embed the generated figures directly into the `.tex` document.
3. Call MCP tool `render_latex_manuscript` to compile `workspace/paper.tex`.
