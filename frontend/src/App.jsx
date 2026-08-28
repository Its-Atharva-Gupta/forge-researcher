import React, { useState, useEffect } from 'react';
import { 
  FlaskConical, 
  FileText, 
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
  ArrowLeft,
  Copy,
  Check,
  FileCode,
  FileSpreadsheet,
  Plus,
  FolderPlus,
  Trash2,
  Edit2,
  Save,
  Folder,
  Layers,
  Sparkles,
  Bot
} from 'lucide-react';

export default function App() {
  const [liveArtifact, setLiveArtifact] = useState('subagents');
  const [workspaceFiles, setWorkspaceFiles] = useState([]);
  const [papers, setPapers] = useState([]);
  const [subagentTasks, setSubagentTasks] = useState([]);
  const [activeFile, setActiveFile] = useState(null);
  const [fileData, setFileData] = useState({ is_image: false, content: "" });
  const [kaggleData, setKaggleData] = useState({ active: false, log: "", message: "Awaiting first GPU experiment dispatch..." });
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [copied, setCopied] = useState(false);
  const [isSaved, setIsSaved] = useState(false);

  // New item modals / inputs
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [isCreatingFolder, setIsCreatingFolder] = useState(false);
  const [newItemName, setNewItemName] = useState("");
  const [renamingPath, setRenamingPath] = useState(null);
  const [renameValue, setRenameValue] = useState("");

  const fetchWorkspaceAndLiterature = async () => {
    setIsRefreshing(true);
    // 1. Subagent Delegations & Prompts
    try {
      const subRes = await fetch('http://localhost:8796/api/subagents/tasks');
      const subData = await subRes.json();
      setSubagentTasks(subData.tasks || []);
    } catch (e) {
      setSubagentTasks([]);
    }

    // 2. Files
    try {
      const res = await fetch('http://localhost:8796/api/workspace/files');
      const data = await res.json();
      setWorkspaceFiles(data.files || []);
    } catch (e) {
      setWorkspaceFiles([]);
    }

    // 3. Papers
    try {
      const paperRes = await fetch('http://localhost:8796/api/literature/papers');
      const paperData = await paperRes.json();
      setPapers(paperData.papers || []);
    } catch (e) {
      setPapers([]);
    }

    // 4. Kaggle Logs
    try {
      const logRes = await fetch('http://localhost:8796/api/kaggle/latest-logs');
      const logData = await logRes.json();
      setKaggleData(logData);
    } catch (e) {
      setKaggleData({ active: false, message: "Awaiting first GPU experiment dispatch..." });
    }
    setIsRefreshing(false);
  };

  const openFileViewer = async (filePath) => {
    setActiveFile(filePath);
    try {
      const res = await fetch(`http://localhost:8796/api/workspace/file?path=${encodeURIComponent(filePath)}`);
      const data = await res.json();
      setFileData({
        is_image: data.is_image || false,
        content: data.content || ""
      });
    } catch (e) {
      setFileData({ is_image: false, content: "Error reading file." });
    }
  };

  const closeFileViewer = () => {
    setActiveFile(null);
    setFileData({ is_image: false, content: "" });
  };

  const handleSaveFile = async () => {
    if (!activeFile || fileData.is_image) return;
    try {
      await fetch('http://localhost:8796/api/workspace/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: activeFile, content: fileData.content })
      });
      setIsSaved(true);
      setTimeout(() => setIsSaved(false), 2000);
      fetchWorkspaceAndLiterature();
    } catch (e) {
      alert("Error saving file: " + e.message);
    }
  };

  const handleCreateItem = async (e) => {
    e?.preventDefault();
    if (!newItemName.trim()) return;

    try {
      await fetch('http://localhost:8796/api/workspace/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: newItemName.trim(),
          is_folder: isCreatingFolder,
          content: isCreatingFolder ? "" : "# New Experiment File\n"
        })
      });
      setNewItemName("");
      setShowCreateModal(false);
      fetchWorkspaceAndLiterature();
    } catch (e) {
      alert("Error creating item: " + e.message);
    }
  };

  const handleDeleteItem = async (e, path) => {
    e.stopPropagation();
    if (!window.confirm(`Are you sure you want to delete '${path}'?`)) return;

    try {
      await fetch('http://localhost:8796/api/workspace/delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path })
      });
      if (activeFile === path) closeFileViewer();
      fetchWorkspaceAndLiterature();
    } catch (e) {
      alert("Error deleting item: " + e.message);
    }
  };

  const handleRenameItem = async (e, oldPath) => {
    e?.preventDefault();
    e?.stopPropagation();
    if (!renameValue.trim()) return;

    try {
      await fetch('http://localhost:8796/api/workspace/rename', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ old_path: oldPath, new_name: renameValue.trim() })
      });
      setRenamingPath(null);
      setRenameValue("");
      fetchWorkspaceAndLiterature();
    } catch (e) {
      alert("Error renaming item: " + e.message);
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

  const getFileIcon = (file) => {
    if (file.is_dir) return <Folder style={{ height: '16px', width: '16px', color: '#a78bfa' }} />;
    if (file.is_image) return <ImageIcon style={{ height: '16px', width: '16px', color: '#f472b6' }} />;
    if (file.name.endsWith('.py')) return <FileCode style={{ height: '16px', width: '16px', color: '#60a5fa' }} />;
    if (file.name.endsWith('.tex')) return <FileText style={{ height: '16px', width: '16px', color: '#a78bfa' }} />;
    if (file.name.endsWith('.tsv') || file.name.endsWith('.csv')) return <FileSpreadsheet style={{ height: '16px', width: '16px', color: '#34d399' }} />;
    return <FileText style={{ height: '16px', width: '16px', color: '#94a3b8' }} />;
  };

  const getBadgeStyle = (file) => {
    if (file.is_dir) return { label: 'DIR', color: '#a78bfa', bg: '#8b5cf618' };
    if (file.name.endsWith('.py')) return { label: 'PYTHON', color: '#60a5fa', bg: '#3b82f618' };
    if (file.name.endsWith('.tex')) return { label: 'LATEX', color: '#a78bfa', bg: '#8b5cf618' };
    if (file.name.endsWith('.tsv')) return { label: 'TSV', color: '#34d399', bg: '#10b98118' };
    if (file.name.endsWith('.json')) return { label: 'JSON', color: '#fbbf24', bg: '#f59e0b18' };
    if (file.name.endsWith('.png')) return { label: 'PNG PLOT', color: '#f472b6', bg: '#ec489918' };
    return { label: 'FILE', color: '#94a3b8', bg: '#64748b18' };
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', width: '100vw', backgroundColor: '#07080c', color: '#f1f5f9', fontFamily: "'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif" }}>
      
      {/* 🌟 Top Navigation Bar */}
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
            <Layers style={{ height: '13px', width: '13px', color: '#a78bfa' }} />
            <span style={{ color: '#94a3b8' }}>Subagents:</span>
            <span style={{ color: '#a78bfa', fontFamily: 'monospace', fontWeight: '600' }}>{subagentTasks.length} Dispatched</span>
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

        {/* 📊 Right Panel: Dedicated Studio Sidebar */}
        <aside style={{ width: '580px', borderLeft: '1px solid rgba(255,255,255,0.08)', backgroundColor: '#0b0d14', display: 'flex', flexDirection: 'column' }}>
          
          {/* Main Tab Controls (Hidden when viewing a full file) */}
          {!activeFile && (
            <div style={{ padding: '10px 14px', borderBottom: '1px solid rgba(255,255,255,0.06)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', backgroundColor: '#080a10' }}>
              <div style={{ display: 'flex', gap: '4px', backgroundColor: '#121520', padding: '3px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
                <button 
                  onClick={() => setLiveArtifact('subagents')} 
                  style={{ padding: '5px 10px', borderRadius: '6px', border: 'none', backgroundColor: liveArtifact === 'subagents' ? '#7c3aed' : 'transparent', color: liveArtifact === 'subagents' ? '#fff' : '#94a3b8', fontSize: '11px', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '5px' }}
                >
                  <Bot style={{ height: '13px', width: '13px' }} />
                  <span>Subagents ({subagentTasks.length})</span>
                </button>
                <button 
                  onClick={() => setLiveArtifact('workspace')} 
                  style={{ padding: '5px 10px', borderRadius: '6px', border: 'none', backgroundColor: liveArtifact === 'workspace' ? '#7c3aed' : 'transparent', color: liveArtifact === 'workspace' ? '#fff' : '#94a3b8', fontSize: '11px', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '5px' }}
                >
                  <FolderTree style={{ height: '13px', width: '13px' }} />
                  <span>Workspace ({workspaceFiles.length})</span>
                </button>
                <button 
                  onClick={() => setLiveArtifact('literature')} 
                  style={{ padding: '5px 10px', borderRadius: '6px', border: 'none', backgroundColor: liveArtifact === 'literature' ? '#7c3aed' : 'transparent', color: liveArtifact === 'literature' ? '#fff' : '#94a3b8', fontSize: '11px', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '5px' }}
                >
                  <BookOpen style={{ height: '13px', width: '13px' }} />
                  <span>Papers ({papers.length})</span>
                </button>
                <button 
                  onClick={() => setLiveArtifact('logs')} 
                  style={{ padding: '5px 10px', borderRadius: '6px', border: 'none', backgroundColor: liveArtifact === 'logs' ? '#7c3aed' : 'transparent', color: liveArtifact === 'logs' ? '#fff' : '#94a3b8', fontSize: '11px', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '5px' }}
                >
                  <Terminal style={{ height: '13px', width: '13px' }} />
                  <span>GPU Logs</span>
                </button>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                {liveArtifact === 'workspace' && (
                  <div style={{ display: 'flex', gap: '4px' }}>
                    <button 
                      onClick={() => { setIsCreatingFolder(false); setShowCreateModal(true); }}
                      title="New File"
                      style={{ background: '#121520', border: '1px solid rgba(255,255,255,0.08)', color: '#60a5fa', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '11px', padding: '5px 8px', borderRadius: '6px', fontWeight: '600' }}
                    >
                      <Plus style={{ height: '12px', width: '12px' }} />
                      <span>File</span>
                    </button>
                    <button 
                      onClick={() => { setIsCreatingFolder(true); setShowCreateModal(true); }}
                      title="New Folder"
                      style={{ background: '#121520', border: '1px solid rgba(255,255,255,0.08)', color: '#a78bfa', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '11px', padding: '5px 8px', borderRadius: '6px', fontWeight: '600' }}
                    >
                      <FolderPlus style={{ height: '12px', width: '12px' }} />
                      <span>Folder</span>
                    </button>
                  </div>
                )}

                <button onClick={fetchWorkspaceAndLiterature} title="Sync latest artifacts" style={{ background: '#121520', border: '1px solid rgba(255,255,255,0.06)', color: '#94a3b8', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '11px', padding: '5px 8px', borderRadius: '6px' }}>
                  <RefreshCw style={{ height: '12px', width: '12px', animation: isRefreshing ? 'spin 1s linear infinite' : 'none' }} />
                </button>
              </div>
            </div>
          )}

          {/* Modal: Create File / Folder */}
          {showCreateModal && (
            <div style={{ padding: '12px 16px', backgroundColor: '#131624', borderBottom: '1px solid rgba(124,58,237,0.3)', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ fontSize: '11px', fontWeight: '600', color: '#c4b5fd', whiteSpace: 'nowrap' }}>
                {isCreatingFolder ? "New Folder Name:" : "New File Name:"}
              </span>
              <form onSubmit={handleCreateItem} style={{ flex: 1, display: 'flex', gap: '8px' }}>
                <input 
                  type="text" 
                  autoFocus
                  value={newItemName}
                  onChange={(e) => setNewItemName(e.target.value)}
                  placeholder={isCreatingFolder ? "e.g. data or models" : "e.g. train.py or notes.md"}
                  style={{ flex: 1, padding: '5px 10px', borderRadius: '6px', backgroundColor: '#090b12', border: '1px solid rgba(255,255,255,0.1)', color: '#fff', fontSize: '11px', outline: 'none' }}
                />
                <button type="submit" style={{ padding: '5px 12px', borderRadius: '6px', backgroundColor: '#7c3aed', color: '#fff', border: 'none', fontSize: '11px', fontWeight: '600', cursor: 'pointer' }}>
                  Create
                </button>
                <button type="button" onClick={() => setShowCreateModal(false)} style={{ padding: '5px 10px', borderRadius: '6px', backgroundColor: 'transparent', color: '#94a3b8', border: '1px solid rgba(255,255,255,0.1)', fontSize: '11px', cursor: 'pointer' }}>
                  Cancel
                </button>
              </form>
            </div>
          )}

          {/* VIEW 1: Full-Screen Dedicated File Viewer / Live Editor (With Save & Back Button) */}
          {activeFile && (
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden', backgroundColor: '#07080c' }}>
              <div style={{ height: '44px', borderBottom: '1px solid rgba(255,255,255,0.06)', backgroundColor: '#0c0e18', padding: '0 16px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <button 
                  onClick={closeFileViewer}
                  style={{ background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.1)', color: '#f1f5f9', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px', fontSize: '11px', fontWeight: '600', padding: '5px 10px', borderRadius: '6px' }}
                >
                  <ArrowLeft style={{ height: '13px', width: '13px' }} />
                  <span>Back to Workspace</span>
                </button>

                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ fontSize: '11px', fontFamily: 'monospace', color: '#cbd5e1', fontWeight: '600' }}>
                    {activeFile}
                  </span>

                  {!fileData.is_image && (
                    <>
                      <button 
                        onClick={handleSaveFile} 
                        style={{ background: '#161928', border: '1px solid rgba(124,58,237,0.4)', color: isSaved ? '#34d399' : '#c4b5fd', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '10px', padding: '4px 8px', borderRadius: '4px', fontWeight: '600' }}
                      >
                        {isSaved ? <Check style={{ height: '11px', width: '11px' }} /> : <Save style={{ height: '11px', width: '11px' }} />}
                        <span>{isSaved ? 'Saved' : 'Save'}</span>
                      </button>

                      <button 
                        onClick={copyCode} 
                        style={{ background: '#181b28', border: '1px solid rgba(255,255,255,0.08)', color: copied ? '#34d399' : '#94a3b8', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '10px', padding: '4px 8px', borderRadius: '4px' }}
                      >
                        {copied ? <Check style={{ height: '11px', width: '11px' }} /> : <Copy style={{ height: '11px', width: '11px' }} />}
                        <span>{copied ? 'Copied' : 'Copy'}</span>
                      </button>
                    </>
                  )}
                </div>
              </div>

              <div style={{ flex: 1, padding: '16px', overflowY: 'auto' }}>
                {fileData.is_image ? (
                  <div style={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '24px', backgroundColor: '#090b12', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.04)' }}>
                    <img 
                      src={fileData.content} 
                      alt={activeFile} 
                      style={{ maxWidth: '100%', maxHeight: '420px', borderRadius: '6px', objectFit: 'contain', boxShadow: '0 8px 30px rgba(0,0,0,0.6)' }} 
                    />
                    <span style={{ fontSize: '11px', fontFamily: 'monospace', color: '#34d399', marginTop: '14px' }}>
                      ✓ Generated Publication Figure ({activeFile})
                    </span>
                  </div>
                ) : (
                  <textarea
                    value={fileData.content}
                    onChange={(e) => setFileData({ ...fileData, content: e.target.value })}
                    spellCheck="false"
                    style={{ width: '100%', height: '100%', minHeight: '500px', backgroundColor: 'transparent', border: 'none', outline: 'none', resize: 'none', fontFamily: "'Fira Code', 'JetBrains Mono', monospace", fontSize: '11.5px', color: '#cbd5e1', lineHeight: '1.65' }}
                  />
                )}
              </div>
            </div>
          )}

          {/* VIEW 2: Subagent Hierarchy & Live Task Prompts */}
          {!activeFile && liveArtifact === 'subagents' && (
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden', padding: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
                <div>
                  <h3 style={{ fontSize: '13px', fontWeight: '700', color: '#fff', margin: 0, display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <Layers style={{ height: '15px', width: '15px', color: '#a78bfa' }} />
                    Subagent Delegations & Prompts
                  </h3>
                  <p style={{ fontSize: '11px', color: '#64748b', margin: '2px 0 0 0' }}>Live contract-bounded worker hierarchy & dispatched instructions</p>
                </div>
                <span style={{ fontSize: '11px', fontFamily: 'monospace', padding: '2px 8px', borderRadius: '4px', backgroundColor: 'rgba(124,58,237,0.12)', color: '#c4b5fd', border: '1px solid rgba(124,58,237,0.2)' }}>
                  {subagentTasks.length} Active Workers
                </span>
              </div>

              {subagentTasks.length === 0 ? (
                <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '32px', textAlign: 'center', gap: '12px' }}>
                  <div style={{ height: '48px', width: '48px', borderRadius: '12px', backgroundColor: 'rgba(124,58,237,0.1)', border: '1px solid rgba(124,58,237,0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Bot style={{ height: '22px', width: '22px', color: '#a78bfa' }} />
                  </div>
                  <div>
                    <h4 style={{ fontSize: '13px', fontWeight: '700', color: '#f1f5f9', margin: '0 0 4px 0' }}>Awaiting Subagent Delegation</h4>
                    <p style={{ fontSize: '11px', color: '#64748b', lineHeight: '1.5', margin: 0, maxWidth: '300px' }}>
                      When the parent research manager delegates tasks to <code>eval-worker</code>, <code>plot-worker</code>, <code>write-worker</code>, or <code>rigor-worker</code>, their assigned prompts and live statuses appear here!
                    </p>
                  </div>
                </div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', overflowY: 'auto' }}>
                  {subagentTasks.map((task, idx) => (
                    <div key={idx} style={{ padding: '14px', borderRadius: '10px', backgroundColor: '#10131d', border: '1px solid rgba(255,255,255,0.06)', display: 'flex', flexDirection: 'column', gap: '10px' }}>
                      
                      {/* Subagent Title Header */}
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <Bot style={{ height: '15px', width: '15px', color: '#a78bfa' }} />
                          <span style={{ fontSize: '12px', fontFamily: 'monospace', fontWeight: '700', color: '#fff' }}>
                            {task.worker_name}
                          </span>
                          <span style={{ fontSize: '10px', color: '#64748b' }}>({task.role})</span>
                        </div>

                        <span style={{ fontSize: '9px', fontFamily: 'monospace', padding: '2px 6px', borderRadius: '4px', backgroundColor: task.status === 'COMPLETED' ? '#065f4625' : '#7c3aed20', color: task.status === 'COMPLETED' ? '#34d399' : '#c4b5fd', border: `1px solid ${task.status === 'COMPLETED' ? '#05966940' : '#7c3aed40'}`, fontWeight: '700' }}>
                          {task.status}
                        </span>
                      </div>

                      {/* Prompt Dispatched By Parent */}
                      <div>
                        <div style={{ fontSize: '10px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.04em', color: '#94a3b8', marginBottom: '4px' }}>
                          Parent Prompt & Contract:
                        </div>
                        <pre style={{ margin: 0, padding: '8px 10px', borderRadius: '6px', backgroundColor: '#080a10', border: '1px solid rgba(255,255,255,0.04)', fontSize: '11px', fontFamily: "'Fira Code', monospace", color: '#cbd5e1', lineHeight: '1.5', whiteSpace: 'pre-wrap', maxHeight: '140px', overflowY: 'auto' }}>
                          {task.task_prompt}
                        </pre>
                      </div>

                      {/* Output Summary */}
                      {task.result_summary && (
                        <div style={{ fontSize: '11px', color: '#94a3b8', borderTop: '1px solid rgba(255,255,255,0.04)', paddingTop: '6px', display: 'flex', justifyContent: 'space-between' }}>
                          <span>Result: {task.result_summary}</span>
                          <span style={{ fontSize: '10px', fontFamily: 'monospace', color: '#64748b' }}>{task.updated_at || task.timestamp}</span>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* VIEW 3: Full Workspace Directory List */}
          {!activeFile && liveArtifact === 'workspace' && (
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden', padding: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
                <div>
                  <h3 style={{ fontSize: '13px', fontWeight: '700', color: '#fff', margin: 0 }}>Workspace Directory</h3>
                  <p style={{ fontSize: '11px', color: '#64748b', margin: '2px 0 0 0' }}>Manage, create, edit, rename, and delete files</p>
                </div>
                <span style={{ fontSize: '11px', fontFamily: 'monospace', padding: '2px 8px', borderRadius: '4px', backgroundColor: 'rgba(124,58,237,0.12)', color: '#c4b5fd', border: '1px solid rgba(124,58,237,0.2)' }}>
                  {workspaceFiles.length} Items
                </span>
              </div>

              {workspaceFiles.length === 0 ? (
                <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '32px', textAlign: 'center', gap: '12px' }}>
                  <div style={{ height: '48px', width: '48px', borderRadius: '12px', backgroundColor: 'rgba(124,58,237,0.1)', border: '1px solid rgba(124,58,237,0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Inbox style={{ height: '22px', width: '22px', color: '#a78bfa' }} />
                  </div>
                  <div>
                    <h4 style={{ fontSize: '13px', fontWeight: '700', color: '#f1f5f9', margin: '0 0 4px 0' }}>Workspace is empty</h4>
                    <p style={{ fontSize: '11px', color: '#64748b', lineHeight: '1.5', margin: 0, maxWidth: '280px' }}>
                      Click <b>+ File</b> or <b>+ Folder</b> above to create items, or let your research agent populate it!
                    </p>
                  </div>
                </div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', overflowY: 'auto' }}>
                  {workspaceFiles.map((file, idx) => {
                    const badge = getBadgeStyle(file);
                    const isRenaming = renamingPath === file.path;

                    return (
                      <div 
                        key={idx}
                        onClick={() => !isRenaming && openFileViewer(file.path)}
                        style={{ 
                          padding: '10px 14px', 
                          borderRadius: '8px', 
                          backgroundColor: '#10131d', 
                          border: '1px solid rgba(255,255,255,0.06)', 
                          display: 'flex', 
                          alignItems: 'center', 
                          justifyContent: 'space-between', 
                          cursor: file.is_dir ? 'default' : 'pointer'
                        }}
                      >
                        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flex: 1, minWidth: 0 }}>
                          {getFileIcon(file)}
                          
                          {isRenaming ? (
                            <form onSubmit={(e) => handleRenameItem(e, file.path)} onClick={(e) => e.stopPropagation()} style={{ display: 'flex', gap: '6px', flex: 1 }}>
                              <input 
                                type="text"
                                autoFocus
                                value={renameValue}
                                onChange={(e) => setRenameValue(e.target.value)}
                                style={{ flex: 1, padding: '3px 8px', borderRadius: '4px', backgroundColor: '#090b12', border: '1px solid #7c3aed', color: '#fff', fontSize: '11px', outline: 'none' }}
                              />
                              <button type="submit" style={{ padding: '3px 8px', borderRadius: '4px', backgroundColor: '#7c3aed', color: '#fff', border: 'none', fontSize: '10px', cursor: 'pointer' }}>OK</button>
                              <button type="button" onClick={(e) => { e.stopPropagation(); setRenamingPath(null); }} style={{ padding: '3px 6px', borderRadius: '4px', background: 'none', color: '#94a3b8', border: '1px solid rgba(255,255,255,0.1)', fontSize: '10px', cursor: 'pointer' }}>✕</button>
                            </form>
                          ) : (
                            <div style={{ minWidth: 0 }}>
                              <div style={{ fontSize: '12px', fontFamily: 'monospace', fontWeight: '600', color: '#f1f5f9', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                                {file.path}
                              </div>
                              <div style={{ fontSize: '10px', color: '#64748b', marginTop: '2px' }}>
                                {file.size}
                              </div>
                            </div>
                          )}
                        </div>

                        {!isRenaming && (
                          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginLeft: '12px' }}>
                            <span style={{ fontSize: '9px', fontFamily: 'monospace', padding: '2px 6px', borderRadius: '4px', backgroundColor: badge.bg, color: badge.color, border: `1px solid ${badge.color}30`, fontWeight: '700' }}>
                              {badge.label}
                            </span>

                            <button 
                              onClick={(e) => {
                                e.stopPropagation();
                                setRenamingPath(file.path);
                                setRenameValue(file.name);
                              }}
                              title="Rename"
                              style={{ background: 'none', border: 'none', color: '#64748b', cursor: 'pointer', padding: '4px', borderRadius: '4px', display: 'flex', alignItems: 'center' }}
                            >
                              <Edit2 style={{ height: '12px', width: '12px' }} />
                            </button>

                            <button 
                              onClick={(e) => handleDeleteItem(e, file.path)}
                              title="Delete"
                              style={{ background: 'none', border: 'none', color: '#ef4444', cursor: 'pointer', padding: '4px', borderRadius: '4px', display: 'flex', alignItems: 'center' }}
                            >
                              <Trash2 style={{ height: '12px', width: '12px' }} />
                            </button>

                            {!file.is_dir && <ChevronRight style={{ height: '14px', width: '14px', color: '#475569' }} />}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          )}

          {/* VIEW 4: Researched Literature Feed */}
          {!activeFile && liveArtifact === 'literature' && (
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden', padding: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
                <div>
                  <h3 style={{ fontSize: '13px', fontWeight: '700', color: '#fff', margin: 0 }}>Literature & Citations</h3>
                  <p style={{ fontSize: '11px', color: '#64748b', margin: '2px 0 0 0' }}>Papers discovered via arXiv & Semantic Scholar</p>
                </div>
                <span style={{ fontSize: '11px', fontFamily: 'monospace', padding: '2px 8px', borderRadius: '4px', backgroundColor: 'rgba(251,191,36,0.12)', color: '#fbbf24', border: '1px solid rgba(251,191,36,0.2)' }}>
                  {papers.length} Papers
                </span>
              </div>

              <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {papers.map((paper, idx) => (
                  <div key={idx} style={{ padding: '14px 16px', borderRadius: '10px', backgroundColor: '#10131d', border: '1px solid rgba(255,255,255,0.06)', display: 'flex', flexDirection: 'column', gap: '10px' }}>
                    <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '12px' }}>
                      <h4 style={{ fontSize: '13px', fontWeight: '700', color: '#f8fafc', lineHeight: '1.4', margin: 0 }}>
                        {paper.title}
                      </h4>
                      <span style={{ fontSize: '9px', fontFamily: 'monospace', padding: '2px 6px', borderRadius: '4px', backgroundColor: 'rgba(251,191,36,0.12)', color: '#fbbf24', border: '1px solid rgba(251,191,36,0.25)', whiteSpace: 'nowrap', fontWeight: '600' }}>
                        {paper.source}
                      </span>
                    </div>

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

                    {paper.summary && (
                      <p style={{ fontSize: '11.5px', color: '#cbd5e1', lineHeight: '1.6', margin: 0, backgroundColor: '#090b12', padding: '10px 12px', borderRadius: '6px', border: '1px solid rgba(255,255,255,0.03)' }}>
                        {paper.summary}
                      </p>
                    )}

                    {paper.url && (
                      <div style={{ display: 'flex', justifyContent: 'flex-end', paddingTop: '2px' }}>
                        <a href={paper.url} target="_blank" rel="noreferrer" style={{ fontSize: '11px', fontWeight: '600', color: '#a78bfa', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '5px', padding: '4px 8px', borderRadius: '4px', backgroundColor: 'rgba(124,58,237,0.1)' }}>
                          <span>Read Manuscript / PDF</span>
                          <ExternalLink style={{ height: '11px', width: '11px' }} />
                        </a>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* VIEW 5: Kaggle GPU Telemetry Logs */}
          {!activeFile && liveArtifact === 'logs' && (
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
