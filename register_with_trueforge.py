"""
Auto-Register ForgeResearcher with Kaggle Cloud GPU & Research Tools
"""
import os
import json
import urllib.request
import urllib.error

TRUEFORGE_API = "http://localhost:8790/api/v1"

# Automatically read Kaggle credentials from ~/.kaggle/kaggle.json or environment
KAGGLE_USER = os.environ.get("KAGGLE_USERNAME")
KAGGLE_TOKEN = os.environ.get("KAGGLE_KEY")

if not KAGGLE_USER or not KAGGLE_TOKEN:
    kaggle_json_path = os.path.expanduser("~/.kaggle/kaggle.json")
    if os.path.exists(kaggle_json_path):
        try:
            with open(kaggle_json_path, "r") as f:
                k_data = json.load(f)
                KAGGLE_USER = k_data.get("username")
                KAGGLE_TOKEN = k_data.get("key")
        except Exception:
            pass

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
    print("=" * 65)
    print("⚡ AUTO-CONFIGURING TRUEFORGE HARNESS FOR FORGERESEARCHER")
    print("=" * 65)

    # 1. Connect
    mcp_check = make_request("/settings/mcp-servers")
    if "error" in mcp_check:
        print(f"  ❌ Cannot connect to TrueForge at http://localhost:8790: {mcp_check['error']}")
        return False
    print("  ✓ Connected to TrueForge runtime.")

    # 2. Register Authenticated Remote Kaggle MCP Server (if credentials present)
    if KAGGLE_TOKEN:
        print(f"  ✓ Kaggle credentials detected for user: {KAGGLE_USER or 'authenticated'}")
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
    else:
        print("  ℹ️  No Kaggle credentials found (running in local sandbox mode).")

    # 3. Register local FastMCP Tool Gateway (Kaggle Cloud GPU Dispatcher + Research Suite)
    tools_payload = {
        "manifest": {
            "type": "remote",
            "name": "forge-researcher-tools",
            "url": "http://127.0.0.1:8795/sse",
            "description": "Kaggle GPU Dispatcher (NVIDIA T4 Dual-GPU), Hugging Face Hub, arXiv, Plotting, LaTeX compiler, and Level-2 rigor auditor."
        }
    }
    make_request("/settings/mcp-servers", method="PUT", data=tools_payload)
    print("  ✓ Registered 'forge-researcher-tools' FastMCP server.")

    # 4. Detect Model
    providers_res = make_request("/settings/model-providers")
    model_name = "deepseek/deepseek"
    if "data" in providers_res and len(providers_res["data"]) > 0:
        first_prov = providers_res["data"][0]
        prov_name = first_prov.get("name")
        models = first_prov.get("manifest", {}).get("models", [])
        if models:
            model_name = f"{prov_name}/{models[0].get('name')}"

    print(f"  ✓ Using Model Provider: {model_name}")
    print(f"\nRegistering 'forge-researcher' Agent...")
    
    agent_instructions = (
        "You are 'forge-researcher', an autonomous empirical ML research harness operating under GUIDED AUTONOMY.\n\n"
        "## CLOUD & LOCAL COMPUTE TOOLS:\n"
        "- `run_experiment_on_kaggle_gpu`: Dispatches training scripts directly to Kaggle's remote cloud NVIDIA T4 Dual-GPUs / TPUs.\n"
        "- `get_kaggle_experiment_logs`: Fetches execution logs, loss curves, and artifact files from running GPU kernels.\n"
        "- `inspect_kaggle_and_local_compute`: Checks your compute hardware specs and quotas.\n\n"
        "## ATTACHED RESEARCH TOOLSETS:\n"
        "- Kaggle Datasets: `search_kaggle_datasets` (Queries Kaggle & scientific datasets).\n"
        "- Hugging Face Hub: `search_huggingface_models`, `search_huggingface_datasets`, `search_huggingface_spaces`.\n"
        "- Literature: `search_arxiv` (arXiv HTTPS query) and `search_semantic_scholar` (CrossRef citation index).\n"
        "- Lab & Paper: `profile_dataset`, `generate_publication_plots`, `render_latex_manuscript`, and `audit_scientific_claims`.\n\n"
        "## GUIDED AUTONOMY SUBAGENTS (Orchestrated via `create_sub_agent`):\n"
        "- `eval-worker`: Dispatches experiments to Kaggle Cloud GPU via `run_experiment_on_kaggle_gpu` or executes in local sandbox (emits `results.tsv`).\n"
        "- `plot-worker`: Publication plotting (emits `figures/`).\n"
        "- `write-worker`: LaTeX paper synthesis (emits `paper.tex`).\n"
        "- `rigor-worker`: Level-2 empirical fact-checker (emits `rigor_audit.json`).\n\n"
        "## APPROVAL GATES:\n"
        "- APPROVAL GATE #1: Formulate 3-trial hypothesis matrix & compute budget, then pause for user approval before compute execution.\n"
        "- APPROVAL GATE #2: Present Level-2 audit results and pause for user approval before finalizing PDF manuscript."
    )

    mcp_servers_list = [{"name": "forge-researcher-tools", "enable_tools": ["@all"], "preload": True}]
    if KAGGLE_TOKEN:
        mcp_servers_list.append({"name": "kaggle", "enable_tools": ["@all"], "preload": True})

    agent_payload = {
        "name": "forge-researcher",
        "manifest": {
            "model": {
                "name": model_name,
                "params": {"reasoning_effort": "minimal"}
            },
            "instructions": agent_instructions,
            "mcp_servers": mcp_servers_list,
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
        print("  ✓ Created agent 'forge-researcher' successfully!")

    print("=" * 65)
    print("🎉 SETUP COMPLETE! OPEN http://localhost:8790 TO START RESEARCHING")
    print("=" * 65)

if __name__ == "__main__":
    setup()
