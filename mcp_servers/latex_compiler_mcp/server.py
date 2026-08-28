"""
LaTeX Conference Manuscript Compiler & Level-2 Rigor Auditor
"""
from typing import Dict, Any, List
import os
import re
import pandas as pd
from fastmcp import FastMCP

mcp = FastMCP("LaTeXCompilerServer")

def render_latex_manuscript(
    title: str,
    authors: List[str],
    abstract: str,
    sections: Dict[str, str],
    figure_paths: List[str],
    output_tex_path: str
) -> Dict[str, Any]:
    """Compiles a structured 2-column LaTeX conference paper draft."""
    clean_title = title.replace("&", "\\&").replace("%", "\\%").replace("_", "\\_")
    clean_abstract = abstract.replace("&", "\\&").replace("%", "\\%")
    
    latex_content = [
        "\\documentclass[twocolumn]{article}",
        "\\usepackage{graphicx}",
        "\\usepackage{booktabs}",
        "\\usepackage{amsmath}",
        "\\usepackage{hyperref}",
        f"\\title{{{clean_title}}}",
        f"\\author{{{', '.join(authors)}}}",
        "\\begin{document}",
        "\\maketitle",
        "\\begin{abstract}",
        clean_abstract,
        "\\end{abstract}"
    ]

    for sec_title, sec_body in sections.items():
        clean_sec_title = sec_title.replace("&", "\\&").replace("_", "\\_")
        clean_sec_body = sec_body.replace("&", "\\&").replace("%", "\\%")
        latex_content.append(f"\\section{{{clean_sec_title}}}")
        latex_content.append(clean_sec_body)

    for i, fig in enumerate(figure_paths):
        latex_content.append("\\begin{figure}[htbp]")
        latex_content.append("\\centering")
        latex_content.append(f"\\includegraphics[width=\\linewidth]{{{fig}}}")
        latex_content.append(f"\\caption{{Experimental result figure {i+1}}}")
        latex_content.append(f"\\label{{fig:result_{i+1}}}")
        latex_content.append("\\end{figure}")

    latex_content.append("\\end{document}")
    
    os.makedirs(os.path.dirname(os.path.abspath(output_tex_path)), exist_ok=True)
    with open(output_tex_path, "w") as f:
        f.write("\n".join(latex_content))

    return {
        "success": True,
        "tex_path": output_tex_path,
        "lines_written": len(latex_content),
        "figures_embedded": len(figure_paths)
    }

def audit_scientific_claims(paper_tex_path: str, results_tsv_path: str) -> Dict[str, Any]:
    """Level-2 Scientific Rigor Fact-Checker verifying paper text matches raw metrics."""
    if not os.path.exists(paper_tex_path):
        return {"error": f"Paper file {paper_tex_path} does not exist"}
    if not os.path.exists(results_tsv_path):
        return {"error": f"Results file {results_tsv_path} does not exist"}

    with open(paper_tex_path, "r") as f:
        paper_text = f.read()

    df = pd.read_csv(results_tsv_path, sep="\t")
    
    metrics_summary = {}
    for col in df.select_dtypes(include=['float64', 'int64']).columns:
        metrics_summary[col] = {
            "min": float(df[col].min()),
            "max": float(df[col].max()),
            "mean": float(df[col].mean())
        }

    floats_in_paper = [float(x) for x in re.findall(r'\b\d+\.\d+\b', paper_text)]
    
    mismatches = []
    for num in floats_in_paper:
        matched = False
        for col, stats in metrics_summary.items():
            if abs(num - stats["min"]) < 1e-3 or abs(num - stats["max"]) < 1e-3 or abs(num - stats["mean"]) < 1e-2:
                matched = True
                break
        if not matched:
            mismatches.append(num)

    passed = len(mismatches) == 0
    return {
        "audit_passed": passed,
        "total_numbers_checked": len(floats_in_paper),
        "unverified_metrics": mismatches,
        "metrics_summary": metrics_summary,
        "message": "Level-2 audit passed: All stated metrics verified against raw results." if passed else "Audit Warning: Discrepancies found between text claims and raw data."
    }


if __name__ == "__main__":
    mcp.run()
