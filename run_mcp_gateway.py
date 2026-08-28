"""
Unified FastMCP SSE Gateway for ForgeResearcher
Serves complete research toolkit:
- Hugging Face Models, Datasets & Spaces search
- Google Colab GPU session launcher
- Kaggle compute & dataset tools
- arXiv papers & CrossRef scholar citations
- Dataset profiling & academic dual-axis plotting
- LaTeX conference manuscript compiler & Level-2 rigor auditor
"""
from typing import Dict, Any, List, Optional
from fastmcp import FastMCP

from mcp_servers.huggingface_mcp.server import search_huggingface_models, search_huggingface_datasets, search_huggingface_spaces
from mcp_servers.arxiv_mcp.server import search_arxiv
from mcp_servers.scholar_mcp.server import search_semantic_scholar
from mcp_servers.kaggle_colab_mcp.server import open_google_colab_session, inspect_colab_and_kaggle_compute
from mcp_servers.latex_compiler_mcp.server import render_latex_manuscript, audit_scientific_claims
from mcp_servers.research_lab_mcp.server import profile_dataset, generate_publication_plots

mcp = FastMCP("forge-researcher-tools")

# 1. Hugging Face Tools
mcp.tool()(search_huggingface_models)
mcp.tool()(search_huggingface_datasets)
mcp.tool()(search_huggingface_spaces)

# 2. Google Colab & Compute Tools
mcp.tool()(open_google_colab_session)
mcp.tool()(inspect_colab_and_kaggle_compute)

# 3. Literature Search Tools
mcp.tool()(search_arxiv)
mcp.tool()(search_semantic_scholar)

# 4. Lab & Evaluation Tools
mcp.tool()(profile_dataset)
mcp.tool()(generate_publication_plots)

# 5. Paper Writing & Level-2 Rigor Audit Tools
mcp.tool()(render_latex_manuscript)
mcp.tool()(audit_scientific_claims)

if __name__ == "__main__":
    mcp.run(transport="sse", host="127.0.0.1", port=8795)
