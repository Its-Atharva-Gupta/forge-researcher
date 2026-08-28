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
  UserCheck,
  ChevronRight,
  Copy,
  Check,
  Maximize2
} from 'lucide-react';

export default function App() {
  const [liveArtifact, setLiveArtifact] = useState('literature');
  const [workspaceFiles, setWorkspaceFiles] = useState([]);
  const [papers, setPapers] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileData, setFileData] = useState({ is_image: false, content: "" });
  const [kaggleData, setKaggleData] = useState({ active: false, log: "", message: "Awaiting first GPU experiment dispatch..." });
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [copied, setCopied] = useState(false);

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

  const copyCode = () => {
    if (fileData.content) {
      navigator.clipboard.writeText(fileData.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  useEffect(() => {
    fetchWorkspaceAndLiterature();
    const interval = setInterval(fetchWorkspaceAndLiterature, 3000);
    return () => clearInterval(interval);
  }, []);

  const getFileBadge = (name) => {
    if (name.endsWith('.py')) return { label: 'PYTHON', bg: '#3b82f620', color: '#60a5fa', border: '#3b82f640' };
    if (name.endsWith('.tex')) return { label: 'LATEX', bg: '#8b5cf620', color: '#a78bfa', border: '#8b5cf640' };
    if (name.endsWith('.tsv') || name.endsWith('.csv')) return { label: 'DATA', bg: '#10b98120', color: '#34d399', border: '#10b98140' };
    if (name.endsWith('.json')) return { label: 'JSON', bg: '#f59e0b20', color: '#fbbf24', border: '#f59e0b40' };
    if (name.endsWith('.png') || name.endsWith('.jpg')) return { label: 'IMAGE', bg: '#ec489920', color: '#f472b6', border: '#ec489940' };
    return { label: 'FILE', bg: '#64748b20', color: '#94a3b8', border: '#64748b40' };
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', width: '100vw', backgroundColor: '#07080c', color: '#f1f5f9', fontFamily: "'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif" }}>
      
      {/* 🌟 Modern Glassmorphism Top Navigation */}
      <header style={{ height: '54px', borderBottom: '1px solid rgba(255,255,255,0.06)', backgroundColor: '#090a10', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 20px', zIndex: 20 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ height: '32px', width: '32px', borderRadius: '8px', background: 'linear-gradient(135deg, #7c3aed, #4f46e5)', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 4px 14px rgba(124,58,237,0.35)' }}>
            <FlaskConical style={{ height: '17px', width: '17px', color: '#fff' }} />
          </div>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px' }}>
            <span style={{ fontWeight: '800', fontSize: '14px', letterSpacing: '-0.02em', color: '#fff' }}>ForgeResearcher</span>
            <span style={{ fontSize: '10px', fontFamily: 'monospace', padding: '1px 6px', borderRadius: '4px', backgroundColor: 'rgba(124,58,237,0.15)', color: '#c4b5fd', border: '1px solid rgba(124,58,237,0.25)', fontWeight: '600' }}>STUDIO</span>
          </div>
        </div>

        {/* Telemetry Status Pills */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '4px 10px', borderRadius: '6px', backgroundColor: '#10121a', border: '1px solid rgba(255,255,255,0.06)', fontSize: '11px' }}>
            <span style={{ height: '7px', width: '7px', borderRadius: '50%', backgroundColor: '#10b981', display: 'inline-block' }}></span>
            <span style={{ color: '#94a3b8' }}>Kaggle GPU:</span>
            <span style={{ color: '#34d399', fontFamily: 'monospace', fontWeight: '600' }}>Tesla P100</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '4px 10px', borderRadius: '6px', backgroundColor: '#10121a', border: '1px solid rgba(255,255,255,0.06)', fontSize: '11px' }}>
            <Database style={{ height: '13px', width: '13px', color: '#60a5fa' }} />
            <span style={{ color: '#94a3b8' }}>Hugging Face:</span>
            <span style={{ color: '#60a5fa', fontFamily: 'monospace', fontWeight: '600' }}>Connected</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '4px 10px', borderRadius: '6px', backgroundColor: '#10121a', border: '1px solid rgba(255,255,255,0.06)', fontSize: '11px' }}>
            <BookOpen style={{ height: '13px', width: '13px', color: '#fbbf24' }} />
            <span style={{ color: '#94a3b8' }}>Literature:</span>
            <span style={{ color: '#fbbf24', fontFamily: 'monospace', fontWeight: '600' }}>{papers.length} Papers</span>
          </div>

          <a href="http://localhost:8790" target="_blank" rel="noreferrer" style={{ display: 'flex', alignItems: 'center', gap: '5px', fontSize: '11px', color: '#c4b5fd', padding: '4px 10px', borderRadius: '6px', backgroundColor: 'rgba(124,58,237,0.12)', border: '1px solid rgba(124,58,237,0.25)', textDecoration: 'none', fontWeight: '600' }}>
            <span>Core</span>
            <ExternalLink style={{ height: '11px', width: '11px' }} />
          </a>
        </div>
      </header>

      {/* 🚀 Main Split-Screen Workspace */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        
        {/* 💬 Center Panel: TRUE LIVE TrueForge Backend WebSocket Chat Container */}
        <main style={{ flex: 1, display: 'flex', flexDirection: 'column', backgroundColor: '#07080c', position: 'relative' }}>
          <iframe 
            src="http://localhost:8790" 
            style={{ width: '100%', height: '100%', border: 'none', backgroundColor: '#07080c' }}
            title="TrueForge Live Agent Chat"
          />
        </main>

        {/* 📊 Right Panel: High-End Studio Artifact & Literature Explorer */}
        <aside style={{ width: '560px', borderLeft: '1px solid rgba(255,255,255,0.08)', backgroundColor: '#0b0d14', display: 'flex', flexDirection: 'column' }}>
          
          {/* Segmented Studio Tabs */}
          <div style={{ padding: '10px 14px', borderBottom: '1px solid rgba(255,255,255,0.06)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', backgroundColor: '#080a10' }}>
            <div style={{ display: 'flex', gap: '6px', backgroundColor: '#121520', padding: '3px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
              <button 
                onClick={() => setLiveArtifact('literature')} 
                style={{ padding: '5px 12px', borderRadius: '6px', border: 'none', backgroundColor: liveArtifact === 'literature' ? '#7c3aed' : 'transparent', color: liveArtifact === 'literature' ? '#fff' : '#94a3b8', fontSize: '11px', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px', transition: 'all 0.15s ease' }}
              >
                <BookOpen style={{ height: '13px', width: '13px' }} />
                <span>Literature ({papers.length})</span>
              </button>
              <button 
                onClick={() => setLiveArtifact('workspace')} 
                style={{ padding: '5px 12px', borderRadius: '6px', border: 'none', backgroundColor: liveArtifact === 'workspace' ? '#7c3aed' : 'transparent', color: liveArtifact === 'workspace' ? '#fff' : '#94a3b8', fontSize: '11px', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px', transition: 'all 0.15s ease' }}
              >
                <FolderTree style={{ height: '13px', width: '13px' }} />
                <span>Workspace ({workspaceFiles.length})</span>
              </button>
              <button 
                onClick={() => setLiveArtifact('logs')} 
                style={{ padding: '5px 12px', borderRadius: '6px', border: 'none', backgroundColor: liveArtifact === 'logs' ? '#7c3aed' : 'transparent', color: liveArtifact === 'logs' ? '#fff' : '#94a3b8', fontSize: '11px', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px', transition: 'all 0.15s ease' }}
              >
                <Terminal style={{ height: '13px', width: '13px' }} />
                <span>GPU Logs</span>
              </button>
            </div>

            <button onClick={fetchWorkspaceAndLiterature} title="Sync latest artifacts" style={{ background: '#121520', border: '1px solid rgba(255,255,255,0.06)', color: '#94a3b8', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '11px', padding: '5px 8px', borderRadius: '6px' }}>
              <RefreshCw style={{ height: '12px', width: '12px', animation: isRefreshing ? 'spin 1s linear infinite' : 'none' }} />
              <span>Sync</span>
            </button>
          </div>

          {/* TAB 1: Real Researched Literature Feed (arXiv & Semantic Scholar) */}
          {liveArtifact === 'literature' && (
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
              <div style={{ flex: 1, padding: '16px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {papers.length === 0 ? (
                  <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '32px', textAlign: 'center', gap: '12px' }}>
                    <div style={{ height: '48px', width: '48px', borderRadius: '12px', backgroundColor: 'rgba(251,191,36,0.08)', border: '1px solid rgba(251,191,36,0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                      <BookOpen style={{ height: '22px', width: '22px', color: '#fbbf24' }} />
                    </div>
                    <div>
                      <h4 style={{ fontSize: '13px', fontWeight: '700', color: '#f1f5f9', margin: '0 0 4px 0' }}>No literature queried yet</h4>
                      <p style={{ fontSize: '11px', color: '#64748b', lineHeight: '1.5', margin: 0, maxWidth: '280px' }}>
                        When your agent searches for papers using <code>search_arxiv</code> or <code>search_semantic_scholar</code>, they will appear here with title, authors, abstract, and PDF links!
                      </p>
                    </div>
                  </div>
                ) : (
                  papers.map((paper, idx) => (
                    <div key={idx} style={{ padding: '14px 16px', borderRadius: '10px', backgroundColor: '#10131d', border: '1px solid rgba(255,255,255,0.06)', display: 'flex', flexDirection: 'column', gap: '10px', transition: 'border-color 0.15s ease' }}>
                      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '12px' }}>
                        <h4 style={{ fontSize: '13px', fontWeight: '700', color: '#f8fafc', lineHeight: '1.4', margin: 0, letterSpacing: '-0.01em' }}>
                          {paper.title}
                        </h4>
                        <span style={{ fontSize: '9px', fontFamily: 'monospace', padding: '2px 6px', borderRadius: '4px', backgroundColor: 'rgba(251,191,36,0.12)', color: '#fbbf24', border: '1px solid rgba(251,191,36,0.25)', whiteSpace: 'nowrap', fontWeight: '600' }}>
                          {paper.source}
                        </span>
                      </div>

                      {/* Authors & Published Date */}
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px', fontSize: '11px', color: '#94a3b8' }}>
                        {paper.authors && paper.authors.length > 0 && (
                          <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                            <UserCheck style={{ height: '13px', width: '13px', color: '#a78bfa' }} />
                            <span>{paper.authors.slice(0, 3).join(', ')}{paper.authors.length > 3 ? ' et al.' : ''}</span>
                          </div>
                        )}
                        {paper.published && (
                          <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                            <Calendar style={{ height: '13px', width: '13px', color: '#60a5fa' }} />
                            <span>{paper.published.split('T')[0]}</span>
                          </div>
                        )}
                      </div>

                      {/* Summary Abstract */}
                      {paper.summary && (
                        <p style={{ fontSize: '11.5px', color: '#cbd5e1', lineHeight: '1.6', margin: 0, backgroundColor: '#090b12', padding: '10px 12px', borderRadius: '6px', border: '1px solid rgba(255,255,255,0.03)' }}>
                          {paper.summary}
                        </p>
                      )}

                      {/* URL Link */}
                      {paper.url && (
                        <div style={{ display: 'flex', justifyContent: 'flex-end', paddingTop: '2px' }}>
                          <a href={paper.url} target="_blank" rel="noreferrer" style={{ fontSize: '11px', fontWeight: '600', color: '#a78bfa', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '5px', padding: '4px 8px', borderRadius: '4px', backgroundColor: 'rgba(124,58,237,0.1)' }}>
                            <span>Read Manuscript / PDF</span>
                            <ExternalLink style={{ height: '11px', width: '11px' }} />
                          </a>
                        </div>
                      )}
                    </div>
                  ))
                )}
              </div>
            </div>
          )}

          {/* TAB 2: Clean Studio Workspace Code & Image Inspector */}
          {liveArtifact === 'workspace' && (
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
              
              {/* Horizontal File Chips Bar */}
              <div style={{ padding: '8px 12px', borderBottom: '1px solid rgba(255,255,255,0.06)', backgroundColor: '#080a10', display: 'flex', gap: '6px', overflowX: 'auto', whiteSpace: 'nowrap' }}>
                {workspaceFiles.map((file, i) => {
                  const badge = getFileBadge(file.name);
                  const isSelected = selectedFile === file.path;
                  return (
                    <button 
                      key={i} 
                      onClick={() => loadFileContent(file.path)}
                      style={{ 
                        padding: '5px 10px', 
                        borderRadius: '6px', 
                        border: isSelected ? `1px solid ${badge.color}` : '1px solid rgba(255,255,255,0.05)', 
                        backgroundColor: isSelected ? '#161926' : '#0e111a', 
                        color: isSelected ? '#fff' : '#94a3b8', 
                        fontSize: '11px', 
                        fontWeight: '500', 
                        cursor: 'pointer', 
                        display: 'flex', 
                        alignItems: 'center', 
                        gap: '6px',
                        transition: 'all 0.15s ease'
                      }}
                    >
                      <span style={{ fontSize: '9px', fontFamily: 'monospace', padding: '1px 4px', borderRadius: '3px', backgroundColor: badge.bg, color: badge.color, border: `1px solid ${badge.border}`, fontWeight: '700' }}>
                        {badge.label}
                      </span>
                      <span style={{ fontFamily: 'monospace', fontSize: '11px' }}>{file.name}</span>
                    </button>
                  );
                })}
              </div>

              {/* Code Editor / Image Viewer Canvas */}
              <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden', backgroundColor: '#080a10' }}>
                
                {/* Editor Header */}
                <div style={{ height: '36px', borderBottom: '1px solid rgba(255,255,255,0.05)', padding: '0 14px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', backgroundColor: '#0a0c13' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <span style={{ fontSize: '11px', fontFamily: 'monospace', color: '#e2e8f0', fontWeight: '600' }}>
                      {selectedFile || "No file selected"}
                    </span>
                  </div>

                  {!fileData.is_image && fileData.content && (
                    <button 
                      onClick={copyCode} 
                      style={{ background: 'none', border: 'none', color: copied ? '#34d399' : '#94a3b8', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '10px', padding: '2px 6px', borderRadius: '4px' }}
                    >
                      {copied ? <Check style={{ height: '11px', width: '11px' }} /> : <Copy style={{ height: '11px', width: '11px' }} />}
                      <span>{copied ? 'Copied' : 'Copy'}</span>
                    </button>
                  )}
                </div>

                {/* Editor Content Surface */}
                <div style={{ flex: 1, padding: '14px', overflowY: 'auto' }}>
                  {fileData.is_image ? (
                    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '20px', backgroundColor: '#06070a', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.04)' }}>
                      <img 
                        src={fileData.content} 
                        alt={selectedFile} 
                        style={{ maxWidth: '100%', maxHeight: '340px', borderRadius: '6px', objectFit: 'contain', boxShadow: '0 8px 30px rgba(0,0,0,0.6)' }} 
                      />
                      <span style={{ fontSize: '10px', fontFamily: 'monospace', color: '#34d399', marginTop: '12px' }}>
                        ✓ Publication Loss / Benchmark Plot
                      </span>
                    </div>
                  ) : (
                    <pre style={{ margin: 0, fontFamily: "'Fira Code', 'JetBrains Mono', monospace", fontSize: '11.5px', color: '#cbd5e1', lineHeight: '1.65', whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
                      {fileData.content || "Select a file from the bar above."}
                    </pre>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* TAB 3: Kaggle GPU Telemetry Logs */}
          {liveArtifact === 'logs' && (
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden', backgroundColor: '#06080e' }}>
              <div style={{ height: '36px', padding: '0 14px', borderBottom: '1px solid rgba(255,255,255,0.05)', backgroundColor: '#0a0c13', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <Terminal style={{ height: '13px', width: '13px', color: '#34d399' }} />
                  <span style={{ fontSize: '11px', fontFamily: 'monospace', color: '#e2e8f0', fontWeight: '600' }}>Kaggle Cloud GPU Telemetry</span>
                </div>
                <span style={{ fontSize: '9px', fontFamily: 'monospace', color: '#34d399', backgroundColor: '#065f4630', padding: '1px 6px', borderRadius: '4px', border: '1px solid #05966940' }}>LIVE STREAM</span>
              </div>

              <div style={{ flex: 1, padding: '16px', overflowY: 'auto', fontFamily: "'Fira Code', monospace", fontSize: '11px', color: '#34d399', lineHeight: '1.6', whiteSpace: 'pre-wrap' }}>
                {kaggleData.active ? kaggleData.log : (
                  <div style={{ color: '#64748b', textAlign: 'center', marginTop: '40px' }}>
                    <Cpu style={{ height: '32px', width: '32px', color: '#475569', margin: '0 auto 10px auto' }} />
                    <p style={{ margin: 0, fontSize: '12px' }}>No remote GPU experiments currently running.</p>
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
