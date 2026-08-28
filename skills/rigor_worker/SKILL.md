---
name: rigor-worker
description: Level-2 Scientific Rigor Auditor checking that paper claims strictly match raw results.tsv data.
---

# Rigor Worker Skill

## Input Contract
- Path to `workspace/paper.tex`
- Path to `workspace/results.tsv`

## Execution Protocol
1. Call MCP tool `audit_scientific_claims("workspace/paper.tex", "workspace/results.tsv")`.
2. Ensure there are no hallucinations, false claims, or fabricated percentages.
3. Write validation summary to `workspace/rigor_audit.json`.
4. If audit fails, reject manuscript and instruct `write-worker` to correct discrepancies.
