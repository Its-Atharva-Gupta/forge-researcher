---
name: latex-manuscript
description: Formats empirical results, tables, and charts into a 4-page LaTeX conference paper.
---

# LaTeX Manuscript Skill

## Drafting Steps
1. Call `generate_loss_accuracy_plot` on `results.tsv` to produce the figure.
2. Structure the conference manuscript:
   - **Title & Abstract**: Highlighting core findings and empirical gains.
   - **Introduction**: Motivation and context.
   - **Related Work**: Referencing ArXiv benchmarks.
   - **Methodology**: Algorithmic modifications tested in sandbox.
   - **Empirical Results**: Including optimization curves and tabular comparisons.
   - **Discussion & Limitations**: Safe boundaries and compute footprint.
3. Call `render_latex_manuscript` to compile the `.tex` document.
4. Trigger the final publication approval gate before exporting the final PDF artifact.
