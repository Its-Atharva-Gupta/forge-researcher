"""
Auto-Register ForgeResearcher with Kaggle Cloud Execution Tools
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
    print("⚡ UPDATING TRUEFORGE AGENT WITH KAGGLE CLOUD KERNEL EXECUTION")
    print("=" * 60)

    # 1. Register server
    mcp_payload = {
        "manifest": {
            "type": "remote",
            "name": "forge-researcher-tools",
            "url": "http://127.0.0.1:8795/sse",
            "description": "Unified research tools: Kaggle search & cloud kernel execution, arXiv papers, Scholar citations, Plotting, LaTeX compiler, and Level-2 rigor auditor."
        }
    }
    make_request("/settings/mcp-servers", method="PUT", data=mcp_payload)

    # 2. Detect Model
    providers_res = make_request("/settings/model-providers")
    model_name = "deepseek/deepseek"
    if "data" in providers_res and len(providers_res["data"]) > 0:
        first_prov = providers_res["data"][0]
        prov_name = first_prov.get("name")
        models = first_prov.get("manifest", {}).get("models", [])
        if models:
            model_name = f"{prov_name}/{models[0].get('name')}"

    print(f"\nRegistering 'forge-researcher' Agent...")
    
    agent_payload = {
        "name": "forge-researcher",
        "manifest": {
            "model": {
                "name": model_name,
                "params": {"reasoning_effort": "minimal"}
            },
            "instructions": (
                "You are 'forge-researcher', an autonomous empirical ML research assistant with local and remote cloud execution tools.\n\n"
                "YOUR ATTACHED RESEARCH TOOLS:\n"
                "- `search_kaggle_datasets`: Call this to discover Kaggle datasets, competitions, and scientific benchmarks.\n"
                "- `execute_kaggle_kernel`: Call this to push and run experiment code on Kaggle's remote cloud compute (with GPU/TPU support).\n"
                "- `get_kaggle_kernel_status`: Call this to check the execution status of a remote Kaggle kernel.\n"
                "- `search_arxiv_papers`: Call this when searching for academic papers on arXiv.\n"
                "- `search_academic_citations`: Call this for Google Scholar / CrossRef citations.\n"
                "- `inspect_compute_environment`: Call this to inspect CPU/RAM and compute boundaries.\n"
                "- `analyze_dataset_profile`: Call this to profile dataset statistics and shapes.\n"
                "- `generate_academic_figures`: Call this to plot loss curves and bar charts.\n"
                "- `compile_latex_paper`: Call this to draft 2-column LaTeX conference papers.\n"
                "- `verify_scientific_claims_audit`: Call this to perform Level-2 fact-checking.\n\n"
                "WHEN ASKED ABOUT KAGGLE COMPUTE OR NOTEBOOKS:\n"
                "You CAN run experiments on Kaggle compute using `execute_kaggle_kernel` (which pushes and runs scripts/notebooks via the Kaggle Kernels API) or inside TrueForge's isolated container sandbox."
            ),
            "mcp_servers": [
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
        print("  ✓ Created agent 'forge-researcher' with Kaggle Cloud Kernel Execution!")

    print("\n" + "=" * 60)
    print("🎉 KAGGLE CLOUD KERNEL EXECUTION IS LIVE!")
    print("=" * 60)

if __name__ == "__main__":
    setup()
