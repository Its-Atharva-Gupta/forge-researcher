"""
Workspace Explorer, Literature Feed & Telemetry API for ForgeResearcher Studio UI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import base64
import uvicorn
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
CACHE_FILE = "/tmp/kaggle_telemetry/latest_run.json"
LITERATURE_FILE = "/tmp/forge_literature/papers.json"

@app.get("/api/literature/papers")
def list_researched_papers():
    """Lists papers and citations discovered and read by the agent via arXiv & Semantic Scholar."""
    if os.path.exists(LITERATURE_FILE):
        try:
            with open(LITERATURE_FILE, "r") as f:
                papers = json.load(f)
            return {"papers": papers, "total": len(papers)}
        except Exception:
            pass
    return {"papers": [], "total": 0}

@app.get("/api/workspace/files")
def list_workspace_files():
    """Lists real files currently present in workspace/."""
    if not os.path.exists(WORKSPACE_DIR):
        return {"files": [], "total": 0}
    
    file_list = []
    for root, _, files in os.walk(WORKSPACE_DIR):
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, start=".")
            size_kb = round(os.path.getsize(full_path) / 1024, 2)
            is_image = f.lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif'))
            file_list.append({
                "path": rel_path,
                "name": f,
                "size": f"{size_kb} KB",
                "is_image": is_image,
                "modified": os.path.getmtime(full_path)
            })
    return {"files": file_list, "total": len(file_list)}

@app.get("/api/workspace/file")
def read_workspace_file(path: str):
    """Reads content of a specific file or returns image Base64 data."""
    safe_path = os.path.abspath(path)
    if not os.path.exists(safe_path):
        return {"error": "File not found"}
    
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

@app.get("/api/kaggle/latest-logs")
def get_latest_kaggle_logs():
    """Fetches real status of the latest Kaggle experiment if run."""
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
