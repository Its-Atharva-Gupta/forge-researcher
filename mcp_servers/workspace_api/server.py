"""
Workspace Explorer, Skills Manager, TrueForge Chat Bridge & Telemetry API
Provides clean REST endpoints to create sessions with 'forge-researcher', send prompts, and stream responses.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
import json
import base64
import urllib.request
import urllib.parse
import uvicorn
from typing import Optional, List, Dict, Any
from kaggle.api.kaggle_api_extended import KaggleApi

app = FastAPI(title="ForgeResearcher Studio & Chat API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

WORKSPACE_DIR = os.path.abspath("workspace")
SKILLS_DIR = os.path.abspath("skills")
os.makedirs(WORKSPACE_DIR, exist_ok=True)
os.makedirs(SKILLS_DIR, exist_ok=True)

CACHE_FILE = "/tmp/kaggle_telemetry/latest_run.json"
LITERATURE_FILE = "/tmp/forge_literature/papers.json"
SUBAGENT_FILE = "/tmp/forge_telemetry/subagents.json"
TRUEFORGE_API = "http://localhost:8790/api/v1"

class ChatMessagePayload(BaseModel):
    message: str
    session_id: Optional[str] = None

class CreateItemPayload(BaseModel):
    name: str
    is_folder: bool = False
    parent_path: Optional[str] = ""
    content: Optional[str] = ""

class RenameItemPayload(BaseModel):
    old_path: str
    new_name: str

class DeleteItemPayload(BaseModel):
    path: str

class SaveFilePayload(BaseModel):
    path: str
    content: str

# -------------------------------------------------------------
# 💬 TRUEFORGE NATIVE CHAT BRIDGE (forge-researcher default agent)
# -------------------------------------------------------------
def get_forge_researcher_agent_id() -> str:
    """Fetches the exact agent ID for 'forge-researcher'."""
    try:
        req = urllib.request.Request(f"{TRUEFORGE_API}/agents")
        with urllib.request.urlopen(req, timeout=5) as res:
            data = json.loads(res.read().decode("utf-8"))
            for agent in data.get("data", []):
                if agent.get("name") == "forge-researcher":
                    return agent.get("id")
    except Exception:
        pass
    return "01m1465yeb27dqye87eph35mev"

@app.get("/api/chat/session")
def get_or_create_session():
    """Gets the latest forge-researcher session or creates a new one."""
    agent_id = get_forge_researcher_agent_id()
    try:
        req = urllib.request.Request(f"{TRUEFORGE_API}/sessions")
        with urllib.request.urlopen(req, timeout=5) as res:
            data = json.loads(res.read().decode("utf-8"))
            for sess in data.get("data", []):
                if sess.get("agent", {}).get("name") == "forge-researcher" or sess.get("agent", {}).get("id") == agent_id:
                    return {"session_id": sess.get("id"), "agent_name": "forge-researcher"}
    except Exception:
        pass

    # Create new session
    try:
        create_payload = json.dumps({
            "agent": {
                "type": "reference",
                "id": agent_id,
                "name": "forge-researcher"
            },
            "title": "ForgeResearcher Autonomous Lab"
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{TRUEFORGE_API}/sessions",
            data=create_payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as res:
            new_sess = json.loads(res.read().decode("utf-8"))
            return {"session_id": new_sess.get("id"), "agent_name": "forge-researcher"}
    except Exception as e:
        return {"session_id": "default-session", "agent_name": "forge-researcher", "error": str(e)}

@app.get("/api/chat/messages")
def get_session_messages(session_id: str):
    """Fetches messages and tool executions for a given session."""
    try:
        req = urllib.request.Request(f"{TRUEFORGE_API}/sessions/{session_id}/messages")
        with urllib.request.urlopen(req, timeout=5) as res:
            data = json.loads(res.read().decode("utf-8"))
            return {"messages": data.get("data", [])}
    except Exception as e:
        return {"messages": [], "error": str(e)}

@app.post("/api/chat/send")
def send_chat_message(payload: ChatMessagePayload):
    """Sends a user prompt to the TrueForge agent engine."""
    session_id = payload.session_id
    if not session_id or session_id == "default-session":
        sess_info = get_or_create_session()
        session_id = sess_info.get("session_id")

    try:
        body = json.dumps({
            "role": "user",
            "content": payload.message
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{TRUEFORGE_API}/sessions/{session_id}/messages",
            data=body,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=30) as res:
            data = json.loads(res.read().decode("utf-8"))
            return {"success": True, "session_id": session_id, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------------------------------------------
# 🎯 SKILLS MANAGER API
# -------------------------------------------------------------
@app.get("/api/skills/list")
def list_skills():
    skills = []
    if not os.path.exists(SKILLS_DIR):
        return {"skills": []}

    for item in sorted(os.listdir(SKILLS_DIR)):
        skill_path = os.path.join(SKILLS_DIR, item)
        if os.path.isdir(skill_path):
            doc_file = os.path.join(skill_path, "SKILL.md")
            if not os.path.exists(doc_file):
                for root, _, files in os.walk(skill_path):
                    if "SKILL.md" in files:
                        doc_file = os.path.join(root, "SKILL.md")
                        break

            desc = "Autonomous research capability skill definition"
            if os.path.exists(doc_file):
                try:
                    with open(doc_file, "r") as f:
                        for l in f:
                            if l.lower().startswith("description:"):
                                desc = l.split(":", 1)[1].strip().strip('"').strip("'")
                                break
                except Exception:
                    pass
            
            rel_doc_path = os.path.relpath(doc_file, start=".") if os.path.exists(doc_file) else f"skills/{item}/SKILL.md"
            skills.append({
                "name": item,
                "path": rel_doc_path,
                "dir_path": f"skills/{item}",
                "description": desc,
                "has_skill_md": os.path.exists(doc_file)
            })
    return {"skills": skills, "total": len(skills)}

@app.get("/api/skills/read")
def read_skill_file(path: str):
    safe_path = os.path.abspath(path)
    if not safe_path.startswith(SKILLS_DIR):
        raise HTTPException(status_code=400, detail="Path outside skills directory")
    
    if not os.path.exists(safe_path):
        os.makedirs(os.path.dirname(safe_path), exist_ok=True)
        default_content = f"---\nname: {os.path.basename(os.path.dirname(safe_path))}\ndescription: Autonomous capability skill definition.\n---\n\n# Skill Instructions\n\nDefine specialized protocols and prompts here.\n"
        with open(safe_path, "w") as f:
            f.write(default_content)
        return {"path": path, "content": default_content}
    
    try:
        with open(safe_path, "r", errors="ignore") as f:
            return {"path": path, "content": f.read()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/skills/save")
def save_skill_file(payload: SaveFilePayload):
    safe_path = os.path.abspath(payload.path)
    if not safe_path.startswith(SKILLS_DIR):
        raise HTTPException(status_code=400, detail="Cannot save outside skills/ directory")
    
    try:
        os.makedirs(os.path.dirname(safe_path), exist_ok=True)
        with open(safe_path, "w") as f:
            f.write(payload.content)
        return {"success": True, "path": payload.path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------------------------------------------
# 🤖 SUBAGENTS & TELEMETRY
# -------------------------------------------------------------
@app.get("/api/subagents/tasks")
def list_subagent_tasks():
    if os.path.exists(SUBAGENT_FILE):
        try:
            with open(SUBAGENT_FILE, "r") as f:
                tasks = json.load(f)
            return {"tasks": tasks, "total": len(tasks)}
        except Exception:
            pass
    return {"tasks": [], "total": 0}

# -------------------------------------------------------------
# 📁 WORKSPACE CRUD API
# -------------------------------------------------------------
@app.get("/api/workspace/files")
def list_workspace_files():
    if not os.path.exists(WORKSPACE_DIR):
        return {"files": [], "total": 0}
    
    file_list = []
    for root, dirs, files in os.walk(WORKSPACE_DIR):
        for d in dirs:
            full_path = os.path.join(root, d)
            rel_path = os.path.relpath(full_path, start=".")
            file_list.append({
                "path": rel_path,
                "name": d,
                "is_dir": True,
                "size": "Folder",
                "is_image": False,
                "modified": os.path.getmtime(full_path)
            })
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, start=".")
            size_kb = round(os.path.getsize(full_path) / 1024, 2)
            is_image = f.lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif'))
            file_list.append({
                "path": rel_path,
                "name": f,
                "is_dir": False,
                "size": f"{size_kb} KB",
                "is_image": is_image,
                "modified": os.path.getmtime(full_path)
            })
            
    file_list.sort(key=lambda x: (not x.get("is_dir", False), x["name"].lower()))
    return {"files": file_list, "total": len(file_list)}

@app.get("/api/workspace/file")
def read_workspace_file(path: str):
    safe_path = os.path.abspath(path)
    if not os.path.exists(safe_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    if os.path.isdir(safe_path):
        return {"path": path, "is_dir": True, "content": "Directory"}
    
    is_image = path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
    if is_image:
        try:
            with open(safe_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
                mime = "image/png" if path.endswith(".png") else "image/jpeg"
                return {
                    "path": path,
                    "is_image": True,
                    "content": f"data:{mime};base64,{encoded}"
                }
        except Exception as e:
            return {"error": str(e)}
    
    try:
        with open(safe_path, "r", errors="ignore") as f:
            return {"path": path, "is_image": False, "content": f.read()}
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/workspace/create")
def create_workspace_item(payload: CreateItemPayload):
    target_dir = os.path.join(WORKSPACE_DIR, payload.parent_path) if payload.parent_path else WORKSPACE_DIR
    target_path = os.path.join(target_dir, payload.name)
    try:
        if payload.is_folder:
            os.makedirs(target_path, exist_ok=True)
            return {"success": True, "path": os.path.relpath(target_path, start=".")}
        else:
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with open(target_path, "w") as f:
                f.write(payload.content or "")
            return {"success": True, "path": os.path.relpath(target_path, start=".")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/workspace/save")
def save_workspace_file(payload: SaveFilePayload):
    safe_path = os.path.abspath(payload.path)
    try:
        with open(safe_path, "w") as f:
            f.write(payload.content)
        return {"success": True, "path": payload.path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/workspace/rename")
def rename_workspace_item(payload: RenameItemPayload):
    old_full = os.path.abspath(payload.old_path)
    if not os.path.exists(old_full):
        raise HTTPException(status_code=404, detail="Item not found")
    new_full = os.path.join(os.path.dirname(old_full), payload.new_name)
    try:
        os.rename(old_full, new_full)
        return {"success": True, "new_path": os.path.relpath(new_full, start=".")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/workspace/delete")
def delete_workspace_item(payload: DeleteItemPayload):
    target_path = os.path.abspath(payload.path)
    if not os.path.exists(target_path):
        raise HTTPException(status_code=404, detail="Item not found")
    try:
        if os.path.isdir(target_path):
            shutil.rmtree(target_path)
        else:
            os.remove(target_path)
        return {"success": True, "deleted": payload.path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------------------------------------------
# 📖 LITERATURE & KAGGLE LOGS API
# -------------------------------------------------------------
@app.get("/api/literature/papers")
def list_researched_papers():
    if os.path.exists(LITERATURE_FILE):
        try:
            with open(LITERATURE_FILE, "r") as f:
                papers = json.load(f)
            return {"papers": papers, "total": len(papers)}
        except Exception:
            pass
    return {"papers": [], "total": 0}

@app.get("/api/kaggle/latest-logs")
def get_latest_kaggle_logs():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                data = json.load(f)
            return data
        except Exception:
            pass

    try:
        api = KaggleApi()
        api.authenticate()
        username = api.get_config_value("username")
        kernels = api.kernels_list(mine=True, page_size=1)
        if not kernels:
            return {"active": False, "message": "No Kaggle experiments dispatched yet."}
        
        latest = kernels[0]
        slug = f"{username}/{latest.ref.split('/')[-1]}"
        status = api.kernels_status(slug)
        output = api.kernels_output(slug)
        return {
            "active": True,
            "kernel_slug": slug,
            "status": status.get("status"),
            "log": output.get("log", "Waiting for output logs...")
        }
    except Exception:
        return {"active": False, "message": "Awaiting first GPU experiment dispatch."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8796)
