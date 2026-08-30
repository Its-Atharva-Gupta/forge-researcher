"""
Unified FastMCP Research Tool Gateway
Exposes all ML Research, Literature, Dataset, SOTA Compute, and Subagent Delegation tools over SSE.
"""
from fastmcp import FastMCP
from mcp_servers.arxiv_mcp.server import search_arxiv
from mcp_servers.scholar_mcp.server import search_semantic_scholar
from mcp_servers.research_lab_mcp.server import (
    profile_dataset,
    generate_publication_plots
)
from mcp_servers.latex_compiler_mcp.server import (
    render_latex_manuscript,
    audit_scientific_claims
)
from mcp_servers.kaggle_mcp.server import (
    search_kaggle_datasets, 
    run_experiment_on_kaggle_gpu, 
    get_kaggle_experiment_logs,
    inspect_kaggle_and_local_compute
)
from mcp_servers.huggingface_mcp.server import (
    search_huggingface_models,
    search_huggingface_datasets,
    search_huggingface_spaces
)
from mcp_servers.subagent_telemetry.server import (
    delegate_subagent_task,
    complete_subagent_task
)

gateway = FastMCP(
    "forge-researcher-tools",
    instructions="Unified Autonomous Research MCP Suite for literature discovery, HF Hub search, Kaggle Cloud GPUs, plotting, LaTeX generation, and subagent hierarchy delegation."
)

# Subagent Hierarchy Delegation & Tracking Tools
gateway.tool(name="delegate_subagent_task", description="Delegates a bounded research sub-task to a specialized subagent (eval-worker, plot-worker, write-worker, rigor-worker) with an explicit prompt and contract.")(delegate_subagent_task)
gateway.tool(name="complete_subagent_task", description="Records successful completion of a delegated subagent task.")(complete_subagent_task)

# Kaggle Remote GPU / TPU Tools
gateway.tool(name="search_kaggle_datasets", description="Search scientific datasets on Kaggle.")(search_kaggle_datasets)
gateway.tool(name="run_experiment_on_kaggle_gpu", description="Push and execute standalone ML training script on Kaggle Cloud GPUs (NVIDIA T4 Dual / P100) or TPUs.")(run_experiment_on_kaggle_gpu)
gateway.tool(name="get_kaggle_experiment_logs", description="Retrieve live execution logs from a running or finished Kaggle experiment.")(get_kaggle_experiment_logs)
gateway.tool(name="inspect_kaggle_and_local_compute", description="Profile Kaggle Cloud GPU hardware quota and local cores.")(inspect_kaggle_and_local_compute)

# Hugging Face Hub Tools
gateway.tool(name="search_huggingface_models", description="Search pre-trained models on Hugging Face Hub.")(search_huggingface_models)
gateway.tool(name="search_huggingface_datasets", description="Search datasets on Hugging Face Hub.")(search_huggingface_datasets)
gateway.tool(name="search_huggingface_spaces", description="Search demo applications and spaces on Hugging Face Hub.")(search_huggingface_spaces)

# Literature, Profiling, Plotting & LaTeX Compilation Tools
gateway.tool(name="search_arxiv", description="Search scientific papers on arXiv API over HTTPS.")(search_arxiv)
gateway.tool(name="search_semantic_scholar", description="Search citation graph and academic papers via Semantic Scholar and CrossRef.")(search_semantic_scholar)
gateway.tool(name="profile_dataset", description="Generate distribution summaries and baseline ML predictions.")(profile_dataset)
gateway.tool(name="generate_publication_plots", description="Create publication-ready dual-axis training curves and comparison plots.")(generate_publication_plots)
gateway.tool(name="render_latex_manuscript", description="Compile clean 2-column LaTeX conference paper.")(render_latex_manuscript)
gateway.tool(name="audit_scientific_claims", description="Level-2 Rigor Auditor: fact-checks metrics in paper against raw logs.")(audit_scientific_claims)

if __name__ == "__main__":
    gateway.run(transport="sse", host="127.0.0.1", port=8795)
