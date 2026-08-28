import os
import tempfile
import json
import pandas as pd
from mcp_servers.research_lab_mcp.server import (
    search_arxiv_papers,
    profile_dataset,
    generate_publication_plots,
    render_latex_manuscript,
    audit_scientific_claims
)

def test_search_arxiv_papers():
    res = search_arxiv_papers("transformer attention", max_results=2)
    assert res.get("success") is True or "error" in res
    if res.get("success"):
        assert "papers" in res
        assert len(res["papers"]) <= 2

def test_profile_dataset():
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = os.path.join(tmpdir, "sample.csv")
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        df.to_csv(csv_path, index=False)
        
        res = profile_dataset(csv_path)
        assert res.get("success") is True
        assert res["profile"]["num_rows"] == 3
        assert res["profile"]["num_columns"] == 2

def test_generate_publication_plots():
    with tempfile.TemporaryDirectory() as tmpdir:
        tsv_path = os.path.join(tmpdir, "results.tsv")
        fig_dir = os.path.join(tmpdir, "figures")
        
        df = pd.DataFrame({
            "iteration": [1, 2, 3],
            "description": ["Baseline", "Feature Engineering", "Ensemble"],
            "val_loss": [0.45, 0.38, 0.31],
            "val_acc": [84.2, 88.5, 91.2]
        })
        df.to_csv(tsv_path, sep="\t", index=False)
        
        res = generate_publication_plots(tsv_path, fig_dir)
        assert res.get("success") is True
        assert len(res["figure_paths"]) == 2
        for p in res["figure_paths"]:
            assert os.path.exists(p)

def test_audit_scientific_claims_passed_and_failed():
    with tempfile.TemporaryDirectory() as tmpdir:
        tsv_path = os.path.join(tmpdir, "results.tsv")
        tex_path = os.path.join(tmpdir, "paper.tex")
        
        df = pd.DataFrame({
            "iteration": [1, 2],
            "val_loss": [0.4, 0.3],
            "val_acc": [85.0, 91.2]
        })
        df.to_csv(tsv_path, sep="\t", index=False)
        
        # 1. Matching claims
        valid_tex = "Our final model achieved 91.2% accuracy on the benchmark."
        with open(tex_path, "w") as f:
            f.write(valid_tex)
        res = audit_scientific_claims(tex_path, tsv_path)
        assert res.get("audit_passed") is True
        
        # 2. Fabricated claims
        invalid_tex = "Our model achieved 99.9% accuracy."
        with open(tex_path, "w") as f:
            f.write(invalid_tex)
        res_bad = audit_scientific_claims(tex_path, tsv_path)
        assert res_bad.get("audit_passed") is False
