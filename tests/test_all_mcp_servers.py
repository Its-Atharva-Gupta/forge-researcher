import os
import tempfile
import pandas as pd
from mcp_servers.arxiv_mcp.server import search_arxiv
from mcp_servers.scholar_mcp.server import search_semantic_scholar
from mcp_servers.kaggle_colab_mcp.server import check_compute_environment, search_open_datasets
from mcp_servers.latex_compiler_mcp.server import render_latex_manuscript, audit_scientific_claims

def test_arxiv_server():
    res = search_arxiv("diffusion models", max_results=2)
    assert res.get("success") is True or "error" in res

def test_scholar_server():
    res = search_semantic_scholar("attention is all you need", limit=2)
    assert res.get("success") is True or "error" in res

def test_kaggle_colab_server():
    env = check_compute_environment()
    assert "cpu_cores" in env
    assert "sandbox_mode" in env

def test_latex_compiler_and_audit():
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "test.tex")
        tsv_path = os.path.join(tmpdir, "results.tsv")
        
        df = pd.DataFrame({"iteration": [1], "val_loss": [0.25], "val_acc": [92.5]})
        df.to_csv(tsv_path, sep="\t", index=False)
        
        render_res = render_latex_manuscript(
            title="Auto ML & Transformers",
            authors=["Agent_1"],
            abstract="Empirical trial.",
            sections={"Results": "We achieved 92.5% accuracy."},
            figure_paths=[],
            output_tex_path=tex_path
        )
        assert render_res["success"] is True
        
        audit_res = audit_scientific_claims(tex_path, tsv_path)
        assert audit_res["audit_passed"] is True
