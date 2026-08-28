"""
Auto-Register ForgeResearcher with Direct MCP Server Names
Registers each MCP server under its intuitive individual name:
- `kaggle-mcp` (with `search_kaggle_and_open_datasets` and `inspect_compute_environment`)
- `arxiv-mcp` (with `search_arxiv_papers`)
- `scholar-mcp` (with `search_academic_citations`)
- `research-lab-mcp` (with `analyze_dataset_profile` and `generate_academic_figures`)
- `latex-mcp` (with `compile_latex_paper` and `verify_scientific_claims_audit`)
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
    print("⚡ CONFIGURING TRUEFORGE WITH NAMED MCP SERVERS (INCLUDING KAGGLE-MCP)")
    print("=" * 60)

    # 1. Connect
    mcp_check = make_request("/settings/mcp-servers")
    if "error" in mcp_check:
        print(f"  ❌ Cannot connect to TrueForge: {mcp_check['error']}")
        return False

    # 2. Register named MCP servers pointing to the SSE gateway
    servers = [
        {"name": "kaggle-mcp", "desc": "Kaggle, OpenML & scientific benchmark dataset search and compute tools"},
        {"name": "arxiv-mcp", "desc": "arXiv literature search tool over HTTPS"},
        {"name": "scholar-mcp", "desc": "Google Scholar and CrossRef academic citation search"},
        {"name": "research-lab-mcp", "desc": "Dataset statistical profiling and dual-axis publication plotting"},
        {"name": "latex-mcp", "desc": "LaTeX conference paper compiler and Level-2 rigor auditor"},
        {"name": "forge-researcher-tools", "desc": "Unified research tools suite"}
    ]

    for s in servers:
        mcp_payload = {
            "manifest": {
                "type": "remote",
                "name": s["name"],
                "url": "http://127.0.0.1:8795/sse",
                "description": s["desc"]
            }
        }
        res = make_request("/settings/mcp-servers", method="PUT", data=mcp_payload)
        if "error" in res:
            print(f"  ❌ Error registering {s['name']}: {res['error']}")
        else:
            print(f"  ✓ Registered MCP server: {s['name']}")

    # 3. Detect Model
    providers_res = make_request("/settings/model-providers")
    model_name = "deepseek/deepseek"
    if "data" in providers_res and len(providers_res["data"]) > 0:
        first_prov = providers_res["data"][0]
        prov_name = first_prov.get("name")
        models = first_prov.get("manifest", {}).get("models", [])
        if models:
            model_name = f"{prov_name}/{models[0].get('name')}"

    print(f"\nRegistering 'forge-researcher' Agent with all named MCP servers...")
    
    agent_payload = {
        "name": "forge-researcher",
        "manifest": {
            "model": {
                "name": model_name,
                "params": {"reasoning_effort": "minimal"}
            },
            "instructions": (
                "You are 'forge-researcher', an autonomous empirical ML research assistant with direct tool integrations.\n\n"
                "YOUR ATTACHED TOOLS & SERVERS:\n"
                "- `kaggle-mcp` (or `forge-researcher-tools`): Tools `discover_open_datasets` (searches Kaggle/OpenML/benchmarks) and `inspect_compute_environment`.\n"
                "- `arxiv-mcp`: Tool `search_arxiv_papers` (searches arXiv literature over HTTPS).\n"
                "- `scholar-mcp`: Tool `search_academic_citations` (searches Google Scholar and CrossRef).\n"
                "- `research-lab-mcp`: Tools `analyze_dataset_profile` and `generate_academic_figures`.\n"
                "- `latex-mcp`: Tools `compile_latex_paper` and `verify_scientific_claims_audit`.\n\n"
                "WHEN ASKED ABOUT KAGGLE, PAPERS, OR DATASETS:\n"
                "- ALWAYS directly call `discover_open_datasets` or `search_arxiv_papers`.\n"
                "- Do NOT attempt to list 'deferred-tools' because all your tools are already directly attached and ready to invoke."
            ),
            "mcp_servers": [
                {"name": "kaggle-mcp", "enable_tools": ["@all"], "preload": True},
                {"name": "arxiv-mcp", "enable_tools": ["@all"], "preload": True},
                {"name": "scholar-mcp", "enable_tools": ["@all"], "preload": True},
                {"name": "research-lab-mcp", "enable_tools": ["@all"], "preload": True},
                {"name": "latex-mcp", "enable_tools": ["@all"], "preload": True},
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
        print("  ✓ Created agent 'forge-researcher' with direct named MCP servers!")

    print("\n" + "=" * 60)
    print("🎉 ALL NAMED MCP SERVERS (INCLUDING KAGGLE-MCP) ARE LIVE!")
    print("=" * 60)

if __name__ == "__main__":
    setup()
