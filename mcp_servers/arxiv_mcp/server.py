"""
arXiv Dedicated MCP Server (Adapted from blazickjp/arxiv-mcp-server)
Provides arXiv search, metadata parsing, and PDF/abstract extraction over HTTPS.
"""
from typing import Dict, Any, List
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("ArXivServer")

@mcp.tool()
def search_arxiv(query: str, max_results: int = 5) -> Dict[str, Any]:
    """Search arXiv papers by query keyword and return structured metadata."""
    encoded = urllib.parse.quote(query)
    url = f"https://export.arxiv.org/api/query?search_query=all:{encoded}&start=0&max_results={max_results}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ForgeResearcher/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
        root = ET.fromstring(data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        papers = []
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns)
            summary = entry.find('atom:summary', ns)
            published = entry.find('atom:published', ns)
            arxiv_id = entry.find('atom:id', ns)
            authors = [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns) if a.find('atom:name', ns) is not None]
            papers.append({
                "title": title.text.strip().replace('\n', ' ') if title is not None else "Untitled",
                "abstract": summary.text.strip().replace('\n', ' ') if summary is not None else "",
                "published": published.text if published is not None else "",
                "url": arxiv_id.text if arxiv_id is not None else "",
                "authors": authors
            })
        return {"success": True, "count": len(papers), "papers": papers}
    except Exception as e:
        return {"error": f"arXiv API error: {str(e)}"}

if __name__ == "__main__":
    mcp.run()
