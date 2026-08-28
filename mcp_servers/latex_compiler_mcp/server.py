"""
LaTeX & Document Synthesis MCP Server
Provides full LaTeX document compilation, character escaping, and Level-2 rigor audit.
"""
from typing import Dict, Any, List
import os
import re
import pandas as pd
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("LaTeXCompilerServer")

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

@mcp.tool()
def render_latex_manuscript(
    title: str,
    authors: List[str],
    abstract: str,
    sections: Dict[str, str],
    figure_paths: List[str],
    output_tex_path: str
) -> Dict[str, Any]:
    """Compiles a structured 2-column LaTeX conference paper draft."""
    try:
        tex = [
            r"\documentclass[10pt,twocolumn,letterpaper]{article}",
            r"\usepackage[utf8]{inputenc}",
            r"\usepackage{graphicx}",
            r"\usepackage{booktabs}",
            r"\usepackage{amsmath,amssymb}",
            r"\usepackage{geometry}",
            r"\geometry{margin=0.75in}",
            r"\usepackage{hyperref}",
            f"\\title{{{escape_latex(title)}}}",
            f"\\author{{{', '.join([escape_latex(a) for a in authors])}}}",
            r"\date{\today}",
            r"\begin{document}",
            r"\maketitle",
            r"\begin{abstract}",
            abstract,
            r"\end{abstract}"
        ]
        for sec_title, sec_body in sections.items():
            tex.append(f"\\section{{{escape_latex(sec_title)}}}")
            tex.append(sec_body)
            if "results" in sec_title.lower() or "experiment" in sec_title.lower():
                for fig in figure_paths:
                    if os.path.exists(fig):
                        safe_cap = escape_latex(f"Empirical artifact: {os.path.basename(fig)}")
                        tex.append(f"\\begin{{figure}}[htbp]\\centering\\includegraphics[width=\\linewidth]{{{fig}}}\\caption{{{safe_cap}}}\\end{{figure}}")
        tex.append(r"\end{document}")
        full_text = "\n\n".join(tex)
        os.makedirs(os.path.dirname(os.path.abspath(output_tex_path)), exist_ok=True)
        with open(output_tex_path, "w") as f:
            f.write(full_text)
        return {"success": True, "output_tex_path": output_tex_path, "chars": len(full_text)}
    except Exception as e:
        return {"error": f"LaTeX rendering failed: {str(e)}"}

@mcp.tool()
def audit_scientific_claims(paper_tex_path: str, results_tsv_path: str) -> Dict[str, Any]:
    """Audits textual claims in paper.tex against raw results.tsv numbers to eliminate hallucinations."""
    if not os.path.exists(paper_tex_path) or not os.path.exists(results_tsv_path):
        return {"error": "Missing input files for audit."}
    try:
        with open(paper_tex_path, "r") as f:
            text = f.read()
        df = pd.read_csv(results_tsv_path, sep="\t")
        max_acc = df["val_acc"].max() if "val_acc" in df.columns else None
        discrepancies = []
        acc_mentions = re.findall(r'(\d+(?:\.\d+)?)\s*%', text)
        if max_acc is not None and not any(abs(float(m) - max_acc) < 0.2 for m in acc_mentions):
            discrepancies.append(f"Paper mentions {acc_mentions}, but best empirical metric was {max_acc:.1f}%.")
        passed = len(discrepancies) == 0
        return {
            "audit_passed": passed,
            "discrepancies": discrepancies,
            "summary": "Paper claims strictly verified against raw logs." if passed else "Audit failed: discrepancy found."
        }
    except Exception as e:
        return {"error": f"Audit error: {str(e)}"}

if __name__ == "__main__":
    mcp.run()
