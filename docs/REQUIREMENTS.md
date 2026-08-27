# Agent Harness Hackathon — TrueForge

**Event:** WeMakeDevs "Agent Harness Hackathon" — build a useful AI agent on TrueForge.
**Dates:** Aug 24–30, 2026 · submissions close **Aug 30, 8:00 PM London** (= ~12:30 AM IST Aug 31).
**Theme:** "Give AI models a license to act." Not a chat wrapper — show the harness doing **real work**.

## Why this is winnable / a good build
The judges reward: real-world interaction, **human-approval checkpoints**, real friction removed,
and domain knowledge that's hard to fake. That's what we structure the agent around.

## Prizes ($10,000 pool)
- NVIDIA **DGX Spark** & a **Mac Mini** (headliners)
- Keychron, Logitech MX Master 3, swag
- **Interview opportunities with TrueFoundry** (hiring channel)

## 3 tracks — win ONE only
1. **Best Use of TrueForge** ← recommend (flagship; rewards harness doing real work) — one prize to winning team
2. **Best Code Quality** — one prize to winning team
3. **Best UI** — iPad to *every* member of winning team

## Hard requirements (must submit)
- Agent must **run on TrueForge**; a judge must see the harness doing real work (MCP tools,
  sandbox execution, subagents, approval checkpoints) — not a thin wrapper around a model call.
- **Every substantive change ships as a GitHub PR reviewed by Qodo** before merge, with proof in the README.
- **Write-up:** the job you gave the agent, how you wired it, what TrueForge handled, what broke.
  Screenshots + a demo clip.
- One Qodo install per team is enough; teammates don't need their own accounts.

## Infra / cost notes
- Online participants **bring their own model API key** (OpenAI-compatible works).
- $50 OpenAI credits only for the **SF live day** (Sat Aug 29, separate Luma signup) — out of reach for us.
- Run locally: `npx @truefoundry/trueforge@latest` → port **8790**, SQLite standalone. Node ≥22 (have v22.23.1).
- Hosted mode: Postgres + Redis via Docker Compose / Helm (we have Docker 29.1).

## Dev environment (verified on this PC)
- node v22.23.1 · npm/npx 12.0.2 · git 2.43 · docker 29.1 · 4 cores · 7.6 GB RAM
- TrueForge CLI verified to boot: `npx @truefoundry/trueforge@latest --help` works, v0.1.4.

## Timeline (from today, Aug 27)
- Day 1: scaffold repo + TrueForge local run + model key + Qodo wired on the repo.
- Day 2: build the agent's real tool flow + approval gate.
- Day 3: polish write-up, screenshots, demo clip, PRs through Qodo, finalise README, submit.

## TODO
- [ ] Confirm the idea/track (see README candidates)
- [ ] Paste model API key into local config
- [ ] git init / create repo on GitHub
- [ ] Wire Qodo GitHub app on the repo
- [ ] Run TrueForge locally, connect model + a tool/MCP server
- [ ] Build the approval-gated action flow
- [ ] Write-up + screenshots + demo clip
- [ ] PRs through Qodo; submit before Aug 30 8pm London
