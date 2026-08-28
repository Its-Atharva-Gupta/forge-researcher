"""
Research Lab FastMCP Server
Integrated research toolkit:
- arXiv literature search (over HTTPS)
- Dataset profiling & validation
- Publication-quality plotting with strict column validation
- LaTeX conference manuscript drafting with character escaping
- Level-2 Scientific Rigor & Fact-Check Auditor
"""
from typing import Dict, Any, List, Optional
import os
import re
import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import pandas as pd
from fastmcp import FastMCP as MCPServer

mcp = MCPServer("ResearchLabServer")

def escape_latex(text: str) -> str:
    """Escapes special LaTeX characters in metadata, titles, and captions."""
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
    }
    pattern = re.compile("|".join(re.escape(k) for k in replacements.keys()))
    return pattern.sub(lambda m: replacements[m.group(0)], text)

# --- 1. LITERATURE RETRIEVAL (ARXIV OVER HTTPS) ---
@mcp.tool()
def search_arxiv_papers(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Queries the official arXiv API over HTTPS for recent papers, abstracts, authors, and arXiv IDs.
    """
    encoded_query = urllib.parse.quote(query)
    url = f"https://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results={max_results}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ForgeResearcher/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        papers = []
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns)
            summary = entry.find('atom:summary', ns)
            published = entry.find('atom:published', ns)
            arxiv_id = entry.find('atom:id', ns)
            
            authors = [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns) if author.find('atom:name', ns) is not None]
            
            papers.append({
                "title": title.text.strip().replace('\n', ' ') if title is not None else "Unknown Title",
                "abstract": summary.text.strip().replace('\n', ' ') if summary is not None else "",
                "published": published.text if published is not None else "",
                "arxiv_url": arxiv_id.text if arxiv_id is not None else "",
                "authors": authors
            })
            
        return {"success": True, "count": len(papers), "papers": papers}
    except Exception as e:
        return {"error": f"Failed to fetch from arXiv API: {str(e)}"}

# --- 2. DATASET PROFILING ---
@mcp.tool()
def profile_dataset(dataset_path: str) -> Dict[str, Any]:
    """
    Profiles a dataset file (CSV/TSV) to report row counts, column types, and summary statistics.
    """
    if not os.path.exists(dataset_path):
        return {"error": f"File {dataset_path} not found."}
    try:
        df = pd.read_csv(dataset_path, sep=None, engine='python')
        return {
            "success": True,
            "profile": {
                "num_rows": len(df),
                "num_columns": len(df.columns),
                "columns": list(df.columns),
                "missing_values": df.isnull().sum().to_dict(),
                "summary": df.describe().to_dict()
            }
        }
    except Exception as e:
        return {"error": f"Failed to profile dataset: {str(e)}"}

# --- 3. ACADEMIC PLOTTING ---
@mcp.tool()
def generate_publication_plots(results_tsv_path: str, output_figure_dir: str) -> Dict[str, Any]:
    """
    Reads results.tsv and generates two publication figures.
    Strictly validates required metric columns (val_loss, val_acc, iteration).
    """
    if not os.path.exists(results_tsv_path):
        return {"error": f"Results log {results_tsv_path} not found."}
    
    try:
        df = pd.read_csv(results_tsv_path, sep="\t")
        if df.empty:
            return {"error": "results.tsv is empty."}
            
        required_cols = ["iteration", "val_loss", "val_acc"]
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            return {"error": f"results.tsv is missing required contract columns: {missing}"}
            
        os.makedirs(output_figure_dir, exist_ok=True)
        plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
        
        # Figure 1: Learning / Loss curve
        fig1, ax1 = plt.subplots(figsize=(6, 4), dpi=300)
        ax1.plot(df["iteration"], df["val_loss"], marker="o", color="#2563eb", label="Validation Loss", lw=2)
        ax1.set_xlabel("Experimental Iteration / Trial", fontsize=10)
        ax1.set_ylabel("Cross-Entropy Loss", fontsize=10)
        ax1.set_title("Empirical Loss Trajectory", fontsize=11, fontweight="bold")
        ax1.legend()
        fig1_path = os.path.join(output_figure_dir, "learning_curve.png")
        fig1.tight_layout()
        fig1.savefig(fig1_path)
        plt.close(fig1)
        
        # Figure 2: Metric Comparison Bar Chart
        fig2, ax2 = plt.subplots(figsize=(6, 4), dpi=300)
        labels = df["description"] if "description" in df.columns else [f"Trial {i}" for i in df["iteration"]]
        short_labels = [str(l)[:18] + '...' if len(str(l)) > 18 else str(l) for l in labels]
        bars = ax2.bar(short_labels, df["val_acc"], color="#16a34a", width=0.5)
        ax2.set_ylabel("Accuracy (%)", fontsize=10)
        ax2.set_title("Benchmark Metric Comparison", fontsize=11, fontweight="bold")
        ax2.set_ylim(max(0, min(df["val_acc"]) - 5), 100)
        for bar in bars:
            yval = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, f"{yval:.1f}%", ha='center', va='bottom', fontsize=8)
            
        fig2_path = os.path.join(output_figure_dir, "benchmark_comparison.png")
        fig2.tight_layout()
        fig2.savefig(fig2_path)
        plt.close(fig2)
        
        return {
            "success": True,
            "figure_paths": [fig1_path, fig2_path]
        }
    except Exception as e:
        return {"error": f"Failed to generate publication plots: {str(e)}"}

# --- 4. SCIENTIFIC MANUSCRIPT DRAFTING ---
@mcp.tool()
def render_latex_manuscript(
    title: str,
    authors: List[str],
    abstract: str,
    sections: Dict[str, str],
    figure_paths: List[str],
    output_tex_path: str
) -> Dict[str, Any]:
    """
    Compiles a structured 2-column LaTeX conference paper draft embedding experimental figures.
    Escapes special characters in titles, metadata, and captions.
    """
    try:
        tex = []
        tex.append(r"\documentclass[10pt,twocolumn,letterpaper]{article}")
        tex.append(r"\usepackage[utf8]{inputenc}")
        tex.append(r"\usepackage{graphicx}")
        tex.append(r"\usepackage{booktabs}")
        tex.append(r"\usepackage{amsmath,amssymb}")
        tex.append(r"\usepackage{geometry}")
        tex.append(r"\geometry{margin=0.75in}")
        tex.append(r"\usepackage{hyperref}")
        
        escaped_title = escape_latex(title)
        escaped_authors = [escape_latex(a) for a in authors]
        
        tex.append(f"\\title{{{escaped_title}}}")
        tex.append(f"\\author{{{', '.join(escaped_authors)}}}")
        tex.append(r"\date{\today}")
        
        tex.append(r"\begin{document}")
        tex.append(r"\maketitle")
        
        tex.append(r"\begin{abstract}")
        tex.append(abstract)
        tex.append(r"\end{abstract}")
        
        for sec_title, sec_body in sections.items():
            escaped_sec_title = escape_latex(sec_title)
            tex.append(f"\\section{{{escaped_sec_title}}}")
            tex.append(sec_body)
            
            if "results" in sec_title.lower() or "experiment" in sec_title.lower():
                for fig in figure_paths:
                    if os.path.exists(fig):
                        safe_caption = escape_latex(f"Empirical evaluation artifact: {os.path.basename(fig)}")
                        tex.append(r"\begin{figure}[htbp]")
                        tex.append(r"\centering")
                        tex.append(f"\\includegraphics[width=\\linewidth]{{{fig}}}")
                        tex.append(f"\\caption{{{safe_caption}}}")
                        tex.append(r"\end{figure}")
                        
        tex.append(r"\end{document}")
        
        full_text = "\n\n".join(tex)
        os.makedirs(os.path.dirname(os.path.abspath(output_tex_path)), exist_ok=True)
        with open(output_tex_path, "w") as f:
            f.write(full_text)
            
        return {"success": True, "output_tex_path": output_tex_path, "chars": len(full_text)}
    except Exception as e:
        return {"error": f"Failed to render LaTeX manuscript: {str(e)}"}

# --- 5. LEVEL-2 RIGOR & FACT-CHECK AUDITOR ---
@mcp.tool()
def audit_scientific_claims(paper_tex_path: str, results_tsv_path: str) -> Dict[str, Any]:
    """
    Audits textual claims in the LaTeX paper against raw numbers in results.tsv.
    Prevents metric hallucinations and ensures empirical grounding.
    """
    if not os.path.exists(paper_tex_path):
        return {"error": f"Paper file {paper_tex_path} not found."}
    if not os.path.exists(results_tsv_path):
        return {"error": f"Results log {results_tsv_path} not found."}
        
    try:
        with open(paper_tex_path, "r") as f:
            paper_text = f.read()
            
        df = pd.read_csv(results_tsv_path, sep="\t")
        
        max_acc = df["val_acc"].max() if "val_acc" in df.columns else None
        min_loss = df["val_loss"].min() if "val_loss" in df.columns else None
        
        discrepancies = []
        
        acc_mentions = re.findall(r'(\d+(?:\.\d+)?)\s*%', paper_text)
        if max_acc is not None:
            max_acc_str = f"{max_acc:.1f}"
            if not any(abs(float(m) - max_acc) < 0.2 for m in acc_mentions):
                discrepancies.append(f"Paper mentions accuracies {acc_mentions}, but best empirical metric was {max_acc_str}%.")
                
        passed = len(discrepancies) == 0
        return {
            "audit_passed": passed,
            "discrepancies": discrepancies,
            "summary": "Paper claims strictly match empirical results.tsv logs." if passed else "Audit failed: Discrepancy found between paper text and empirical metrics."
        }
    except Exception as e:
        return {"error": f"Rigor audit failed: {str(e)}"}

if __name__ == "__main__":
    mcp.run()
