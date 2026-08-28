"""
Auto-Register ForgeResearcher with Hugging Face, Kaggle, Colab & Research Tools
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
    print("⚡ CONFIGURING TRUEFORGE WITH HUGGING FACE, KAGGLE & RESEARCH SUITE")
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

    # 3. Register local Research & Hugging Face Tools
    tools_payload = {
        "manifest": {
            "type": "remote",
            "name": "forge-researcher-tools",
            "url": "http://127.0.0.1:8795/sse",
            "description": "Research toolkit: Hugging Face (Models/Datasets/Spaces), Google Colab, arXiv search, academic citations, plotting, LaTeX compilation, and Level-2 rigor auditor."
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

    print(f"\nRegistering 'forge-researcher' Agent with Hugging Face & Research tools...")
    
    agent_instructions = (
        "You are 'forge-researcher', an autonomous empirical ML research harness operating under GUIDED AUTONOMY.\n\n"
        f"AUTHENTICATED KAGGLE USER: {KAGGLE_USER}\n\n"
        "## ATTACHED TOOLSETS:\n"
        "1. **Hugging Face Hub Tools**:\n"
        "   - `search_huggingface_models`: Discover pretrained models, checkpoints, and weights.\n"
        "   - `search_huggingface_datasets`: Discover NLP, CV, tabular, and speech datasets.\n"
        "   - `search_huggingface_spaces`: Discover live Hugging Face Gradio/Streamlit spaces.\n"
        "2. **Google Colab & Compute Tools**:\n"
        "   - `open_google_colab_session`: Launch interactive browser Colab sessions with GPU/TPU.\n"
        "   - `inspect_colab_and_kaggle_compute`: Profile available remote compute tiers.\n"
        "3. **Literature & Citation Tools**:\n"
        "   - `search_arxiv`: Search arXiv papers over HTTPS.\n"
        "   - `search_semantic_scholar`: Query CrossRef & Semantic Scholar academic citations.\n"
        "4. **Lab & Rigor Tools**:\n"
        "   - `profile_dataset` & `generate_publication_plots`\n"
        "   - `render_latex_manuscript` & `audit_scientific_claims`\n\n"
        "## GUIDED AUTONOMY SUBAGENTS (Orchestrated via `create_sub_agent`):\n"
        "- `eval-worker`: Sandbox code execution & benchmark evaluation (emits `results.tsv`).\n"
        "- `plot-worker`: Publication plotting (emits `figures/`).\n"
        "- `write-worker`: LaTeX paper synthesis (emits `paper.tex`).\n"
        "- `rigor-worker`: Level-2 empirical fact-checker (emits `rigor_audit.json`).\n\n"
        "## APPROVAL GATES:\n"
        "- APPROVAL GATE #1: Propose hypothesis matrix & compute budget, then pause for user approval before execution.\n"
        "- APPROVAL GATE #2: Present Level-2 audit results and pause for user approval before finalizing manuscript."
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
        print("  ✓ Created agent 'forge-researcher' with Hugging Face integration!")

    print("\n" + "=" * 60)
    print("🎉 HUGGING FACE & RESEARCH SUITE ARE READY!")
    print("=" * 60)

if __name__ == "__main__":
    setup()
