# Agent Harness Hackathon

Building through an agent harness, not just a chat loop.

## How to run (local, standalone)

```bash
npx @truefoundry/trueforge@latest
# server starts on http://localhost:8790
```

Requires Node.js >= 22. Uses SQLite by default (local-only, not production-safe).

## The idea

> **Recommended default: India traffic-challan contest coach** (a TrueForge agent).
>
> What it does: takes a challan case number / plate, reads the relevant traffic rule,
> gathers the facts, and **drafts a formal contest/first-appeal notice**.
> The agent **cannot file it** — it presents the draft and asks the human for approval before
> any "send/submit" action (the harness's approval checkpoint). Real-world tool use + a
> genuine human-approval gate + hard-to-fake domain knowledge = very on-theme for the judges.
>
> Alternative candidates:
> - **Invoice/expense approval agent** — categorises invoices, flags anomalies, requires
>   human approval before any payment. (Needs an email/docs API = more auth setup.)
> - **Deploy/ops guardrail agent** — reviews config/runbooks, proposes changes, requires
>   human approval before touching anything.

## Track
Best Use of TrueForge (flagship).

## Requirements
See `docs/REQUIREMENTS.md` for the full rules, prizes, Qodo setup, and timeline.

## Stack
- TrueForge (open-source agent harness), local standalone mode
- Node.js >= 22
- OpenAI-compatible model key (any provider)
- MCP tools / sandbox for real work
- Qodo for PR code review
