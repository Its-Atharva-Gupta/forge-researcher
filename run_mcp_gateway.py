"""
Unified FastMCP SSE Gateway for ForgeResearcher
Serves dedicated research tools over persistent SSE:
- `search_kaggle_datasets`: Discovers Kaggle datasets and scientific benchmarks.
- `execute_kaggle_kernel`: Runs experiment scripts on remote Kaggle cloud compute (GPU/TPU).
- `get_kaggle_kernel_status`: Checks logs and status of running Kaggle kernels.
- `search_arxiv_papers`: Searches arXiv papers over HTTPS.
- `search_academic_citations`: Searches CrossRef & Semantic Scholar citations.
- `inspect_compute_environment`: Profiles local CPU sandbox and remote Kaggle dispatch.
- `analyze_dataset_profile`: Profiles CSV/TSV stats and shapes.
- `generate_academic_figures`: Dual-axis publication plotting engine.
- `compile_latex_paper`: 2-column LaTeX conference manuscript compiler.
- `verify_scientific_claims_audit`: Level-2 Scientific Rigor Fact-Checker.
"""
from typing import Dict, Any, List, Optional
from mcp.server.mcpserver import MCPServer

from mcp_servers.arxiv_mcp.server import search_arxiv
from mcp_servers.scholar_mcp.server import search_semantic_scholar
from mcp_servers.kaggle_colab_mcp.server import search_kaggle_datasets, execute_kaggle_kernel, get_kaggle_kernel_status, inspect_compute_environment
from mcp_servers.latex_compiler_mcp.server import render_latex_manuscript, audit_scientific_claims
from mcp_servers.research_lab_mcp.server import profile_dataset, generate_publication_plots

mcp = MCPServer("forge-researcher-tools")

@mcp.tool()
def search_kaggle_datasets(query: str, max_results: int = 5) -> Dict[str, Any]:
    """Search Kaggle, competition benchmarks, and open scientific datasets."""
    return search_kaggle_datasets(query, max_results)

@mcp.tool()
def execute_kaggle_kernel(
    kernel_title: str,
    code_content: str,
    enable_gpu: bool = False,
    dataset_sources: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Execute Python ML experiment on Kaggle remote cloud compute (with GPU support)."""
    return execute_kaggle_kernel(kernel_title, code_content, enable_gpu, dataset_sources)

@mcp.tool()
def get_kaggle_kernel_status(kernel_slug: str) -> Dict[str, Any]:
    """Check execution status of a Kaggle remote kernel."""
    return get_kaggle_kernel_status(kernel_slug)

@mcp.tool()
def search_arxiv_papers(query: str, max_results: int = 5) -> Dict[str, Any]:
    """Search arXiv papers by topic over HTTPS with failover cache."""
    return search_arxiv(query, max_results)

@mcp.tool()
def search_academic_citations(query: str, limit: int = 5) -> Dict[str, Any]:
    """Search academic literature and citations via CrossRef and Semantic Scholar."""
    return search_semantic_scholar(query, limit)

@mcp.tool()
def inspect_compute_environment() -> Dict[str, Any]:
    """Profile local sandbox and remote Kaggle cloud compute environment."""
    return inspect_compute_environment()

@mcp.tool()
def analyze_dataset_profile(dataset_path: str) -> Dict[str, Any]:
    """Profile CSV/TSV dataset stats and column types."""
    return profile_dataset(dataset_path)

@mcp.tool()
def generate_academic_figures(results_tsv_path: str, output_figure_dir: str) -> Dict[str, Any]:
    """Generate dual-axis publication loss and benchmark comparison plots."""
    return generate_publication_plots(results_tsv_path, output_figure_dir)

@mcp.tool()
def compile_latex_paper(
    title: str,
    authors: List[str],
    abstract: str,
    sections: Dict[str, str],
    figure_paths: List[str],
    output_tex_path: str
) -> Dict[str, Any]:
    """Compile 2-column LaTeX conference manuscript."""
    return render_latex_manuscript(title, authors, abstract, sections, figure_paths, output_tex_path)

@mcp.tool()
def verify_scientific_claims_audit(paper_tex_path: str, results_tsv_path: str) -> Dict[str, Any]:
    """Level-2 Scientific Rigor Fact-Checker verifying paper text matches raw metrics."""
    return audit_scientific_claims(paper_tex_path, results_tsv_path)

if __name__ == "__main__":
    mcp.run(transport="sse", host="127.0.0.1", port=8795)
