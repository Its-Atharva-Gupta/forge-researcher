"""
Google Scholar & Semantic Scholar Dedicated MCP Server (Adapted from JackKuo666/Google-Scholar-MCP-Server)
Provides citation graph tracking, author searches, and publication venue lookups.
"""
from typing import Dict, Any, List, Optional
import urllib.parse
import urllib.request
import json
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("ScholarServer")

@mcp.tool()
def search_semantic_scholar(query: str, limit: int = 5) -> Dict[str, Any]:
    """
    Search academic literature on Semantic Scholar API for citation counts and open-access papers.
    """
    encoded = urllib.parse.quote(query)
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={encoded}&limit={limit}&fields=title,authors,year,citationCount,abstract,openAccessPdf"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ForgeResearcher/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        papers = []
        for item in data.get("data", []):
            papers.append({
                "title": item.get("title"),
                "year": item.get("year"),
                "citationCount": item.get("citationCount", 0),
                "authors": [a.get("name") for a in item.get("authors", [])],
                "abstract": item.get("abstract", "")[:300] + "..." if item.get("abstract") else "",
                "pdf_url": item.get("openAccessPdf", {}).get("url") if item.get("openAccessPdf") else None
            })
        return {"success": True, "count": len(papers), "papers": papers}
    except Exception as e:
        return {"error": f"Semantic Scholar lookup failed: {str(e)}"}

if __name__ == "__main__":
    mcp.run()
