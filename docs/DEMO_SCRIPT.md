# ForgeResearcher: 3-Minute Demo Video Script

**Target Video Length:** ~3:00  
**Focus Areas:** Real MCP tool interaction, sandboxed execution, and explicit **Human-in-the-Loop Approval Gates**.

---

## ⏱️ Act 1: The Problem & The Mission (0:00 - 0:40)
- **Visual:** Show terminal / TrueForge UI interface.
- **Narrator:**
  > *"Machine Learning research is often slowed down by repetitive manual iteration: surveying baselines on ArXiv, writing experiment scripts, logging metrics, and formatting papers. But giving an AI agent direct root access to run compute or publish unchecked is dangerous.*
  > *Meet **ForgeResearcher**—an autonomous empirical research agent built on TrueForge that explores scientific hypotheses inside an isolated sandbox while keeping humans in the loop through strict approval gates."*

---

## ⏱️ Act 2: Literature Review & Approval Gate #1 (0:40 - 1:20)
- **Visual:** User inputs: *"Benchmark and optimize tabular ensemble classifiers on our noisy classification task against recent baseline architectures."*
- **Action:**
  - `LitReviewer` subagent triggers and queries the Research Lab MCP server.
  - Generates hypothesis: *"Test Gradient Boosting with adaptive learning rates vs Random Forests."*
- **Highlight Approval Gate #1:**
  - TrueForge UI displays: `[Licence Required: Approval Gate #1 - Authorize Sandboxed Compute Batch (3 Trials)]`
  - User clicks **"Approve"**.

---

## ⏱️ Act 3: Sandboxed AutoResearch Loop & Metric Trajectory (1:20 - 2:15)
- **Visual:**
  - `AutoExperimenter` modifies `experiments/train.py`.
  - Runs validation inside TrueForge's isolated container sandbox.
  - Shows Trial 1 (Accuracy: 86.1%) $\to$ Trial 2 (Accuracy: 88.9%) $\to$ Trial 3 (Accuracy: 91.2%).
  - Logs audit results to `experiments/results.tsv`.
  - Generates dual-axis optimization curve via `generate_loss_accuracy_plot`.

---

## ⏱️ Act 4: Paper Synthesis & Approval Gate #3 (2:15 - 3:00)
- **Visual:**
  - `PaperAuthor` subagent compiles the `.tex` manuscript embedding the empirical charts and ArXiv citations.
  - TrueForge displays `[Licence Required: Approval Gate #3 - Approve Final Publication & PDF Export]`.
  - User approves $\to$ PDF viewer opens the clean, 2-column conference paper.
  - Quick glance at the public GitHub repo showing all Pull Requests reviewed by **Qodo**.
- **Narrator:**
  > *"Empirical research, verified in a sandbox, governed by human approval, and built with production-grade engineering discipline."*
