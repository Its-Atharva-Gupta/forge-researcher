"""
Research Lab Streamable HTTP / SSE FastMCP Gateway
Serves all ForgeResearcher research tools over HTTP/SSE.
"""
from typing import Dict, Any, List
import asyncio
import os
import uvicorn
from mcp.server.mcpserver import MCPServer

from mcp_servers.arxiv_mcp.server import search_arxiv
from mcp_servers.scholar_mcp.server import search_semantic_scholar
from mcp_servers.kaggle_colab_mcp.server import search_open_datasets, check_compute_environment
from mcp_servers.latex_compiler_mcp.server import render_latex_manuscript, audit_scientific_claims
from mcp_servers.research_lab_mcp.server import profile_dataset, generate_publication_plots

server = MCPServer("forge-researcher-tools")

@server.tool()
def search_arxiv_papers(query: str, max_results: int = 5) -> Dict[str, Any]:
    """Search arXiv papers by topic over HTTPS."""
    return search_arxiv(query, max_results)

@server.tool()
def search_academic_citations(query: str, limit: int = 5) -> Dict[str, Any]:
    """Search Google Scholar and Semantic Scholar citations."""
    return search_semantic_scholar(query, limit)

@server.tool()
def discover_open_datasets(query: str, limit: int = 5) -> Dict[str, Any]:
    """Discover scientific datasets from open repositories."""
    return search_open_datasets(query, limit)

@server.tool()
def inspect_compute_environment() -> Dict[str, Any]:
    """Profile local and sandboxed compute environment."""
    return check_compute_environment()

@server.tool()
def analyze_dataset_profile(dataset_path: str) -> Dict[str, Any]:
    """Profile CSV/TSV dataset stats and column types."""
    return profile_dataset(dataset_path)

@server.tool()
def generate_academic_figures(results_tsv_path: str, output_figure_dir: str) -> Dict[str, Any]:
    """Generate dual-axis publication loss and benchmark comparison plots."""
    return generate_publication_plots(results_tsv_path, output_figure_dir)

@server.tool()
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

@server.tool()
def verify_scientific_claims_audit(paper_tex_path: str, results_tsv_path: str) -> Dict[str, Any]:
    """Level-2 Scientific Rigor Fact-Checker verifying paper text matches raw metrics."""
    return audit_scientific_claims(paper_tex_path, results_tsv_path)

if __name__ == "__main__":
    server.run(transport="sse", port=8795, host="127.0.0.1")
