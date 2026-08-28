import React, { useState } from 'react';
import { 
  FlaskConical, 
  FileText, 
  CheckCircle2, 
  Layers, 
  Sparkles, 
  BarChart3, 
  ShieldCheck, 
  ExternalLink,
  Database
} from 'lucide-react';

export default function App() {
  const [liveArtifact, setLiveArtifact] = useState('charts');

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
        <aside style={{ width: '300px', borderRight: '1px solid rgba(255,255,255,0.08)', backgroundColor: 'rgba(15,17,26,0.7)', padding: '16px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '20px' }}>
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
                    <CheckCircle2 style={{ height: '14px', width: '14px', color: '#34d399' }} />
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

        {/* 📊 Right Panel: Live Research Studio Artifact & Telemetry Viewer */}
        <aside style={{ width: '360px', borderLeft: '1px solid rgba(255,255,255,0.08)', backgroundColor: 'rgba(15,17,26,0.7)', display: 'flex', flexDirection: 'column' }}>
          
          {/* Tab Selection */}
          <div style={{ height: '48px', borderBottom: '1px solid rgba(255,255,255,0.08)', display: 'flex', alignItems: 'center', justifyContent: 'space-around', padding: '0 8px' }}>
            <button onClick={() => setLiveArtifact('charts')} style={{ padding: '6px 12px', borderRadius: '6px', border: 'none', backgroundColor: liveArtifact === 'charts' ? '#7c3aed' : 'transparent', color: liveArtifact === 'charts' ? '#fff' : '#94a3b8', fontSize: '12px', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <BarChart3 style={{ height: '14px', width: '14px' }} />
              <span>Plots</span>
            </button>
            <button onClick={() => setLiveArtifact('paper')} style={{ padding: '6px 12px', borderRadius: '6px', border: 'none', backgroundColor: liveArtifact === 'paper' ? '#7c3aed' : 'transparent', color: liveArtifact === 'paper' ? '#fff' : '#94a3b8', fontSize: '12px', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <FileText style={{ height: '14px', width: '14px' }} />
              <span>Paper</span>
            </button>
            <button onClick={() => setLiveArtifact('audit')} style={{ padding: '6px 12px', borderRadius: '6px', border: 'none', backgroundColor: liveArtifact === 'audit' ? '#7c3aed' : 'transparent', color: liveArtifact === 'audit' ? '#fff' : '#94a3b8', fontSize: '12px', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <ShieldCheck style={{ height: '14px', width: '14px' }} />
              <span>Audit</span>
            </button>
          </div>

          {/* Tab Content */}
          <div style={{ flex: 1, padding: '16px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {liveArtifact === 'charts' && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                <div>
                  <h3 style={{ fontSize: '12px', fontWeight: '700', textTransform: 'uppercase', color: '#e2e8f0', margin: '0 0 4px 0', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <BarChart3 style={{ height: '16px', width: '16px', color: '#34d399' }} />
                    Empirical Convergence Curves
                  </h3>
                  <p style={{ fontSize: '11px', color: '#94a3b8', margin: 0 }}>Generated by `plot-worker` on real Kaggle GPU training metrics.</p>
                </div>

                <div style={{ padding: '14px', borderRadius: '10px', backgroundColor: 'rgba(24,27,41,0.6)', border: '1px solid rgba(255,255,255,0.08)' }}>
                  <div style={{ height: '160px', width: '100%', borderRadius: '8px', backgroundColor: '#0f111a', border: '1px solid rgba(255,255,255,0.05)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                    <BarChart3 style={{ height: '40px', width: '40px', color: '#a78bfa', marginBottom: '8px' }} />
                    <span style={{ fontFamily: 'monospace', fontSize: '12px', color: '#cbd5e1' }}>Loss vs Validation Accuracy Trajectory</span>
                    <span style={{ fontSize: '11px', color: '#34d399', fontFamily: 'monospace', marginTop: '4px' }}>Peak Val Acc: 99.14% (Epoch 7)</span>
                  </div>
                </div>

                <div style={{ padding: '12px', borderRadius: '10px', backgroundColor: 'rgba(24,27,41,0.6)', border: '1px solid rgba(255,255,255,0.08)' }}>
                  <span style={{ fontSize: '12px', fontWeight: '700', color: '#e2e8f0' }}>Raw Metrics Extract (results.tsv)</span>
                  <div style={{ backgroundColor: '#0b0c13', padding: '10px', borderRadius: '6px', fontFamily: 'monospace', fontSize: '11px', color: '#cbd5e1', marginTop: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
                    <div style={{ color: '#94a3b8', fontWeight: '600', borderBottom: '1px solid rgba(255,255,255,0.08)', paddingBottom: '4px' }}>epoch | train_loss | val_acc | time(s)</div>
                    <div style={{ marginTop: '4px' }}>1     | 0.16981    | 98.40%  | 10.6s</div>
                    <div>4     | 0.02370    | 99.07%  | 10.5s</div>
                    <div style={{ color: '#34d399', fontWeight: '700' }}>7     | 0.00990    | 99.14%  | 10.6s ★</div>
                    <div>8     | 0.01022    | 98.99%  | 10.5s</div>
                  </div>
                </div>
              </div>
            )}

            {liveArtifact === 'paper' && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <div>
                  <h3 style={{ fontSize: '12px', fontWeight: '700', textTransform: 'uppercase', color: '#e2e8f0', margin: '0 0 4px 0', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <FileText style={{ height: '16px', width: '16px', color: '#fbbf24' }} />
                    Synthesized LaTeX Manuscript
                  </h3>
                  <p style={{ fontSize: '11px', color: '#94a3b8', margin: 0 }}>Produced by `write-worker` via `render_latex_manuscript`.</p>
                </div>

                <div style={{ padding: '16px', borderRadius: '10px', backgroundColor: 'rgba(24,27,41,0.6)', border: '1px solid rgba(255,255,255,0.08)', fontSize: '12px', lineHeight: '1.6' }}>
                  <div style={{ textAlign: 'center', borderBottom: '1px solid rgba(255,255,255,0.08)', paddingBottom: '8px', marginBottom: '8px' }}>
                    <h4 style={{ fontWeight: '700', fontSize: '13px', color: '#fff', margin: 0 }}>Reproducible Cloud-GPU MNIST Benchmark</h4>
                    <p style={{ fontSize: '10px', color: '#94a3b8', fontStyle: 'italic', margin: '2px 0 0 0' }}>A Baseline CNN Smoke Test on Kaggle Tesla P100</p>
                    <span style={{ fontSize: '10px', fontFamily: 'monospace', color: '#a78bfa' }}>Author: atharvagupta123</span>
                  </div>

                  <div style={{ marginTop: '8px' }}>
                    <span style={{ fontWeight: '700', fontSize: '11px', color: '#c4b5fd', textTransform: 'uppercase' }}>Abstract</span>
                    <p style={{ fontSize: '11px', color: '#cbd5e1', margin: '4px 0 0 0' }}>
                      We report a minimal, fully reproducible experiment validating a cloud-GPU training pipeline on Kaggle’s Tesla P100. The model reaches a best validation accuracy of 99.14% in roughly 85 seconds of training.
                    </p>
                  </div>
                </div>
              </div>
            )}

            {liveArtifact === 'audit' && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <div>
                  <h3 style={{ fontSize: '12px', fontWeight: '700', textTransform: 'uppercase', color: '#e2e8f0', margin: '0 0 4px 0', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <ShieldCheck style={{ height: '16px', width: '16px', color: '#c084fc' }} />
                    Level-2 Scientific Rigor Fact-Checker
                  </h3>
                  <p style={{ fontSize: '11px', color: '#94a3b8', margin: 0 }}>Zero metric hallucinations guaranteed against raw logs.</p>
                </div>

                <div style={{ padding: '14px', borderRadius: '10px', backgroundColor: 'rgba(6,78,59,0.3)', border: '1px solid rgba(16,185,129,0.3)' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#34d399', fontWeight: '700', fontSize: '12px', marginBottom: '6px' }}>
                    <CheckCircle2 style={{ height: '16px', width: '16px' }} />
                    <span>Rigor Audit Status: PASSED (100%)</span>
                  </div>
                  <p style={{ fontSize: '11px', color: '#a7f3d0', margin: 0 }}>
                    All numbers cited in paper.tex (99.14%, 84.64s, 421,642 params) matched raw telemetry in results.tsv.
                  </p>
                </div>
              </div>
            )}
          </div>
        </aside>
      </div>
    </div>
  );
}
