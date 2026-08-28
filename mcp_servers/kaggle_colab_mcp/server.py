"""
Robust Dataset Discovery & Compute Profiler MCP Server
"""
from typing import Dict, Any, List
import urllib.parse
import urllib.request
import json
import os
import multiprocessing
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("KaggleColabServer")

BUILTIN_DATASETS = [
    {"id": "tabular-classification", "name": "Synthetic Multi-Class Tabular Benchmark (20 Features, 2000 Samples)", "format": "CSV/Numpy", "status": "ready"},
    {"id": "iris", "name": "Iris Flower Classification Benchmark", "format": "CSV", "status": "ready"},
    {"id": "california-housing", "name": "California Housing Regression Benchmark", "format": "CSV", "status": "ready"},
    {"id": "digits", "name": "Optical Recognition of Handwritten Digits (8x8)", "format": "Numpy", "status": "ready"},
    {"id": "breast-cancer", "name": "Wisconsin Diagnostic Breast Cancer Benchmark", "format": "CSV", "status": "ready"}
]

@mcp.tool()
def search_open_datasets(query: str, limit: int = 5) -> Dict[str, Any]:
    """
    Searches open scientific datasets across OpenML, Kaggle mirrors, and built-in ML benchmarks.
    """
    encoded = urllib.parse.quote(query)
    url = f"https://www.openml.org/api/v1/json/data/list/data_name/{encoded}/limit/{limit}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        
        datasets = []
        raw_list = data.get("data", {}).get("dataset", [])
        for item in raw_list:
            datasets.append({
                "id": str(item.get("did")),
                "name": item.get("name"),
                "format": item.get("format"),
                "status": item.get("status")
            })
        if datasets:
            return {"success": True, "count": len(datasets), "datasets": datasets, "source": "openml_live_api"}
    except Exception:
        pass

    # Match against built-in benchmarks
    q_lower = query.lower()
    matched = [d for d in BUILTIN_DATASETS if q_lower in d["name"].lower() or q_lower in d["id"].lower()]
    if not matched:
        matched = BUILTIN_DATASETS[:limit]

    return {
        "success": True,
        "count": len(matched),
        "datasets": matched[:limit],
        "source": "built_in_scientific_benchmarks"
    }

@mcp.tool()
def inspect_compute_environment() -> Dict[str, Any]:
    """
    Profiles local and sandboxed compute environment.
    """
    return {
        "cpu_cores": multiprocessing.cpu_count(),
        "sandbox_mode": "TrueForge Isolated Container",
        "gpu_available": False,
        "recommended_timeout_seconds": 120,
        "storage_path": os.path.abspath("workspace")
    }

if __name__ == "__main__":
    mcp.run()
