"""
Unified FastMCP SSE Gateway for ForgeResearcher
Serves full research suite including direct Kaggle GPU Cloud Compute execution:
- `run_experiment_on_kaggle_gpu`: Dispatches ML models to Kaggle NVIDIA T4 Dual-GPU/TPU compute.
- `get_kaggle_experiment_logs`: Fetches logs and results from running Kaggle GPU experiments.
- `inspect_kaggle_and_local_compute`: Profiles Kaggle Cloud GPU hardware.
- `search_huggingface_models` & `search_huggingface_datasets`: Hugging Face Hub tools.
- `search_arxiv` & `search_semantic_scholar`: Academic literature tools.
- `profile_dataset` & `generate_publication_plots`: Research lab tools.
- `render_latex_manuscript` & `audit_scientific_claims`: Conference manuscript synthesis.
"""
from typing import Dict, Any, List, Optional
from fastmcp import FastMCP

from mcp_servers.kaggle_colab_mcp.server import run_experiment_on_kaggle_gpu, get_kaggle_experiment_logs, inspect_kaggle_and_local_compute
from mcp_servers.huggingface_mcp.server import search_huggingface_models, search_huggingface_datasets, search_huggingface_spaces
from mcp_servers.arxiv_mcp.server import search_arxiv
from mcp_servers.scholar_mcp.server import search_semantic_scholar
from mcp_servers.latex_compiler_mcp.server import render_latex_manuscript, audit_scientific_claims
from mcp_servers.research_lab_mcp.server import profile_dataset, generate_publication_plots

mcp = FastMCP("forge-researcher-tools")

# 1. Kaggle Remote Cloud GPU/TPU Execution Tools
mcp.tool()(run_experiment_on_kaggle_gpu)
mcp.tool()(get_kaggle_experiment_logs)
mcp.tool()(inspect_kaggle_and_local_compute)

# 2. Hugging Face Tools
mcp.tool()(search_huggingface_models)
mcp.tool()(search_huggingface_datasets)
mcp.tool()(search_huggingface_spaces)

# 3. Literature Tools
mcp.tool()(search_arxiv)
mcp.tool()(search_semantic_scholar)

# 4. Lab & Evaluation Tools
mcp.tool()(profile_dataset)
mcp.tool()(generate_publication_plots)

# 5. Paper Writing & Rigor Audit Tools
mcp.tool()(render_latex_manuscript)
mcp.tool()(audit_scientific_claims)

if __name__ == "__main__":
    mcp.run(transport="sse", host="127.0.0.1", port=8795)
