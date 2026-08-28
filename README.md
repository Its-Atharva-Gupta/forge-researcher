# ForgeResearcher 🔬⚡

> **Autonomous Empirical ML Research Agent built on TrueForge with Sandboxed Execution, Approval-Gated Compute, and Qodo Code Review.**

Developed for the **WeMakeDevs Agent Harness Hackathon (TrueForge)** in partnership with **TrueFoundry** & **Qodo**.

---

## 🌟 Overview

**ForgeResearcher** automates the repetitive cycle of machine learning research without sacrificing safety or control. Inspired by Andrej Karpathy's `autoresearch` and Orchestra Research's `AI-research-SKILLs`, ForgeResearcher orchestrates the full scientific method:
1. **Literature & Baseline Survey:** Queries ArXiv / Semantic Scholar for baseline benchmarks.
2. **Approval Gate #1 (Compute Authorization):** Halts and requests human authorization before launching compute trials.
3. **Sandboxed AutoResearch Loop:** Modifies `experiments/train.py`, audits safety via FastMCP tools, executes inside TrueForge's isolated container sandbox, and logs empirical metrics to `experiments/results.tsv`.
4. **Paper Synthesis:** Compiles findings, statistical charts, and LaTeX tables into a 4-page conference-style PDF manuscript.

---

## 🛡️ TrueForge Harness Features Demonstrated

- **Isolated Sandbox Execution:** All training and metric evaluations execute inside TrueForge's isolated runtime sandbox.
- **Human-in-the-Loop Approval Gates:**
  - `Gate #1`: Authorize compute budget before batch trials.
  - `Gate #2`: Anomaly recovery & error handling.
  - `Gate #3`: Authorize final publication & PDF export.
- **Multi-Subagent Hierarchy:** Coordinated execution across `LitReviewer`, `AutoExperimenter`, and `PaperAuthor`.
- **Custom MCP Integration:** Powered by the `ResearchLabServer` FastMCP server.

---

## 🚀 Quick Start (Local Setup)

### 1. Environment Setup
```bash
# Uses uv (fast Python package manager)
uv venv .venv
source .venv/bin/activate
uv pip install -r <(echo "pytest mcp pandas matplotlib scikit-learn numpy")
```

### 2. Run Test Suite
```bash
.venv/bin/python -m pytest tests/
```

### 3. Run Benchmark Locally
```bash
.venv/bin/python experiments/prepare.py
.venv/bin/python experiments/train.py
```

### 4. Launch TrueForge Harness
```bash
npx @truefoundry/trueforge@latest
# Open TrueForge dashboard on http://localhost:8790
```

---

## 🔍 Qodo Code Review Evidence

In accordance with hackathon engineering best practices, every substantive feature was developed through branch-based Pull Requests reviewed by **Qodo** before merge:

- **[PR #1: FastMCP Research Lab Server & Verification Suite](https://github.com/Its-Atharva-Gupta/forge-researcher/pull/1)**
  - *Summary:* Implemented FastMCP tools for dataset profiling, plotting, and code validation.
  - *Qodo Review:* Automated review conducted on PR creation.
- **[PR #2: Karpathy-style 3-File AutoResearch Sandbox Environment](https://github.com/Its-Atharva-Gupta/forge-researcher/pull/2)**
  - *Summary:* Added immutable `prepare.py`, mutable `train.py`, and `results.tsv` audit logger.
  - *Qodo Review:* Automated review conducted on PR creation.
- **[PR #3: TrueForge Agent Skills, Subagent Hierarchy, and Approval Gates](https://github.com/Its-Atharva-Gupta/forge-researcher/pull/3)**
  - *Summary:* Configured multi-subagent hierarchy and defined explicit approval gates in `trueforge_config/agent.yaml`.
  - *Qodo Review:* Automated review conducted on PR creation.

---

## 📁 Repository Structure

```
.
├── experiments/
│   ├── prepare.py          # [IMMUTABLE] Fixed dataset split & ground truth metrics
│   ├── train.py            # [MUTABLE] Model architecture & training loop edited by agent
│   ├── program.md          # [DIRECTIVES] Exploration constraints & metric bounds
│   └── results.tsv         # Experiment audit log
├── mcp_servers/
│   └── research_lab_mcp/   # Custom FastMCP server for research utilities
│       └── server.py
├── skills/                 # TrueForge skill definitions
│   ├── autoresearch_loop/
│   ├── latex_manuscript/
│   └── literature_review/
├── trueforge_config/
│   ├── agent.yaml          # Agent definition & approval gates
│   └── mcp_settings.json   # MCP configuration
├── tests/                  # Automated verification test suite
└── docs/
    ├── REQUIREMENTS.md     # Hackathon requirements dossier
    └── DEMO_SCRIPT.md      # 3-minute video presentation guide
```
