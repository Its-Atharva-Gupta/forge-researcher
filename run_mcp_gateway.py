"""
Unified FastMCP SSE Gateway for ForgeResearcher
Serves full research suite including Google Colab & Kaggle:
- `open_google_colab_session`: Launches live Google Colab compute session in browser.
- `inspect_colab_and_kaggle_compute`: Profiles Colab GPU/TPU & Kaggle compute boundaries.
- `search_arxiv_papers`: Searches arXiv papers over HTTPS.
- `search_academic_citations`: Searches CrossRef & Semantic Scholar citations.
- `analyze_dataset_profile`: Profiles CSV/TSV stats and shapes.
- `generate_academic_figures`: Dual-axis publication plotting engine.
- `compile_latex_paper`: 2-column LaTeX conference manuscript compiler.
- `verify_scientific_claims_audit`: Level-2 Scientific Rigor Fact-Checker.
"""
from typing import Dict, Any, List, Optional
from fastmcp import FastMCP

from mcp_servers.arxiv_mcp.server import search_arxiv
from mcp_servers.scholar_mcp.server import search_semantic_scholar
from mcp_servers.kaggle_colab_mcp.server import open_google_colab_session, inspect_colab_and_kaggle_compute
from mcp_servers.latex_compiler_mcp.server import render_latex_manuscript, audit_scientific_claims
from mcp_servers.research_lab_mcp.server import profile_dataset, generate_publication_plots

mcp = FastMCP("forge-researcher-tools")

@mcp.tool()
def open_google_colab_session(notebook_title: Optional[str] = "ForgeResearcher_Experiment") -> Dict[str, Any]:
    """Open Google Colab browser session with GPU/TPU compute and Colab MCP bridge."""
    return open_google_colab_session(notebook_title)

@mcp.tool()
def inspect_colab_and_kaggle_compute() -> Dict[str, Any]:
    """Profile remote Google Colab GPU/TPU and Kaggle cloud compute resources."""
    return inspect_colab_and_kaggle_compute()

@mcp.tool()
def search_arxiv_papers(query: str, max_results: int = 5) -> Dict[str, Any]:
    """Search arXiv papers by topic over HTTPS with failover cache."""
    return search_arxiv(query, max_results)

@mcp.tool()
def search_academic_citations(query: str, limit: int = 5) -> Dict[str, Any]:
    """Search academic literature and citations via CrossRef and Semantic Scholar."""
    return search_semantic_scholar(query, limit)

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
