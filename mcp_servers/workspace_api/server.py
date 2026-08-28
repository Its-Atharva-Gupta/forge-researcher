"""
Workspace Explorer & Telemetry API for ForgeResearcher Studio UI
Serves real-time files and Kaggle execution logs from the active workspace directory.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import uvicorn
from kaggle.api.kaggle_api_extended import KaggleApi

app = FastAPI(title="ForgeResearcher Workspace API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

WORKSPACE_DIR = os.path.abspath("workspace")

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
            file_list.append({
                "path": rel_path,
                "name": f,
                "size": f"{size_kb} KB",
                "modified": os.path.getmtime(full_path)
            })
    return {"files": file_list, "total": len(file_list)}

@app.get("/api/workspace/file")
def read_workspace_file(path: str):
    """Reads content of a specific file in workspace/."""
    safe_path = os.path.abspath(path)
    if not safe_path.startswith(WORKSPACE_DIR) or not os.path.exists(safe_path):
        return {"error": "File not found or outside workspace"}
    
    try:
        with open(safe_path, "r", errors="ignore") as f:
            return {"path": path, "content": f.read()}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/kaggle/latest-logs")
def get_latest_kaggle_logs():
    """Fetches real status of the latest Kaggle experiment if run."""
    try:
        api = KaggleApi()
        api.authenticate()
        username = api.get_config_value("username")
        # List latest kernels
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
    except Exception as e:
        return {"active": False, "message": "Awaiting first GPU experiment dispatch."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8796)
