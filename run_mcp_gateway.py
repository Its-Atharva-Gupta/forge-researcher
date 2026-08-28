"""
Unified FastMCP SSE Gateway for ForgeResearcher
"""
from typing import Dict, Any, List, Optional
from fastmcp import FastMCP

from mcp_servers.arxiv_mcp.server import search_arxiv
from mcp_servers.scholar_mcp.server import search_semantic_scholar
from mcp_servers.kaggle_colab_mcp.server import open_google_colab_session, inspect_colab_and_kaggle_compute
from mcp_servers.latex_compiler_mcp.server import render_latex_manuscript, audit_scientific_claims
from mcp_servers.research_lab_mcp.server import profile_dataset, generate_publication_plots

mcp = FastMCP("forge-researcher-tools")

# Register using FastMCP's tool decorator pattern
mcp.tool()(search_arxiv)
mcp.tool()(search_semantic_scholar)
mcp.tool()(open_google_colab_session)
mcp.tool()(inspect_colab_and_kaggle_compute)
mcp.tool()(profile_dataset)
mcp.tool()(generate_publication_plots)
mcp.tool()(render_latex_manuscript)
mcp.tool()(audit_scientific_claims)

if __name__ == "__main__":
    mcp.run(transport="sse", host="127.0.0.1", port=8795)
