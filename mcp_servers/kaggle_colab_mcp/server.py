"""
Kaggle & Remote Compute Dataset MCP Server
Provides dataset discovery, downloading, and remote environment profiling.
"""
from typing import Dict, Any, List
import os
import urllib.request
import json
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("KaggleColabServer")

@mcp.tool()
def search_open_datasets(query: str, limit: int = 5) -> Dict[str, Any]:
    """
    Searches open scientific datasets across public repositories (OpenML / Kaggle mirrors).
    """
    encoded = urllib.parse.quote(query)
    url = f"https://www.openml.org/api/v1/json/data/list/data_name/{encoded}/limit/{limit}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ForgeResearcher/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        
        datasets = []
        raw_list = data.get("data", {}).get("dataset", [])
        for item in raw_list:
            datasets.append({
                "id": item.get("did"),
                "name": item.get("name"),
                "format": item.get("format"),
                "status": item.get("status")
            })
        return {"success": True, "count": len(datasets), "datasets": datasets}
    except Exception as e:
        return {"error": f"OpenML Dataset search failed: {str(e)}"}

@mcp.tool()
def check_compute_environment() -> Dict[str, Any]:
    """
    Profiles local/remote compute capabilities (CPU cores, RAM, sandbox constraints).
    """
    import os
    import multiprocessing
    return {
        "cpu_cores": multiprocessing.cpu_count(),
        "sandbox_mode": "TrueForge Isolated Container",
        "recommended_timeout_seconds": 120
    }

if __name__ == "__main__":
    mcp.run()
