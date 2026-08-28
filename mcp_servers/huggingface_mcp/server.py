"""
Hugging Face MCP Server
Exposes tools to search models, datasets, spaces, and papers on Hugging Face Hub.
"""
from typing import Dict, Any, List, Optional
from fastmcp import FastMCP
from huggingface_hub import HfApi

mcp = FastMCP("HuggingFaceServer")
api = HfApi()

def search_huggingface_models(query: str, limit: int = 5) -> Dict[str, Any]:
    """Search machine learning models on the Hugging Face Hub (e.g. LLMs, embeddings, vision models)."""
    try:
        models = api.list_models(search=query, limit=limit, sort="downloads")
        results = []
        for m in models:
            results.append({
                "id": m.id,
                "author": m.author,
                "downloads": m.downloads,
                "likes": m.likes,
                "pipeline_tag": m.pipeline_tag,
                "url": f"https://huggingface.co/{m.id}"
            })
        return {"success": True, "count": len(results), "models": results, "source": "huggingface_hub_api"}
    except Exception as e:
        return {"error": f"Hugging Face model search failed: {str(e)}"}

def search_huggingface_datasets(query: str, limit: int = 5) -> Dict[str, Any]:
    """Search scientific and ML datasets on Hugging Face Hub."""
    try:
        datasets = api.list_datasets(search=query, limit=limit, sort="downloads")
        results = []
        for d in datasets:
            results.append({
                "id": d.id,
                "author": d.author,
                "downloads": d.downloads,
                "likes": d.likes,
                "url": f"https://huggingface.co/datasets/{d.id}"
            })
        return {"success": True, "count": len(results), "datasets": results, "source": "huggingface_hub_api"}
    except Exception as e:
        return {"error": f"Hugging Face dataset search failed: {str(e)}"}

def search_huggingface_spaces(query: str, limit: int = 5) -> Dict[str, Any]:
    """Search interactive demo spaces on Hugging Face Hub."""
    try:
        spaces = api.list_spaces(search=query, limit=limit, sort="likes")
        results = []
        for s in spaces:
            results.append({
                "id": s.id,
                "author": s.author,
                "likes": s.likes,
                "url": f"https://huggingface.co/spaces/{s.id}"
            })
        return {"success": True, "count": len(results), "spaces": results, "source": "huggingface_hub_api"}
    except Exception as e:
        return {"error": f"Hugging Face spaces search failed: {str(e)}"}

if __name__ == "__main__":
    mcp.tool()(search_huggingface_models)
    mcp.tool()(search_huggingface_datasets)
    mcp.tool()(search_huggingface_spaces)
    mcp.run()
