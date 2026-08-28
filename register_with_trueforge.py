"""
Auto-Register ForgeResearcher with Official Kaggle MCP Endpoint & Research Tools
Registers:
1. `kaggle` (Official Remote MCP endpoint: https://www.kaggle.com/mcp)
2. `forge-researcher-tools` (Local FastMCP SSE suite for arXiv, LaTeX, plotting, and rigor audit)
"""
import os
import json
import urllib.request
import urllib.error

TRUEFORGE_API = "http://localhost:8790/api/v1"

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
    print("⚡ CONNECTING OFFICIAL KAGGLE MCP SERVER & RESEARCH TOOLKIT")
    print("=" * 60)

    # 1. Connect
    mcp_check = make_request("/settings/mcp-servers")
    if "error" in mcp_check:
        print(f"  ❌ Cannot connect to TrueForge: {mcp_check['error']}")
        return False

    # 2. Register Official Remote Kaggle MCP Server (https://www.kaggle.com/mcp)
    print("\n[1/3] Registering official remote Kaggle MCP server (https://www.kaggle.com/mcp)...")
    kaggle_payload = {
        "manifest": {
            "type": "remote",
            "name": "kaggle",
            "url": "https://www.kaggle.com/mcp",
            "description": "Official Kaggle MCP Server: Search & download datasets, run & manage notebooks/kernels, enter competitions, and create model benchmarks."
        }
    }
    k_res = make_request("/settings/mcp-servers", method="PUT", data=kaggle_payload)
    if "error" in k_res:
        print(f"  ⚠️  Kaggle remote register response: {k_res['error']}")
    else:
        print("  ✓ Registered official 'kaggle' MCP server (https://www.kaggle.com/mcp)!")

    # 3. Register local Research Tools (arXiv, plotting, LaTeX, rigor audit)
    print("\n[2/3] Registering 'forge-researcher-tools' in TrueForge...")
    tools_payload = {
        "manifest": {
            "type": "remote",
            "name": "forge-researcher-tools",
            "url": "http://127.0.0.1:8795/sse",
            "description": "Research toolkit: arXiv search, academic citations, plotting, LaTeX compilation, and Level-2 rigor auditor."
        }
    }
    t_res = make_request("/settings/mcp-servers", method="PUT", data=tools_payload)
    if "error" in t_res:
        print(f"  ❌ Error registering research tools: {t_res['error']}")
    else:
        print("  ✓ Registered 'forge-researcher-tools' MCP server!")

    # 4. Detect Model
    providers_res = make_request("/settings/model-providers")
    model_name = "deepseek/deepseek"
    if "data" in providers_res and len(providers_res["data"]) > 0:
        first_prov = providers_res["data"][0]
        prov_name = first_prov.get("name")
        models = first_prov.get("manifest", {}).get("models", [])
        if models:
            model_name = f"{prov_name}/{models[0].get('name')}"

    print(f"\n[3/3] Registering 'forge-researcher' Agent with official Kaggle & Research tools...")
    
    agent_payload = {
        "name": "forge-researcher",
        "manifest": {
            "model": {
                "name": model_name,
                "params": {"reasoning_effort": "minimal"}
            },
            "instructions": (
                "You are 'forge-researcher', an autonomous empirical ML research assistant.\n\n"
                "YOUR ATTACHED CAPABILITIES:\n"
                "1. `kaggle` MCP Server (https://www.kaggle.com/mcp):\n"
                "   - Notebooks: Start, manage, and retrieve outputs for Kaggle Notebooks & GPU/TPU compute.\n"
                "   - Datasets: Search, list files, and inspect metadata.\n"
                "   - Competitions: Search competitions, download files, and submit solutions.\n"
                "   - Models & Benchmarking: Manage Kaggle models and benchmarks.\n\n"
                "2. `forge-researcher-tools` MCP Server:\n"
                "   - `search_arxiv_papers`: Query arXiv API for research papers.\n"
                "   - `search_academic_citations`: Query CrossRef & Semantic Scholar citations.\n"
                "   - `inspect_compute_environment`: Profile local sandbox & memory.\n"
                "   - `analyze_dataset_profile`: Profile CSV/TSV statistics & shapes.\n"
                "   - `generate_academic_figures`: Draw dual-axis loss curves and benchmark bar charts.\n"
                "   - `compile_latex_paper`: Draft 2-column conference LaTeX papers.\n"
                "   - `verify_scientific_claims_audit`: Perform Level-2 empirical fact-checking."
            ),
            "mcp_servers": [
                {"name": "kaggle", "enable_tools": ["@all"], "preload": False},
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
        print("  ✓ Created agent 'forge-researcher' with official Kaggle MCP integration!")

    print("\n" + "=" * 60)
    print("🎉 OFFICIAL KAGGLE MCP SERVER & RESEARCH TOOLKIT ARE READY!")
    print("=" * 60)

if __name__ == "__main__":
    setup()
