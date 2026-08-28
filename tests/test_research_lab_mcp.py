import os
import tempfile
import pandas as pd
from mcp_servers.research_lab_mcp.server import (
    validate_sandbox_code,
    generate_loss_accuracy_plot,
    render_latex_manuscript
)

def test_validate_sandbox_code_safe():
    safe_code = """
import numpy as np
from sklearn.ensemble import RandomForestClassifier
X = np.random.randn(100, 10)
y = np.random.randint(0, 2, 100)
clf = RandomForestClassifier(n_estimators=10)
clf.fit(X, y)
"""
    result = validate_sandbox_code(safe_code)
    assert result["is_safe"] is True
    assert len(result["issues"]) == 0

def test_validate_sandbox_code_dangerous():
    dangerous_code = """
import os
os.system('rm -rf /')
"""
    result = validate_sandbox_code(dangerous_code)
    assert result["is_safe"] is False
    assert any("os.system" in issue for issue in result["issues"])

def test_generate_loss_accuracy_plot():
    with tempfile.TemporaryDirectory() as tmpdir:
        tsv_path = os.path.join(tmpdir, "results.tsv")
        img_path = os.path.join(tmpdir, "plot.png")
        
        df = pd.DataFrame({
            "iteration": [1, 2, 3],
            "val_loss": [1.5, 1.2, 0.9],
            "val_acc": [65.0, 74.5, 82.1]
        })
        df.to_csv(tsv_path, sep="\t", index=False)
        
        result = generate_loss_accuracy_plot(tsv_path, img_path)
        assert result.get("success") is True
        assert os.path.exists(img_path)

def test_render_latex_manuscript():
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "paper.tex")
        res = render_latex_manuscript(
            title="Automated Exploration of Tabular Ensembles",
            authors=["ForgeResearcher Agent", "Atharva Gupta"],
            abstract="We empirically evaluate algorithmic iterations on tabular classification benchmarks...",
            sections={"Introduction": "Tabular models...", "Experiments": "We ran 5 trials."},
            results_table_tsv="",
            figure_path="plot.png",
            output_tex_path=tex_path
        )
        assert res.get("success") is True
        assert os.path.exists(tex_path)
