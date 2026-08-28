"""
Auto-Register ForgeResearcher with Direct Kaggle GPU Cloud Compute & Research Tools
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
    print("⚡ CONFIGURING TRUEFORGE WITH DIRECT KAGGLE CLOUD GPU EXECUTION")
    print("=" * 60)

    # 1. Connect
    mcp_check = make_request("/settings/mcp-servers")
    if "error" in mcp_check:
        print(f"  ❌ Cannot connect to TrueForge: {mcp_check['error']}")
        return False

    # 2. Register Authenticated Remote Kaggle MCP Server (for datasets & competitions)
    kaggle_payload = {
        "manifest": {
            "type": "remote",
            "name": "kaggle",
            "url": "https://www.kaggle.com/mcp",
            "description": "Official Kaggle MCP Server: Search/download datasets, competitions, and models.",
            "auth": {
                "type": "header",
                "headers": {
                    "Authorization": f"Bearer {KAGGLE_TOKEN}"
                }
            }
        }
    }
    make_request("/settings/mcp-servers", method="PUT", data=kaggle_payload)

    # 3. Register local FastMCP Tool Gateway (Kaggle Cloud GPU Dispatcher + Research Suite)
    tools_payload = {
        "manifest": {
            "type": "remote",
            "name": "forge-researcher-tools",
            "url": "http://127.0.0.1:8795/sse",
            "description": "Kaggle GPU Dispatcher (NVIDIA T4 Dual-GPU), Hugging Face, arXiv, Plotting, LaTeX compiler, and Level-2 rigor auditor."
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

    print(f"\nRegistering 'forge-researcher' Agent with Kaggle Cloud GPU Compute...")
    
    agent_instructions = (
        "You are 'forge-researcher', an autonomous empirical ML research harness operating under GUIDED AUTONOMY.\n\n"
        f"AUTHENTICATED KAGGLE USER: {KAGGLE_USER} (Cloud GPU Execution ENABLED)\n\n"
        "## KAGGLE REMOTE CLOUD GPU DISPATCH (Use this whenever the user wants GPU compute!):\n"
        "- `run_experiment_on_kaggle_gpu`: Pushes and runs your experiment code directly on remote Kaggle cloud NVIDIA T4 Dual-GPUs / TPUs. Returns the live Kaggle notebook URL.\n"
        "- `get_kaggle_experiment_logs`: Fetches execution logs, loss numbers, and artifact files from the running Kaggle GPU kernel.\n"
        "- `inspect_kaggle_and_local_compute`: Checks your Kaggle GPU quotas and hardware specs.\n\n"
        "## OTHER ATTACHED TOOLSETS:\n"
        "- Hugging Face: `search_huggingface_models`, `search_huggingface_datasets`, `search_huggingface_spaces`.\n"
        "- Literature: `search_arxiv` (arXiv HTTPS query) and `search_semantic_scholar`.\n"
        "- Lab & Paper: `profile_dataset`, `generate_publication_plots`, `render_latex_manuscript`, and `audit_scientific_claims`.\n\n"
        "## GUIDED AUTONOMY SUBAGENTS (Orchestrated via `create_sub_agent`):\n"
        "- `eval-worker`: Dispatches experiments to Kaggle Cloud GPU via `run_experiment_on_kaggle_gpu` or executes in local sandbox.\n"
        "- `plot-worker`: Publication plotting (emits `figures/`).\n"
        "- `write-worker`: LaTeX paper synthesis (emits `paper.tex`).\n"
        "- `rigor-worker`: Level-2 empirical fact-checker (emits `rigor_audit.json`).\n\n"
        "## APPROVAL GATES:\n"
        "- APPROVAL GATE #1: Formulate 3-trial hypothesis matrix & compute budget, then pause for user approval before GPU dispatch.\n"
        "- APPROVAL GATE #2: Present Level-2 audit results and pause for user approval before finalizing PDF manuscript."
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

    existing_agents = make_request("/agents")
    if "data" in existing_agents:
        for a in existing_agents["data"]:
            if a.get("name") == "forge-researcher":
                make_request(f"/agents/{a['id']}", method="DELETE")

    agent_res = make_request("/agents", method="POST", data=agent_payload)
    if "error" in agent_res:
        print(f"  ❌ Error creating agent: {agent_res['error']}")
    else:
        print("  ✓ Created agent 'forge-researcher' with Kaggle Cloud GPU execution!")

    print("\n" + "=" * 60)
    print("🎉 KAGGLE CLOUD GPU EXECUTION IS FULLY CONFIGURED!")
    print("=" * 60)

if __name__ == "__main__":
    setup()
