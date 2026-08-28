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
  Cpu,
  Inbox,
  Image as ImageIcon,
  BookOpen,
  Calendar,
  UserCheck
} from 'lucide-react';

export default function App() {
  const [liveArtifact, setLiveArtifact] = useState('literature');
  const [workspaceFiles, setWorkspaceFiles] = useState([]);
  const [papers, setPapers] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileData, setFileData] = useState({ is_image: false, content: "" });
  const [kaggleData, setKaggleData] = useState({ active: false, log: "", message: "Awaiting first GPU experiment dispatch..." });
  const [isRefreshing, setIsRefreshing] = useState(false);

  const fetchWorkspaceAndLiterature = async () => {
    setIsRefreshing(true);
    // 1. Files
    try {
      const res = await fetch('http://localhost:8796/api/workspace/files');
      const data = await res.json();
      setWorkspaceFiles(data.files || []);
      if (data.files && data.files.length > 0 && !selectedFile) {
        loadFileContent(data.files[0].path);
      }
    } catch (e) {
      setWorkspaceFiles([]);
    }

    // 2. Papers Discovered via arXiv & Semantic Scholar
    try {
      const paperRes = await fetch('http://localhost:8796/api/literature/papers');
      const paperData = await paperRes.json();
      setPapers(paperData.papers || []);
    } catch (e) {
      setPapers([]);
    }

    // 3. Kaggle Logs
    try {
      const logRes = await fetch('http://localhost:8796/api/kaggle/latest-logs');
      const logData = await logRes.json();
      setKaggleData(logData);
    } catch (e) {
      setKaggleData({ active: false, message: "Awaiting first GPU experiment dispatch..." });
    }
    setIsRefreshing(false);
  };

  const loadFileContent = async (filePath) => {
    setSelectedFile(filePath);
    try {
      const res = await fetch(`http://localhost:8796/api/workspace/file?path=${encodeURIComponent(filePath)}`);
      const data = await res.json();
      setFileData({
        is_image: data.is_image || false,
        content: data.content || "Empty file"
      });
    } catch (e) {
      setFileData({ is_image: false, content: "Error reading file." });
    }
  };

  useEffect(() => {
    fetchWorkspaceAndLiterature();
    const interval = setInterval(fetchWorkspaceAndLiterature, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', width: '100vw', backgroundColor: '#07080c', color: '#f1f5f9', fontFamily: "'Plus Jakarta Sans', sans-serif" }}>
      
      {/* 🌟 Top Navigation: Live Hardware & Service Telemetry */}
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

        {/* Telemetry Badges */}
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
            <BookOpen style={{ height: '14px', width: '14px', color: '#fbbf24' }} />
            <span style={{ color: '#94a3b8' }}>arXiv / Scholar:</span>
            <span style={{ color: '#fbbf24', fontFamily: 'monospace', fontWeight: '600' }}>{papers.length} Papers Read</span>
          </div>

          <a href="http://localhost:8790" target="_blank" rel="noreferrer" style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', color: '#c4b5fd', padding: '6px 12px', borderRadius: '6px', backgroundColor: 'rgba(124,58,237,0.15)', border: '1px solid rgba(124,58,237,0.3)', textDecoration: 'none' }}>
            <span>TrueForge Core</span>
            <ExternalLink style={{ height: '12px', width: '12px' }} />
          </a>
        </div>
      </header>

      {/* 🚀 Main Split-Screen Workspace */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        
        {/* 💬 Center Panel: TRUE LIVE TrueForge Backend WebSocket Chat Container */}
        <main style={{ flex: 1, display: 'flex', flexDirection: 'column', backgroundColor: '#090a0f', position: 'relative' }}>
          <iframe 
            src="http://localhost:8790" 
            style={{ width: '100%', height: '100%', border: 'none', backgroundColor: '#090a0f' }}
            title="TrueForge Live Agent Chat"
          />
        </main>

        {/* 📊 Right Panel: Researched Literature Feed, Workspace Explorer & GPU Stream */}
        <aside style={{ width: '520px', borderLeft: '1px solid rgba(255,255,255,0.08)', backgroundColor: 'rgba(15,17,26,0.92)', display: 'flex', flexDirection: 'column' }}>
          
          {/* Tab Navigation */}
          <div style={{ height: '48px', borderBottom: '1px solid rgba(255,255,255,0.08)', display: 'flex', alignItems: 'center', justifyContent: 'space-around', padding: '0 8px', backgroundColor: '#0c0e17' }}>
            <button 
              onClick={() => setLiveArtifact('literature')} 
              style={{ padding: '6px 12px', borderRadius: '6px', border: 'none', backgroundColor: liveArtifact === 'literature' ? '#7c3aed' : 'transparent', color: liveArtifact === 'literature' ? '#fff' : '#94a3b8', fontSize: '12px', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}
            >
              <BookOpen style={{ height: '14px', width: '14px' }} />
              <span>Researched Papers ({papers.length})</span>
            </button>
            <button 
              onClick={() => setLiveArtifact('workspace')} 
              style={{ padding: '6px 12px', borderRadius: '6px', border: 'none', backgroundColor: liveArtifact === 'workspace' ? '#7c3aed' : 'transparent', color: liveArtifact === 'workspace' ? '#fff' : '#94a3b8', fontSize: '12px', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}
            >
              <FolderTree style={{ height: '14px', width: '14px' }} />
              <span>Workspace Files ({workspaceFiles.length})</span>
            </button>
            <button 
              onClick={() => setLiveArtifact('logs')} 
              style={{ padding: '6px 12px', borderRadius: '6px', border: 'none', backgroundColor: liveArtifact === 'logs' ? '#7c3aed' : 'transparent', color: liveArtifact === 'logs' ? '#fff' : '#94a3b8', fontSize: '12px', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}
            >
              <Terminal style={{ height: '14px', width: '14px' }} />
              <span>Kaggle GPU Logs</span>
            </button>
          </div>

          {/* TAB 1: Real Researched Literature Feed (arXiv & Semantic Scholar) */}
          {liveArtifact === 'literature' && (
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
              <div style={{ padding: '10px 14px', borderBottom: '1px solid rgba(255,255,255,0.06)', backgroundColor: '#10131f', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <BookOpen style={{ height: '14px', width: '14px', color: '#fbbf24' }} />
                  <span style={{ fontSize: '11px', fontWeight: '600', color: '#e2e8f0' }}>Literature & Citations Discovered</span>
                </div>
                <button onClick={fetchWorkspaceAndLiterature} style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '10px' }}>
                  <RefreshCw style={{ height: '11px', width: '11px', animation: isRefreshing ? 'spin 1s linear infinite' : 'none' }} />
                  <span>Sync</span>
                </button>
              </div>

              <div style={{ flex: 1, padding: '14px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {papers.length === 0 ? (
                  <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '24px', textAlign: 'center', gap: '12px' }}>
                    <div style={{ height: '48px', width: '48px', borderRadius: '14px', backgroundColor: 'rgba(251,191,36,0.1)', border: '1px solid rgba(251,191,36,0.25)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                      <BookOpen style={{ height: '22px', width: '22px', color: '#fbbf24' }} />
                    </div>
                    <div>
                      <h4 style={{ fontSize: '12px', fontWeight: '700', color: '#f1f5f9', margin: '0 0 4px 0' }}>No literature queried yet</h4>
                      <p style={{ fontSize: '11px', color: '#94a3b8', lineHeight: '1.5', margin: 0, maxWidth: '280px' }}>
                        When your agent searches for papers using <code>search_arxiv</code> or <code>search_semantic_scholar</code>, they will appear here with title, authors, abstract, and PDF links!
                      </p>
                    </div>
                  </div>
                ) : (
                  papers.map((paper, idx) => (
                    <div key={idx} style={{ padding: '14px', borderRadius: '10px', backgroundColor: 'rgba(24,27,41,0.7)', border: '1px solid rgba(255,255,255,0.08)', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '8px' }}>
                        <h4 style={{ fontSize: '12px', fontWeight: '700', color: '#f8fafc', lineHeight: '1.4', margin: 0 }}>
                          {paper.title}
                        </h4>
                        <span style={{ fontSize: '9px', fontFamily: 'monospace', padding: '2px 6px', borderRadius: '4px', backgroundColor: 'rgba(251,191,36,0.15)', color: '#fbbf24', border: '1px solid rgba(251,191,36,0.3)', whiteSpace: 'nowrap' }}>
                          {paper.source}
                        </span>
                      </div>

                      {/* Authors & Published Date */}
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', fontSize: '10px', color: '#94a3b8' }}>
                        {paper.authors && paper.authors.length > 0 && (
                          <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                            <UserCheck style={{ height: '12px', width: '12px', color: '#a78bfa' }} />
                            <span>{paper.authors.slice(0, 3).join(', ')}{paper.authors.length > 3 ? ' et al.' : ''}</span>
                          </div>
                        )}
                        {paper.published && (
                          <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                            <Calendar style={{ height: '12px', width: '12px', color: '#60a5fa' }} />
                            <span>{paper.published.split('T')[0]}</span>
                          </div>
                        )}
                      </div>

                      {/* Summary Abstract */}
                      {paper.summary && (
                        <p style={{ fontSize: '11px', color: '#cbd5e1', lineHeight: '1.5', margin: 0, display: '-webkit-box', WebkitLineClamp: 3, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                          {paper.summary}
                        </p>
                      )}

                      {/* URL Link */}
                      {paper.url && (
                        <div style={{ marginTop: '2px', borderTop: '1px solid rgba(255,255,255,0.05)', paddingTop: '6px' }}>
                          <a href={paper.url} target="_blank" rel="noreferrer" style={{ fontSize: '10px', fontFamily: 'monospace', color: '#a78bfa', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '4px' }}>
                            <span>Read Full Manuscript / PDF</span>
                            <ExternalLink style={{ height: '10px', width: '10px' }} />
                          </a>
                        </div>
                      )}
                    </div>
                  ))
                )}
              </div>
            </div>
          )}

          {/* TAB 2: Workspace Files */}
          {liveArtifact === 'workspace' && (
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
              <div style={{ padding: '10px 14px', borderBottom: '1px solid rgba(255,255,255,0.06)', backgroundColor: '#10131f', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <FolderTree style={{ height: '14px', width: '14px', color: '#60a5fa' }} />
                  <span style={{ fontSize: '11px', fontWeight: '600', color: '#e2e8f0' }}>workspace/ directory</span>
                </div>
                <button onClick={fetchWorkspaceAndLiterature} style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '10px' }}>
                  <RefreshCw style={{ height: '11px', width: '11px', animation: isRefreshing ? 'spin 1s linear infinite' : 'none' }} />
                  <span>Sync</span>
                </button>
              </div>

              {workspaceFiles.length === 0 ? (
                <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '24px', textAlign: 'center', gap: '12px' }}>
                  <div style={{ height: '48px', width: '48px', borderRadius: '14px', backgroundColor: 'rgba(124,58,237,0.1)', border: '1px solid rgba(124,58,237,0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Inbox style={{ height: '22px', width: '22px', color: '#a78bfa' }} />
                  </div>
                  <div>
                    <h4 style={{ fontSize: '12px', fontWeight: '700', color: '#f1f5f9', margin: '0 0 4px 0' }}>Workspace is currently empty</h4>
                    <p style={{ fontSize: '11px', color: '#94a3b8', lineHeight: '1.5', margin: 0, maxWidth: '260px' }}>
                      When your agent generates experiment scripts, <code>results.tsv</code>, figures, or <code>paper.tex</code>, they will appear here live!
                    </p>
                  </div>
                </div>
              ) : (
                <>
                  {/* File List */}
                  <div style={{ height: '140px', overflowY: 'auto', borderBottom: '1px solid rgba(255,255,255,0.08)', backgroundColor: '#0c0e17' }}>
                    {workspaceFiles.map((file, i) => (
                      <div 
                        key={i} 
                        onClick={() => loadFileContent(file.path)}
                        style={{ 
                          padding: '8px 14px', 
                          display: 'flex', 
                          alignItems: 'center', 
                          justifyContent: 'space-between', 
                          cursor: 'pointer',
                          backgroundColor: selectedFile === file.path ? 'rgba(124,58,237,0.15)' : 'transparent',
                          borderLeft: selectedFile === file.path ? '3px solid #7c3aed' : '3px solid transparent'
                        }}
                      >
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          {file.is_image ? (
                            <ImageIcon style={{ height: '13px', width: '13px', color: '#34d399' }} />
                          ) : (
                            <FileText style={{ height: '13px', width: '13px', color: selectedFile === file.path ? '#a78bfa' : '#64748b' }} />
                          )}
                          <span style={{ fontSize: '11px', fontFamily: 'monospace', color: selectedFile === file.path ? '#fff' : '#cbd5e1' }}>{file.path}</span>
                        </div>
                        <span style={{ fontSize: '10px', fontFamily: 'monospace', color: '#64748b' }}>{file.size}</span>
                      </div>
                    ))}
                  </div>

                  {/* File / Image Content Preview */}
                  <div style={{ flex: 1, padding: '14px', overflowY: 'auto', backgroundColor: '#090b12', display: 'flex', flexDirection: 'column' }}>
                    <div style={{ fontSize: '10px', fontFamily: 'sans-serif', color: '#64748b', marginBottom: '8px', borderBottom: '1px solid rgba(255,255,255,0.05)', paddingBottom: '4px' }}>
                      Viewing: <b>{selectedFile}</b>
                    </div>

                    {fileData.is_image ? (
                      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '10px', backgroundColor: '#06070a', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.06)' }}>
                        <img 
                          src={fileData.content} 
                          alt={selectedFile} 
                          style={{ maxWidth: '100%', maxHeight: '280px', borderRadius: '6px', objectFit: 'contain', boxShadow: '0 4px 20px rgba(0,0,0,0.5)' }} 
                        />
                        <span style={{ fontSize: '10px', fontFamily: 'monospace', color: '#34d399', marginTop: '8px' }}>
                          Generated Academic Figure
                        </span>
                      </div>
                    ) : (
                      <div style={{ fontFamily: "'Fira Code', monospace", fontSize: '11px', color: '#cbd5e1', lineHeight: '1.5', whiteSpace: 'pre-wrap' }}>
                        {fileData.content}
                      </div>
                    )}
                  </div>
                </>
              )}
            </div>
          )}

          {/* TAB 3: Kaggle GPU Logs */}
          {liveArtifact === 'logs' && (
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
              <div style={{ padding: '10px 14px', borderBottom: '1px solid rgba(255,255,255,0.06)', backgroundColor: '#10131f', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <Terminal style={{ height: '14px', width: '14px', color: '#34d399' }} />
                  <span style={{ fontSize: '11px', fontFamily: 'monospace', color: '#e2e8f0', fontWeight: '600' }}>Kaggle Cloud GPU Telemetry</span>
                </div>
                <span style={{ fontSize: '9px', fontFamily: 'monospace', color: '#94a3b8' }}>Live</span>
              </div>

              <div style={{ flex: 1, padding: '14px', overflowY: 'auto', backgroundColor: '#06080e', fontFamily: "'Fira Code', monospace", fontSize: '11px', color: '#34d399', lineHeight: '1.5', whiteSpace: 'pre-wrap' }}>
                {kaggleData.active ? kaggleData.log : (
                  <div style={{ color: '#64748b', textAlign: 'center', marginTop: '40px' }}>
                    <Cpu style={{ height: '32px', width: '32px', color: '#475569', margin: '0 auto 10px auto' }} />
                    <p style={{ margin: 0 }}>No remote GPU experiments currently running.</p>
                    <p style={{ fontSize: '10px', marginTop: '4px' }}>When you dispatch a run with <code>run_experiment_on_kaggle_gpu</code>, live logs will stream here!</p>
                  </div>
                )}
              </div>
            </div>
          )}

        </aside>
      </div>
    </div>
  );
}
