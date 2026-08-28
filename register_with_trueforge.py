"""
1-Command Auto-Registration for TrueForge
Registers `forge-researcher-tools` with `preload: true` so all research tools are directly accessible.
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
    print("⚡ CONFIGURING TRUEFORGE AGENT WITH PRELOADED MCP TOOLS")
    print("=" * 60)

    # 1. Connect
    print("\n[1/3] Connecting to TrueForge on http://localhost:8790...")
    mcp_check = make_request("/settings/mcp-servers")
    if "error" in mcp_check:
        print(f"  ❌ Cannot connect to TrueForge: {mcp_check['error']}")
        return False
    print("  ✓ Connected successfully to TrueForge runtime.")

    # 2. Register MCP Server
    print("\n[2/3] Registering 'forge-researcher-tools' in TrueForge...")
    mcp_payload = {
        "manifest": {
            "type": "remote",
            "name": "forge-researcher-tools",
            "url": "http://127.0.0.1:8795/sse",
            "description": "Complete research toolkit: arXiv, Scholar, Kaggle/OpenML datasets, plotting, LaTeX drafting, and Level-2 rigor audit."
        }
    }
    mcp_res = make_request("/settings/mcp-servers", method="PUT", data=mcp_payload)
    if "error" in mcp_res:
        print(f"  ❌ Error registering MCP server: {mcp_res['error']}")
    else:
        print("  ✓ Registered 'forge-researcher-tools' MCP server!")

    # 3. Detect Model
    providers_res = make_request("/settings/model-providers")
    model_name = "deepseek/deepseek"
    if "data" in providers_res and len(providers_res["data"]) > 0:
        first_prov = providers_res["data"][0]
        prov_name = first_prov.get("name")
        models = first_prov.get("manifest", {}).get("models", [])
        if models:
            model_name = f"{prov_name}/{models[0].get('name')}"

    print(f"\n[3/3] Registering 'forge-researcher' Agent (with eager tool preloading)...")
    
    agent_payload = {
        "name": "forge-researcher",
        "manifest": {
            "model": {
                "name": model_name,
                "params": {"reasoning_effort": "minimal"}
            },
            "instructions": (
                "You are 'forge-researcher', an autonomous empirical ML research harness.\n\n"
                "YOUR WORKFLOW:\n"
                "1. When given a research goal, use `search_arxiv_papers` and `search_academic_citations` to pull real literature.\n"
                "2. When asked about datasets or Kaggle access, use `discover_open_datasets` and `inspect_compute_environment`.\n"
                "3. Formulate an empirical hypothesis matrix (3 trials) and compute budget.\n"
                "4. APPROVAL GATE #1: Pause and ask user for explicit approval before running compute.\n"
                "5. Once approved, write custom Python experiment scripts in `workspace/` and execute them in the sandbox.\n"
                "6. Emit `workspace/results.tsv` and call `generate_academic_figures` to produce publication charts.\n"
                "7. Call `compile_latex_paper` to compile `workspace/paper.tex`.\n"
                "8. Call `verify_scientific_claims_audit` to perform Level-2 fact-checking against raw logs.\n"
                "9. APPROVAL GATE #2: Pause and ask user for approval before exporting the final PDF manuscript."
            ),
            "mcp_servers": [
                {
                    "name": "forge-researcher-tools",
                    "enable_tools": ["@all"],
                    "preload": True,
                    "require_approval_for_tools": []
                }
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
        print("  ✓ Created agent 'forge-researcher' with preload: true!")

    print("\n" + "=" * 60)
    print("🎉 SUCCESS! ForgeResearcher is updated with direct tool preloading.")
    print("👉 Open http://localhost:8790, start a NEW chat session with 'forge-researcher'!")
    print("=" * 60)

if __name__ == "__main__":
    setup()
