# ForgeResearcher 🔬⚡

> **Autonomous Empirical ML Research Harness built on TrueForge with Guided Autonomy, Sandboxed Execution, Multi-Subagent Routing, and Qodo Code Review.**

Developed for the **WeMakeDevs Agent Harness Hackathon (TrueForge)** in partnership with **TrueFoundry** & **Qodo**.

---

## 🌟 Guided Autonomy Architecture

**ForgeResearcher** replaces rigid static templates with an **open-ended, contract-bounded research harness**:

```mermaid
flowchart TD
    User([User Prompt: Open Research Goal]) --> RM[Parent Agent: research-manager]
    
    subgraph Guided Autonomy Engine
        RM --> Plan[1. Formulate Hypothesis Matrix & Time Budget]
        Plan --> Gate1{Approval Gate #1: Authorize Sandboxed Compute}
        
        Gate1 -- Approved --> SubA[Subagent A: eval-worker]
        
        subgraph Subagent Contracts
            SubA -->|Dynamically writes & executes in Sandbox| Res[Emits workspace/results.tsv]
            Res --> SubB[Subagent B: plot-worker]
            SubB -->|Generates publication figures| Figs[Emits workspace/figures/]
            
            Res & Figs --> SubC[Subagent C: write-worker]
            SubC -->|Drafts LaTeX manuscript| Paper[Emits workspace/paper.tex]
            
            Paper --> SubD[Subagent D: rigor-worker]
            SubD -->|Level-2 Audit: Verifies claims vs data| Audit[Emits workspace/rigor_audit.json]
        end
        
        Audit --> Gate2{Approval Gate #2: Authorize Final Manuscript Export}
    end
    
    Gate2 -- Approved --> FinalPDF([Compiled PDF Paper + Verified Code Artifacts])
```

---

## 🛡️ Subagents & Responsibilities

| Subagent | Role | Input Contract | Output Contract |
| :--- | :--- | :--- | :--- |
| **`research-manager`** (Parent) | Orchestrator & Approval Owner | User's open research objective | Orchestrates subagents, manages human approval gates, verifies output. |
| **`eval-worker`** | ML Code Writer & Sandbox Runner | Hypothesis specification & dataset target | Generates dynamic training script in `workspace/`, runs in TrueForge sandbox, outputs `results.tsv`. |
| **`plot-worker`** | Publication Visualizer | `results.tsv` | Generates 2 publication-ready charts (e.g. learning curve & metric comparison bar chart) in `workspace/figures/`. |
| **`write-worker`** | Academic LaTeX Author | Research plan + `results.tsv` + figures | Produces 2-column LaTeX manuscript (`workspace/paper.tex`). |
| **`rigor-worker`** | Scientific Auditor | `paper.tex` + `results.tsv` | Audits manuscript claims against empirical metrics to ensure zero hallucinations; outputs `rigor_audit.json`. |

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

### 3. Run End-to-End Simulation
```bash
PYTHONPATH=. .venv/bin/python run_end_to_end_simulation.py
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
  - *Summary:* Implemented initial FastMCP tools for dataset profiling, plotting, and code validation.
  - *Qodo Review:* Automated review conducted on PR creation.
- **[PR #2: Karpathy-style 3-File AutoResearch Sandbox Environment](https://github.com/Its-Atharva-Gupta/forge-researcher/pull/2)**
  - *Summary:* Prototyped initial fixed benchmark sandbox environment.
  - *Qodo Review:* Automated review conducted on PR creation.
- **[PR #3: TrueForge Agent Skills, Subagent Hierarchy, and Approval Gates](https://github.com/Its-Atharva-Gupta/forge-researcher/pull/3)**
  - *Summary:* Configured subagent hierarchy and defined approval gates in `trueforge_config/agent.yaml`.
  - *Qodo Review:* Automated review conducted on PR creation.
- **[PR #4: Guided Autonomy Parent Manager and 4-Subagent Hierarchy](https://github.com/Its-Atharva-Gupta/forge-researcher/pull/4)**
  - *Summary:* Full refactor to Guided Autonomy: Parent `research-manager`, contracted subagents (`eval-worker`, `plot-worker`, `write-worker`, `rigor-worker`), integrated arXiv tool, and Level-2 rigor auditor.
  - *Qodo Review:* Automated review conducted on PR creation with detailed findings.
- **[PR #5: Fix MCP Server based on Qodo Review Findings](https://github.com/Its-Atharva-Gupta/forge-researcher/pull/5)**
  - *Summary:* Fixed all issues surfaced by Qodo: upgraded arXiv API to HTTPS transport, enforced strict metric column validation in plotting to prevent blank images, and added LaTeX special character escaping.
  - *Qodo Review:* Verified and merged cleanly into `master`.

---

## 📁 Repository Structure

```
.
├── workspace/                  # [DYNAMIC] Ephemeral research directory created & used at runtime
├── mcp_servers/
│   └── research_lab_mcp/       # Integrated FastMCP server (arXiv, dataset, plotting, latex, rigor audit)
│       └── server.py
├── skills/                     # TrueForge skill definitions
│   ├── research_manager/       # Parent orchestrator & approval logic
│   ├── eval_worker/            # Sandboxed ML execution & metric contract
│   ├── plot_worker/            # Publication visualizer
│   ├── write_worker/           # Academic LaTeX drafting
│   └── rigor_worker/           # Level-2 Fact-check & claim verification
├── trueforge_config/
│   ├── agent.yaml              # TrueForge agent definition & approval gates
│   └── mcp_settings.json       # MCP configuration
├── run_end_to_end_simulation.py # Full executable pipeline simulation script
├── tests/                      # Automated verification test suite
└── docs/
    ├── REQUIREMENTS.md         # Hackathon requirements dossier
    └── DEMO_SCRIPT.md          # 3-minute video presentation guide
```
