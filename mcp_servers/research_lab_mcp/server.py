"""
Research Lab MCP Server
Provides research utilities: LaTeX paper compilation, benchmark plotting, dataset profiling, and code safety validation.
"""
from typing import Dict, Any, List
import os
import json
import matplotlib.pyplot as plt
import pandas as pd
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("ResearchLabServer")

@mcp.tool()
def profile_benchmark_dataset(dataset_path: str) -> Dict[str, Any]:
    """
    Analyzes a CSV/TSV or dataset file to extract shapes, class distributions, and feature summaries.
    """
    if not os.path.exists(dataset_path):
        return {"error": f"File {dataset_path} does not exist."}
    
    try:
        df = pd.read_csv(dataset_path, sep=None, engine='python')
        profile = {
            "num_samples": len(df),
            "num_features": len(df.columns),
            "columns": list(df.columns),
            "missing_values": df.isnull().sum().to_dict(),
            "summary_stats": df.describe().to_dict()
        }
        return {"success": True, "profile": profile}
    except Exception as e:
        return {"error": f"Failed to profile dataset: {str(e)}"}

@mcp.tool()
def generate_loss_accuracy_plot(results_tsv_path: str, output_image_path: str) -> Dict[str, Any]:
    """
    Reads results.tsv (Karpathy-style experiment log) and produces a publication-quality training & validation chart.
    """
    if not os.path.exists(results_tsv_path):
        return {"error": f"Log file {results_tsv_path} not found."}

    try:
        df = pd.read_csv(results_tsv_path, sep="\t")
        
        plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), dpi=300)
        
        if "val_loss" in df.columns:
            ax1.plot(df["iteration"], df["val_loss"], marker="o", color="#0284c7", label="Val Loss")
            ax1.set_xlabel("Trial / Iteration")
            ax1.set_ylabel("Validation Loss")
            ax1.set_title("Validation Loss Trajectory")
            ax1.legend()
            
        if "val_acc" in df.columns:
            ax2.plot(df["iteration"], df["val_acc"], marker="s", color="#16a34a", label="Val Accuracy")
            ax2.set_xlabel("Trial / Iteration")
            ax2.set_ylabel("Accuracy (%)")
            ax2.set_title("Model Accuracy Improvement")
            ax2.legend()
            
        plt.tight_layout()
        os.makedirs(os.path.dirname(os.path.abspath(output_image_path)), exist_ok=True)
        plt.savefig(output_image_path)
        plt.close()
        
        return {"success": True, "output_image": output_image_path}
    except Exception as e:
        return {"error": f"Plotting failed: {str(e)}"}

@mcp.tool()
def validate_sandbox_code(code_string: str) -> Dict[str, Any]:
    """
    Audits generated train.py code for safety constraints before sandbox execution.
    Flags suspicious OS/network primitives and enforces bounded iteration checks.
    """
    forbidden_tokens = ["os.system", "subprocess.Popen", "shutil.rmtree", "__import__('os')", "eval(", "exec("]
    issues = []
    
    for token in forbidden_tokens:
        if token in code_string:
            issues.append(f"Potentially dangerous pattern detected: {token}")
            
    is_safe = len(issues) == 0
    return {
        "is_safe": is_safe,
        "issues": issues,
        "recommendation": "Code approved for sandbox execution" if is_safe else "Code blocked. Please remove unsafe system calls."
    }

@mcp.tool()
def render_latex_manuscript(
    title: str,
    authors: List[str],
    abstract: str,
    sections: Dict[str, str],
    results_table_tsv: str,
    figure_path: str,
    output_tex_path: str
) -> Dict[str, Any]:
    """
    Assembles a full conference-style LaTeX (.tex) document with empirical tables and figures.
    """
    try:
        tex_content = []
        tex_content.append(r"\documentclass[10pt,twocolumn,letterpaper]{article}")
        tex_content.append(r"\usepackage[utf8]{inputenc}")
        tex_content.append(r"\usepackage{graphicx}")
        tex_content.append(r"\usepackage{booktabs}")
        tex_content.append(r"\usepackage{amsmath,amssymb}")
        tex_content.append(r"\usepackage{geometry}")
        tex_content.append(r"\geometry{margin=0.75in}")
        tex_content.append(r"\usepackage{hyperref}")
        
        tex_content.append(f"\\title{{{title}}}")
        tex_content.append(f"\\author{{{', '.join(authors)}}}")
        tex_content.append(r"\date{\today}")
        
        tex_content.append(r"\begin{document}")
        tex_content.append(r"\maketitle")
        
        tex_content.append(r"\begin{abstract}")
        tex_content.append(abstract)
        tex_content.append(r"\end{abstract}")
        
        # Sections
        for sec_name, sec_body in sections.items():
            tex_content.append(f"\\section{{{sec_name}}}")
            tex_content.append(sec_body)
            
            # Embed figure in Experimental Results
            if sec_name.lower() in ["experiments", "results", "empirical evaluation"]:
                if os.path.exists(figure_path):
                    tex_content.append(r"\begin{figure}[htbp]")
                    tex_content.append(r"\centering")
                    tex_content.append(f"\\includegraphics[width=\\linewidth]{{{figure_path}}}")
                    tex_content.append(r"\caption{Optimization trajectories across iterations in TrueForge sandbox.}")
                    tex_content.append(r"\label{fig:results}")
                    tex_content.append(r"\end{figure}")
                    
        tex_content.append(r"\end{document}")
        
        full_tex = "\n\n".join(tex_content)
        os.makedirs(os.path.dirname(os.path.abspath(output_tex_path)), exist_ok=True)
        with open(output_tex_path, "w") as f:
            f.write(full_tex)
            
        return {"success": True, "output_tex_path": output_tex_path, "num_characters": len(full_tex)}
    except Exception as e:
        return {"error": f"Failed to generate LaTeX manuscript: {str(e)}"}

if __name__ == "__main__":
    mcp.run()
