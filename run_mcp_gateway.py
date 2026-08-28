"""
Unified FastMCP SSE Gateway for ForgeResearcher
Serves dedicated research tools over persistent SSE:
- search_kaggle_datasets (Kaggle API + open scientific benchmarks)
- search_arxiv_papers (arXiv API over HTTPS + fallbacks)
- search_academic_citations (CrossRef + Semantic Scholar)
- inspect_compute_environment (CPU/RAM/storage profiling)
- analyze_dataset_profile (CSV/TSV stats)
- generate_academic_figures (Loss curves & bar charts)
- compile_latex_paper (2-column LaTeX manuscript)
- verify_scientific_claims_audit (Level-2 Fact-Checker)
"""
from typing import Dict, Any, List
from mcp.server.mcpserver import MCPServer

from mcp_servers.arxiv_mcp.server import search_arxiv
from mcp_servers.scholar_mcp.server import search_semantic_scholar
from mcp_servers.kaggle_colab_mcp.server import search_kaggle_datasets, inspect_compute_environment
from mcp_servers.latex_compiler_mcp.server import render_latex_manuscript, audit_scientific_claims
from mcp_servers.research_lab_mcp.server import profile_dataset, generate_publication_plots

mcp = MCPServer("forge-researcher-tools")

@mcp.tool()
def search_kaggle_datasets(query: str, max_results: int = 5) -> Dict[str, Any]:
    """Search Kaggle, competition benchmarks, and open scientific datasets."""
    return search_kaggle_datasets(query, max_results)

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
    """Profile local and sandboxed compute environment (CPU cores, RAM, storage)."""
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
