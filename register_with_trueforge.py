"""
Auto-Register ForgeResearcher with Explicit Guided Autonomy Subagent Roles
Configures the parent `research-manager` with the 4 contracted subagent roles:
- `eval-worker` (LM evaluation harness / code sandbox)
- `plot-worker` (Academic plotting engine)
- `write-worker` (LaTeX 2-column paper synthesis)
- `rigor-worker` (Level-2 empirical fact-checker)
"""
import os
import json
import urllib.request
import urllib.error

TRUEFORGE_API = "http://localhost:8790/api/v1"

KAGGLE_TOKEN = os.environ.get("KAGGLE_KEY", "KGAT_e248157027a0f42dd30f6976a1a0d2c2")
KAGGLE_USER = os.environ.get("KAGGLE_USERNAME", "atharvagupta123")

def make_request(endpoint, method="GET", data=None):
    url = f"{TRUEFORGE_API}{endpoint}"
    headers = {"Content-Type": "application/json"}
    body = json.dumps(data).encode("utf-8") if data else None
    
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        return {"error": f"HTTP {e.code}: {err_msg}"}
    except Exception as e:
        return {"error": str(e)}

def setup():
    print("=" * 60)
    print("⚡ CONFIGURING TRUEFORGE WITH GUIDED AUTONOMY SUBAGENTS")
    print("=" * 60)

    # 1. Connect
    mcp_check = make_request("/settings/mcp-servers")
    if "error" in mcp_check:
        print(f"  ❌ Cannot connect to TrueForge: {mcp_check['error']}")
        return False

    # 2. Register Authenticated Remote Kaggle MCP Server
    kaggle_payload = {
        "manifest": {
            "type": "remote",
            "name": "kaggle",
            "url": "https://www.kaggle.com/mcp",
            "description": "Official Kaggle MCP Server: Search/download datasets, run/manage notebooks & GPU kernels, competitions, and models.",
            "auth": {
                "type": "header",
                "headers": {
                    "Authorization": f"Bearer {KAGGLE_TOKEN}"
                }
            }
        }
    }
    make_request("/settings/mcp-servers", method="PUT", data=kaggle_payload)

    # 3. Register local Research & Colab Tools
    tools_payload = {
        "manifest": {
            "type": "remote",
            "name": "forge-researcher-tools",
            "url": "http://127.0.0.1:8795/sse",
            "description": "Research toolkit: Google Colab, arXiv search, academic citations, plotting, LaTeX compilation, and Level-2 rigor auditor."
        }
    }
    make_request("/settings/mcp-servers", method="PUT", data=tools_payload)

    # 4. Detect Model
    providers_res = make_request("/settings/model-providers")
    model_name = "deepseek/deepseek"
    if "data" in providers_res and len(providers_res["data"]) > 0:
        first_prov = providers_res["data"][0]
        prov_name = first_prov.get("name")
        models = first_prov.get("manifest", {}).get("models", [])
        if models:
            model_name = f"{prov_name}/{models[0].get('name')}"

    print(f"\nRegistering 'forge-researcher' with Guided Autonomy Subagent Contracts...")
    
    agent_instructions = (
        "You are 'forge-researcher', an autonomous empirical ML research harness operating under GUIDED AUTONOMY.\n\n"
        f"AUTHENTICATED KAGGLE USER: {KAGGLE_USER}\n\n"
        "## SUBAGENT ROLES & CONTRACTS (You MUST orchestrate these via `create_sub_agent`):\n"
        "When executing a full research cycle or complex exploration, you delegate to these 4 contracted sub-agents:\n"
        "1. **`eval-worker`** (Role: Code Sandbox & Benchmark Evaluation)\n"
        "   - Contract: Writes experiment scripts and runs them in `workspace/` sandbox.\n"
        "   - Output: Emits `workspace/results.tsv` containing iteration, val_loss, and val_acc.\n"
        "2. **`plot-worker`** (Role: Academic Plotting Engine)\n"
        "   - Contract: Invokes `generate_publication_plots` on `workspace/results.tsv`.\n"
        "   - Output: Generates publication loss and comparison charts in `workspace/figures/`.\n"
        "3. **`write-worker`** (Role: LaTeX Conference Manuscript Synthesis)\n"
        "   - Contract: Uses official conference templates (NeurIPS, ICLR, ICML) to write `workspace/paper.tex`.\n"
        "   - Output: Invokes `render_latex_manuscript` with abstract, methodology, and embedded figures.\n"
        "4. **`rigor-worker`** (Role: Level-2 Scientific Fact-Checker & Auditor)\n"
        "   - Contract: Invokes `audit_scientific_claims` to fact-check numbers in `workspace/paper.tex` against raw numbers in `workspace/results.tsv`.\n"
        "   - Output: Produces `workspace/rigor_audit.json` to prevent metric hallucination.\n\n"
        "## RESEARCH WORKFLOW & APPROVAL GATES:\n"
        "Step 1: Literature Search — Call `search_arxiv` or `search_semantic_scholar` to pull real papers.\n"
        "Step 2: Hypothesis Matrix — Propose 3 experimental trials with metrics and budget.\n"
        "Step 3: APPROVAL GATE #1 — Pause and ask the user: 'Do you approve running these compute trials in the sandbox?'\n"
        "Step 4: Delegation — Spawn `eval-worker`, `plot-worker`, `write-worker`, and `rigor-worker` in sequence.\n"
        "Step 5: APPROVAL GATE #2 — Present audit results and ask for user approval before finalizing the PDF."
    )

    agent_payload = {
        "name": "forge-researcher",
        "manifest": {
            "model": {
                "name": model_name,
                "params": {"reasoning_effort": "minimal"}
            },
            "instructions": agent_instructions,
            "mcp_servers": [
                {"name": "kaggle", "enable_tools": ["@all"], "preload": True},
                {"name": "forge-researcher-tools", "enable_tools": ["@all"], "preload": True}
            ],
            "config": {
                "iteration_limit": 100,
                "sandbox": {
                    "enabled": True,
                    "file_downloads": True
                },
                "dynamic_sub_agents": {
                    "enabled": True
                },
                "context_management": {
                    "compaction": {"enabled": True},
                    "large_tool_response": {"enabled": True}
                },
                "generative_ui": {"enabled": True},
                "ask_user_questions": {"enabled": True}
            }
        }
    }

    # Delete existing if present then recreate
    existing_agents = make_request("/agents")
    if "data" in existing_agents:
        for a in existing_agents["data"]:
            if a.get("name") == "forge-researcher":
                make_request(f"/agents/{a['id']}", method="DELETE")

    agent_res = make_request("/agents", method="POST", data=agent_payload)
    if "error" in agent_res:
        print(f"  ❌ Error creating agent: {agent_res['error']}")
    else:
        print("  ✓ Created agent 'forge-researcher' with explicit Guided Autonomy Subagent hierarchy!")

    print("\n" + "=" * 60)
    print("🎉 GUIDED AUTONOMY SUBAGENTS ARE CONFIGURED!")
    print("=" * 60)

if __name__ == "__main__":
    setup()
