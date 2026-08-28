"""
Workspace Explorer, File Manager, Literature Feed & Telemetry API for ForgeResearcher Studio UI
Supports Full CRUD: List, Create File/Folder, Rename, Delete, Edit/Save, and Base64 Images.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
import json
import base64
import uvicorn
from typing import Optional
from kaggle.api.kaggle_api_extended import KaggleApi

app = FastAPI(title="ForgeResearcher Workspace & Literature API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

WORKSPACE_DIR = os.path.abspath("workspace")
os.makedirs(WORKSPACE_DIR, exist_ok=True)
CACHE_FILE = "/tmp/kaggle_telemetry/latest_run.json"
LITERATURE_FILE = "/tmp/forge_literature/papers.json"

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

@app.get("/api/workspace/files")
def list_workspace_files():
    """Lists all files and directories in workspace/."""
    if not os.path.exists(WORKSPACE_DIR):
        return {"files": [], "total": 0}
    
    file_list = []
    for root, dirs, files in os.walk(WORKSPACE_DIR):
        # Include directories
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
        
        # Include files
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
            
    # Sort folders first, then files alphabetically
    file_list.sort(key=lambda x: (not x.get("is_dir", False), x["name"].lower()))
    return {"files": file_list, "total": len(file_list)}

@app.get("/api/workspace/file")
def read_workspace_file(path: str):
    """Reads content of a file or returns Base64 image data."""
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
    """Creates a new file or folder in workspace/."""
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
    """Saves edits to a file in workspace/."""
    safe_path = os.path.abspath(payload.path)
    try:
        with open(safe_path, "w") as f:
            f.write(payload.content)
        return {"success": True, "path": payload.path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/workspace/rename")
def rename_workspace_item(payload: RenameItemPayload):
    """Renames a file or folder in workspace/."""
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
    """Deletes a file or directory in workspace/."""
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

@app.get("/api/literature/papers")
def list_researched_papers():
    """Lists papers and citations discovered via arXiv & Semantic Scholar."""
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
    """Fetches real status of the latest Kaggle experiment."""
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
