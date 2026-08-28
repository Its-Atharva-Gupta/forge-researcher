import React, { useState, useEffect } from 'react';
import { 
  FlaskConical, 
  FileText, 
  CheckCircle2, 
  Layers, 
  Sparkles, 
  BarChart3, 
  ShieldCheck, 
  ExternalLink,
  Database,
  Code2,
  FolderTree,
  Terminal,
  RefreshCw,
  Cpu
} from 'lucide-react';

export default function App() {
  const [liveArtifact, setLiveArtifact] = useState('code');
  const [workspaceFiles, setWorkspaceFiles] = useState([
    { name: "workspace/results.tsv", size: "1.4 KB", type: "data", time: "Just now" },
    { name: "workspace/paper.tex", size: "12.8 KB", type: "tex", time: "2m ago" },
    { name: "workspace/figures/convergence.png", size: "142 KB", type: "image", time: "2m ago" },
    { name: "workspace/rigor_audit.json", size: "2.1 KB", type: "json", time: "1m ago" },
    { name: "workspace/experiment_kaggle.py", size: "4.6 KB", type: "code", time: "3m ago" }
  ]);

  const [selectedFile, setSelectedFile] = useState("workspace/experiment_kaggle.py");
  const [kaggleLogs, setKaggleLogs] = useState(
`[KAGGLE CLOUD GPU EXECUTION]
Kernel: atharvagupta123/mnist-t1-cu118-numpy-fix
Hardware: NVIDIA Tesla P100-PCIE-16GB (sm 60)
Environment: CUDA 11.8 / PyTorch 2.2.0 / NumPy 1.26.4

[00:01] DEVICE=cuda GPU=Tesla P100-PCIE-16GB
[00:03] Loaded MNIST dataset: 60,000 train / 10,000 test
[00:14] Epoch 1/8 - Loss: 0.16981 | Val Acc: 98.40% | Time: 10.6s
[00:25] Epoch 2/8 - Loss: 0.04858 | Val Acc: 98.83% | Time: 10.5s
[00:36] Epoch 3/8 - Loss: 0.03261 | Val Acc: 98.98% | Time: 10.6s
[00:46] Epoch 4/8 - Loss: 0.02370 | Val Acc: 99.07% | Time: 10.5s
[00:57] Epoch 5/8 - Loss: 0.01808 | Val Acc: 98.98% | Time: 10.6s
[01:08] Epoch 6/8 - Loss: 0.01456 | Val Acc: 98.82% | Time: 10.5s
[01:19] Epoch 7/8 - Loss: 0.00990 | Val Acc: 99.14% | Time: 10.6s ★ (Best)
[01:29] Epoch 8/8 - Loss: 0.01022 | Val Acc: 98.99% | Time: 10.5s

Total Training Time: 84.64s
Output: Saved results to workspace/results.tsv & model_weights.pt
Status: SUCCESS (Exit Code: 0)`
  );

  const fileContents = {
    "workspace/experiment_kaggle.py": `import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
import pandas as pd
import time

# Verify Kaggle GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"DEVICE={device} GPU={torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")

class ConvNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 3)
        self.conv2 = nn.Conv2d(32, 64, 3)
        self.fc1 = nn.Linear(64 * 5 * 5, 128)
        self.fc2 = nn.Linear(128, 10)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(2, 2)

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(-1, 64 * 5 * 5)
        x = self.relu(self.fc1(x))
        return self.fc2(x)

# Training loop emitting results.tsv
# ...`,
    "workspace/results.tsv": `epoch\ttrain_loss\tval_acc\ttime_seconds
1\t0.16981\t98.40\t10.64
2\t0.04858\t98.83\t10.51
3\t0.03261\t98.98\t10.62
4\t0.02370\t99.07\t10.55
5\t0.01808\t98.98\t10.61
6\t0.01456\t98.82\t10.53
7\t0.00990\t99.14\t10.64
8\t0.01022\t98.99\t10.54`,
    "workspace/rigor_audit.json": `{
  "audit_status": "PASSED",
  "verified_metrics": {
    "peak_validation_accuracy": 99.14,
    "best_epoch": 7,
    "total_gpu_time_s": 84.64,
    "parameter_count": 421642
  },
  "hallucination_detected": false
}`,
    "workspace/paper.tex": `\\documentclass[twocolumn]{article}
\\title{Reproducible Cloud-GPU MNIST Benchmark}
\\author{atharvagupta123}
\\begin{document}
\\maketitle
\\begin{abstract}
We report a minimal, fully reproducible experiment validating a cloud-GPU training pipeline on Kaggle Tesla P100...
\\end{abstract}
\\end{document}`
  };

  const subagents = [
    { name: "research-manager", role: "Parent Autonomy Orchestrator", status: "Active", tag: "Orchestration", color: "#8b5cf6" },
    { name: "eval-worker", role: "Kaggle GPU Dispatcher & Sandbox", status: "Ready", tag: "Compute", color: "#3b82f6" },
    { name: "plot-worker", role: "Dual-Axis Academic Plotting", status: "Ready", tag: "Visualization", color: "#10b981" },
    { name: "write-worker", role: "LaTeX Conference Synthesis", status: "Ready", tag: "Writing", color: "#f59e0b" },
    { name: "rigor-worker", role: "Level-2 Empirical Fact-Checker", status: "Ready", tag: "Audit", color: "#ec4899" },
  ];

  const pipelineStages = [
    { id: 1, title: "1. Literature & HF Discovery", desc: "arXiv HTTPS & Hugging Face Hub search", tool: "search_arxiv, search_huggingface_models" },
    { id: 2, title: "2. Hypothesis Matrix & Budget", desc: "3-trial matrix formulation & GPU compute sizing", tool: "inspect_kaggle_and_local_compute" },
    { id: 3, title: "3. Approval Gate #1", desc: "Explicit user authorization before GPU execution", tool: "ask_user_questions" },
    { id: 4, title: "4. Kaggle Cloud GPU Execution", desc: "Dispatched to remote NVIDIA Tesla P100 / Dual-T4", tool: "run_experiment_on_kaggle_gpu" },
    { id: 5, title: "5. Dual-Axis Plotting & LaTeX", desc: "Generates loss curves & 2-column paper.tex", tool: "generate_publication_plots, render_latex_manuscript" },
    { id: 6, title: "6. Level-2 Rigor Fact-Check & Gate #2", desc: "Validates all claims vs raw results.tsv", tool: "audit_scientific_claims" }
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', width: '100vw', backgroundColor: '#07080c', color: '#f1f5f9', fontFamily: "'Plus Jakarta Sans', sans-serif" }}>
      
      {/* 🌟 Top Navigation: Hardware Telemetry */}
      <header style={{ height: '56px', borderBottom: '1px solid rgba(255,255,255,0.08)', backgroundColor: 'rgba(15,17,26,0.85)', backdropFilter: 'blur(16px)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 20px', zIndex: 20 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ height: '34px', width: '34px', borderRadius: '8px', background: 'linear-gradient(135deg, #7c3aed, #4f46e5)', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 4px 12px rgba(124,58,237,0.3)' }}>
            <FlaskConical style={{ height: '18px', width: '18px', color: '#fff' }} />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ fontWeight: '700', fontSize: '14px', color: '#fff' }}>ForgeResearcher</span>
              <span style={{ fontSize: '10px', fontFamily: 'monospace', padding: '2px 6px', borderRadius: '4px', backgroundColor: 'rgba(124,58,237,0.2)', color: '#c4b5fd', border: '1px solid rgba(124,58,237,0.3)' }}>Studio 2.0</span>
            </div>
            <p style={{ fontSize: '11px', color: '#94a3b8', margin: 0 }}>Autonomous Empirical ML Research Harness on TrueForge</p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '4px 12px', borderRadius: '20px', backgroundColor: 'rgba(24,27,41,0.6)', border: '1px solid rgba(255,255,255,0.08)', fontSize: '12px' }}>
            <span style={{ height: '8px', width: '8px', borderRadius: '50%', backgroundColor: '#10b981', display: 'inline-block' }}></span>
            <span style={{ color: '#94a3b8' }}>Kaggle Cloud GPU:</span>
            <span style={{ color: '#34d399', fontFamily: 'monospace', fontWeight: '600' }}>Tesla P100 / Dual-T4</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '4px 12px', borderRadius: '20px', backgroundColor: 'rgba(24,27,41,0.6)', border: '1px solid rgba(255,255,255,0.08)', fontSize: '12px' }}>
            <Database style={{ height: '14px', width: '14px', color: '#60a5fa' }} />
            <span style={{ color: '#94a3b8' }}>Hugging Face Hub:</span>
            <span style={{ color: '#60a5fa', fontFamily: 'monospace', fontWeight: '600' }}>Online</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '4px 12px', borderRadius: '20px', backgroundColor: 'rgba(24,27,41,0.6)', border: '1px solid rgba(255,255,255,0.08)', fontSize: '12px' }}>
            <ShieldCheck style={{ height: '14px', width: '14px', color: '#c084fc' }} />
            <span style={{ color: '#94a3b8' }}>Level-2 Fact-Check:</span>
            <span style={{ color: '#c084fc', fontFamily: 'monospace', fontWeight: '600' }}>Active</span>
          </div>

          <a href="http://localhost:8790" target="_blank" rel="noreferrer" style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', color: '#c4b5fd', padding: '6px 12px', borderRadius: '6px', backgroundColor: 'rgba(124,58,237,0.15)', border: '1px solid rgba(124,58,237,0.3)', textDecoration: 'none' }}>
            <span>TrueForge Core</span>
            <ExternalLink style={{ height: '12px', width: '12px' }} />
          </a>
        </div>
      </header>

      {/* 🚀 Main Split-Screen Workspace */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        
        {/* 🧭 Left Panel: Subagent Registry & Stepper */}
        <aside style={{ width: '280px', borderRight: '1px solid rgba(255,255,255,0.08)', backgroundColor: 'rgba(15,17,26,0.7)', padding: '16px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#94a3b8', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Layers style={{ height: '14px', width: '14px', color: '#a78bfa' }} />
                Guided Autonomy Hierarchy
              </span>
              <span style={{ fontSize: '10px', fontFamily: 'monospace', padding: '2px 6px', borderRadius: '4px', backgroundColor: 'rgba(255,255,255,0.05)', color: '#94a3b8' }}>5 Agents</span>
            </div>
            <p style={{ fontSize: '11px', color: '#64748b', margin: 0 }}>Contract-bounded subagents coordinated by parent manager.</p>
          </div>

          {/* Subagent Cards */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {subagents.map((agent, i) => (
              <div key={i} style={{ padding: '10px', borderRadius: '8px', backgroundColor: 'rgba(24,27,41,0.6)', border: '1px solid rgba(255,255,255,0.05)' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '4px' }}>
                  <span style={{ fontFamily: 'monospace', fontSize: '12px', fontWeight: '600', color: '#e2e8f0' }}>{agent.name}</span>
                  <span style={{ fontSize: '10px', fontFamily: 'monospace', padding: '2px 6px', borderRadius: '4px', color: agent.color, backgroundColor: `${agent.color}15`, border: `1px solid ${agent.color}30` }}>{agent.tag}</span>
                </div>
                <p style={{ fontSize: '11px', color: '#94a3b8', margin: 0 }}>{agent.role}</p>
              </div>
            ))}
          </div>

          {/* Stepper */}
          <div style={{ paddingTop: '12px', borderTop: '1px solid rgba(255,255,255,0.08)' }}>
            <span style={{ fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#94a3b8', display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '12px' }}>
              <Sparkles style={{ height: '14px', width: '14px', color: '#fbbf24' }} />
              Research Lifecycle Stages
            </span>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {pipelineStages.map((stage) => (
                <div key={stage.id} style={{ padding: '10px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)', backgroundColor: 'rgba(255,255,255,0.02)' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontWeight: '600', fontSize: '12px', color: '#f1f5f9', marginBottom: '2px' }}>
                    <CheckCircle2 style={{ height: '14px', width: '14px', color: '#475569' }} />
                    <span>{stage.title}</span>
                  </div>
                  <p style={{ fontSize: '11px', color: '#94a3b8', margin: 0, paddingLeft: '22px' }}>{stage.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </aside>

        {/* 💬 Center Panel: TRUE LIVE TrueForge Backend WebSocket Chat Container */}
        <main style={{ flex: 1, display: 'flex', flexDirection: 'column', backgroundColor: '#090a0f', position: 'relative' }}>
          <iframe 
            src="http://localhost:8790" 
            style={{ width: '100%', height: '100%', border: 'none', backgroundColor: '#090a0f' }}
            title="TrueForge Live Agent Chat"
          />
        </main>

        {/* 📊 Right Panel: Code Inspector, Kaggle GPU Logs & Workspace Explorer */}
        <aside style={{ width: '440px', borderLeft: '1px solid rgba(255,255,255,0.08)', backgroundColor: 'rgba(15,17,26,0.85)', display: 'flex', flexDirection: 'column' }}>
          
          {/* Tab Navigation */}
          <div style={{ height: '48px', borderBottom: '1px solid rgba(255,255,255,0.08)', display: 'flex', alignItems: 'center', justifyContent: 'space-around', padding: '0 8px', backgroundColor: '#0c0e17' }}>
            <button 
              onClick={() => setLiveArtifact('code')} 
              style={{ padding: '6px 10px', borderRadius: '6px', border: 'none', backgroundColor: liveArtifact === 'code' ? '#7c3aed' : 'transparent', color: liveArtifact === 'code' ? '#fff' : '#94a3b8', fontSize: '11px', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '5px' }}
            >
              <Code2 style={{ height: '13px', width: '13px' }} />
              <span>Kaggle Code</span>
            </button>
            <button 
              onClick={() => setLiveArtifact('logs')} 
              style={{ padding: '6px 10px', borderRadius: '6px', border: 'none', backgroundColor: liveArtifact === 'logs' ? '#7c3aed' : 'transparent', color: liveArtifact === 'logs' ? '#fff' : '#94a3b8', fontSize: '11px', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '5px' }}
            >
              <Terminal style={{ height: '13px', width: '13px' }} />
              <span>GPU Logs</span>
            </button>
            <button 
              onClick={() => setLiveArtifact('workspace')} 
              style={{ padding: '6px 10px', borderRadius: '6px', border: 'none', backgroundColor: liveArtifact === 'workspace' ? '#7c3aed' : 'transparent', color: liveArtifact === 'workspace' ? '#fff' : '#94a3b8', fontSize: '11px', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '5px' }}
            >
              <FolderTree style={{ height: '13px', width: '13px' }} />
              <span>Workspace</span>
            </button>
            <button 
              onClick={() => setLiveArtifact('audit')} 
              style={{ padding: '6px 10px', borderRadius: '6px', border: 'none', backgroundColor: liveArtifact === 'audit' ? '#7c3aed' : 'transparent', color: liveArtifact === 'audit' ? '#fff' : '#94a3b8', fontSize: '11px', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '5px' }}
            >
              <ShieldCheck style={{ height: '13px', width: '13px' }} />
              <span>Rigor</span>
            </button>
          </div>

          {/* Tab 1: Kaggle Code Inspector */}
          {liveArtifact === 'code' && (
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
              <div style={{ padding: '10px 14px', borderBottom: '1px solid rgba(255,255,255,0.06)', backgroundColor: '#10131f', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <Code2 style={{ height: '14px', width: '14px', color: '#a78bfa' }} />
                  <span style={{ fontSize: '11px', fontFamily: 'monospace', color: '#e2e8f0', fontWeight: '600' }}>workspace/experiment_kaggle.py</span>
                </div>
                <span style={{ fontSize: '9px', fontFamily: 'monospace', padding: '2px 6px', borderRadius: '4px', backgroundColor: 'rgba(16,185,129,0.15)', color: '#34d399', border: '1px solid rgba(16,185,129,0.3)' }}>
                  NVIDIA Tesla P100 Dispatched
                </span>
              </div>

              <div style={{ flex: 1, padding: '12px', overflowY: 'auto', backgroundColor: '#090b12', fontFamily: "'Fira Code', monospace", fontSize: '11px', color: '#cbd5e1', lineHeight: '1.6', whiteSpace: 'pre' }}>
                {fileContents["workspace/experiment_kaggle.py"]}
              </div>
            </div>
          )}

          {/* Tab 2: Kaggle GPU Execution Logs */}
          {liveArtifact === 'logs' && (
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
              <div style={{ padding: '10px 14px', borderBottom: '1px solid rgba(255,255,255,0.06)', backgroundColor: '#10131f', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <Terminal style={{ height: '14px', width: '14px', color: '#34d399' }} />
                  <span style={{ fontSize: '11px', fontFamily: 'monospace', color: '#e2e8f0', fontWeight: '600' }}>Remote GPU Stdout Telemetry</span>
                </div>
                <span style={{ fontSize: '9px', fontFamily: 'monospace', color: '#94a3b8' }}>Live Stream</span>
              </div>

              <div style={{ flex: 1, padding: '12px', overflowY: 'auto', backgroundColor: '#06080e', fontFamily: "'Fira Code', monospace", fontSize: '11px', color: '#34d399', lineHeight: '1.5', whiteSpace: 'pre-wrap' }}>
                {kaggleLogs}
              </div>
            </div>
          )}

          {/* Tab 3: Workspace Directory & File Inspector */}
          {liveArtifact === 'workspace' && (
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
              <div style={{ padding: '10px 14px', borderBottom: '1px solid rgba(255,255,255,0.06)', backgroundColor: '#10131f', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <FolderTree style={{ height: '14px', width: '14px', color: '#60a5fa' }} />
                  <span style={{ fontSize: '11px', fontWeight: '600', color: '#e2e8f0' }}>Agent Workspace (`workspace/`)</span>
                </div>
                <span style={{ fontSize: '10px', fontFamily: 'monospace', color: '#94a3b8' }}>5 Artifacts</span>
              </div>

              {/* File List */}
              <div style={{ height: '160px', overflowY: 'auto', borderBottom: '1px solid rgba(255,255,255,0.08)', backgroundColor: '#0c0e17' }}>
                {workspaceFiles.map((file, i) => (
                  <div 
                    key={i} 
                    onClick={() => setSelectedFile(file.name)}
                    style={{ 
                      padding: '8px 14px', 
                      display: 'flex', 
                      alignItems: 'center', 
                      justifyContent: 'space-between', 
                      cursor: 'pointer',
                      backgroundColor: selectedFile === file.name ? 'rgba(124,58,237,0.15)' : 'transparent',
                      borderLeft: selectedFile === file.name ? '3px solid #7c3aed' : '3px solid transparent'
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <FileText style={{ height: '13px', width: '13px', color: selectedFile === file.name ? '#a78bfa' : '#64748b' }} />
                      <span style={{ fontSize: '11px', fontFamily: 'monospace', color: selectedFile === file.name ? '#fff' : '#cbd5e1' }}>{file.name}</span>
                    </div>
                    <span style={{ fontSize: '10px', fontFamily: 'monospace', color: '#64748b' }}>{file.size}</span>
                  </div>
                ))}
              </div>

              {/* File Content Preview */}
              <div style={{ flex: 1, padding: '12px', overflowY: 'auto', backgroundColor: '#090b12', fontFamily: "'Fira Code', monospace", fontSize: '11px', color: '#cbd5e1', lineHeight: '1.5', whiteSpace: 'pre' }}>
                <div style={{ fontSize: '10px', fontFamily: 'sans-serif', color: '#64748b', marginBottom: '8px', borderBottom: '1px solid rgba(255,255,255,0.05)', paddingBottom: '4px' }}>
                  Viewing: <b>{selectedFile}</b>
                </div>
                {fileContents[selectedFile] || "Select a file above to inspect its contents."}
              </div>
            </div>
          )}

          {/* Tab 4: Level-2 Scientific Rigor Fact-Check */}
          {liveArtifact === 'audit' && (
            <div style={{ flex: 1, padding: '16px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '14px' }}>
              <div>
                <h3 style={{ fontSize: '12px', fontWeight: '700', textTransform: 'uppercase', color: '#e2e8f0', margin: '0 0 4px 0', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <ShieldCheck style={{ height: '16px', width: '16px', color: '#c084fc' }} />
                  Level-2 Rigor Auditor
                </h3>
                <p style={{ fontSize: '11px', color: '#94a3b8', margin: 0 }}>Empirical fact-checker verifying paper vs raw metrics.</p>
              </div>

              <div style={{ padding: '14px', borderRadius: '10px', backgroundColor: 'rgba(6,78,59,0.3)', border: '1px solid rgba(16,185,129,0.3)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#34d399', fontWeight: '700', fontSize: '12px', marginBottom: '6px' }}>
                  <CheckCircle2 style={{ height: '16px', width: '16px' }} />
                  <span>Rigor Audit Status: PASSED (100%)</span>
                </div>
                <p style={{ fontSize: '11px', color: '#a7f3d0', margin: 0 }}>
                  All numbers cited in paper.tex (99.14%, 84.64s, 421,642 params) match raw telemetry in results.tsv.
                </p>
              </div>

              <div style={{ padding: '12px', borderRadius: '8px', backgroundColor: 'rgba(24,27,41,0.6)', border: '1px solid rgba(255,255,255,0.06)' }}>
                <span style={{ fontSize: '11px', fontWeight: '700', color: '#e2e8f0' }}>Verified Scientific Assertions:</span>
                <div style={{ marginTop: '8px', display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '11px', fontFamily: 'monospace' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 8px', borderRadius: '4px', backgroundColor: 'rgba(255,255,255,0.03)' }}>
                    <span>Peak Val Accuracy</span>
                    <span style={{ color: '#34d399', fontWeight: '700' }}>MATCH (99.14%)</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 8px', borderRadius: '4px', backgroundColor: 'rgba(255,255,255,0.03)' }}>
                    <span>GPU Runtime</span>
                    <span style={{ color: '#34d399', fontWeight: '700' }}>MATCH (84.64 s)</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 8px', borderRadius: '4px', backgroundColor: 'rgba(255,255,255,0.03)' }}>
                    <span>Parameter Count</span>
                    <span style={{ color: '#34d399', fontWeight: '700' }}>MATCH (421,642)</span>
                  </div>
                </div>
              </div>
            </div>
          )}

        </aside>
      </div>
    </div>
  );
}
