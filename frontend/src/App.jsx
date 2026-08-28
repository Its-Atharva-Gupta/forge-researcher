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
  Database,
  Inbox
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

          {/* Clean Ready-State Surface */}
          <div style={{ flex: 1, padding: '24px 16px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center', gap: '14px' }}>
            <div style={{ height: '56px', width: '56px', borderRadius: '16px', backgroundColor: 'rgba(124,58,237,0.1)', border: '1px solid rgba(124,58,237,0.25)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Inbox style={{ height: '26px', width: '26px', color: '#a78bfa' }} />
            </div>

            <div>
              <h4 style={{ fontSize: '13px', fontWeight: '700', color: '#f1f5f9', margin: '0 0 6px 0' }}>Artifact Studio Ready</h4>
              <p style={{ fontSize: '12px', color: '#94a3b8', lineHeight: '1.5', margin: 0, maxWidth: '280px' }}>
                When you initiate a research query, your generated <b>dual-axis loss curves</b>, <b>compiled LaTeX manuscripts</b>, and <b>Level-2 rigor audits</b> will render live in this panel!
              </p>
            </div>

            <div style={{ marginTop: '8px', padding: '10px 14px', borderRadius: '8px', backgroundColor: 'rgba(24,27,41,0.6)', border: '1px solid rgba(255,255,255,0.06)', width: '100%', boxSizing: 'border-box' }}>
              <div style={{ fontSize: '11px', fontWeight: '600', color: '#cbd5e1', marginBottom: '4px' }}>Awaiting First Experiment</div>
              <div style={{ fontSize: '10px', fontFamily: 'monospace', color: '#64748b' }}>Status: Idle & Ready for Query</div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}
