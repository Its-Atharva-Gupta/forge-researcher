"""
Official Kaggle Remote GPU/TPU Execution & Cloud Compute MCP Server
"""
from typing import Dict, Any, List, Optional
import os
import json
import tempfile
import multiprocessing
import time
from fastmcp import FastMCP
from kaggle.api.kaggle_api_extended import KaggleApi

mcp = FastMCP("KaggleCloudComputeServer")

# Ensure telemetry cache dir exists
CACHE_DIR = "/tmp/kaggle_telemetry"
os.makedirs(CACHE_DIR, exist_ok=True)
LATEST_LOG_FILE = os.path.join(CACHE_DIR, "latest_run.json")

def get_kaggle_api():
    api = KaggleApi()
    try:
        api.authenticate()
        return api
    except Exception:
        return None

def run_experiment_on_kaggle_gpu(
    experiment_title: str,
    code_content: str,
    enable_gpu: bool = True,
    enable_tpu: bool = False,
    dataset_sources: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Pushes and executes an ML training script directly on Kaggle's cloud GPUs (NVIDIA T4 x2 / P100) or TPUs."""
    api = get_kaggle_api()
    if not api:
        return {"error": "Kaggle credentials not configured. Please set KAGGLE_USERNAME and KAGGLE_KEY."}

    kernel_slug = experiment_title.lower().strip().replace(" ", "-").replace("_", "-")
    username = api.get_config_value("username") or os.environ.get("KAGGLE_USERNAME", "kaggle-user")
    full_slug = f"{username}/{kernel_slug}"

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            script_path = os.path.join(tmpdir, "main.py")
            with open(script_path, "w") as f:
                f.write(code_content)

            meta = {
                "id": full_slug,
                "title": experiment_title,
                "code_file": "main.py",
                "language": "python",
                "kernel_type": "script",
                "is_private": "true",
                "enable_gpu": "true" if enable_gpu else "false",
                "enable_tpu": "true" if enable_tpu else "false",
                "enable_internet": "true",
                "dataset_sources": dataset_sources or []
            }
            with open(os.path.join(tmpdir, "kernel-metadata.json"), "w") as f:
                json.dump(meta, f)

            res = api.kernels_push(tmpdir)
            
            # Save also to workspace/ so user sees it in workspace explorer
            os.makedirs("workspace", exist_ok=True)
            workspace_code_file = f"workspace/{kernel_slug}.py"
            with open(workspace_code_file, "w") as wf:
                wf.write(code_content)

            # Write immediate telemetry state
            telemetry_data = {
                "active": True,
                "title": experiment_title,
                "kernel_slug": full_slug,
                "kernel_url": f"https://www.kaggle.com/code/{full_slug}",
                "code": code_content,
                "hardware": "NVIDIA T4 Dual GPU" if enable_gpu else ("Google TPU v3-8" if enable_tpu else "CPU"),
                "status": "QUEUED_AND_RUNNING",
                "log": f"Dispatched kernel '{full_slug}' to Kaggle Cloud GPU at {time.strftime('%X')}.\nWaiting for kernel container spin-up and output logs...\nURL: https://www.kaggle.com/code/{full_slug}",
                "timestamp": time.time()
            }
            with open(LATEST_LOG_FILE, "w") as tf:
                json.dump(telemetry_data, tf)

            return {
                "success": True,
                "mode": "KAGGLE_REMOTE_CLOUD_GPU",
                "kernel_slug": full_slug,
                "kernel_url": f"https://www.kaggle.com/code/{full_slug}",
                "version_number": res.versionNumber,
                "hardware": "NVIDIA T4 Dual GPU" if enable_gpu else ("Google TPU v3-8" if enable_tpu else "CPU"),
                "status": "QUEUED_AND_RUNNING_ON_KAGGLE",
                "message": f"Successfully dispatched experiment '{experiment_title}' to remote Kaggle GPU compute!"
            }
    except Exception as e:
        return {"error": f"Failed to dispatch to Kaggle GPU: {str(e)}"}

def get_kaggle_experiment_logs(experiment_slug: str) -> Dict[str, Any]:
    """Fetches status and output logs of a running/completed Kaggle GPU experiment."""
    api = get_kaggle_api()
    if not api:
        return {"error": "Kaggle credentials not configured."}
    try:
        status = api.kernels_status(experiment_slug)
        output = api.kernels_output(experiment_slug)
        current_status = status.get("status")
        current_log = output.get("log", "")

        # Update telemetry file
        if os.path.exists(LATEST_LOG_FILE):
            try:
                with open(LATEST_LOG_FILE, "r") as tf:
                    t_data = json.load(tf)
                t_data["status"] = current_status
                if current_log:
                    t_data["log"] = current_log
                with open(LATEST_LOG_FILE, "w") as tf:
                    json.dump(t_data, tf)
            except Exception:
                pass

        return {
            "success": True,
            "experiment_slug": experiment_slug,
            "status": current_status,
            "log": current_log or f"Kernel status: {current_status}",
            "files_produced": [f.get("name") for f in output.get("files", [])]
        }
    except Exception as e:
        return {"error": f"Failed to get Kaggle experiment logs: {str(e)}"}

def search_kaggle_datasets(query: str, max_results: int = 5) -> Dict[str, Any]:
    """Searches Kaggle and open scientific repositories for machine learning datasets."""
    api = get_kaggle_api()
    if api:
        try:
            datasets = api.dataset_list(search=query, page=1)
            results = []
            for d in datasets[:max_results]:
                results.append({
                    "ref": d.ref,
                    "title": d.title,
                    "size": d.size,
                    "voteCount": d.voteCount,
                    "url": f"https://www.kaggle.com/datasets/{d.ref}"
                })
            return {
                "success": True,
                "authenticated": True,
                "count": len(results),
                "datasets": results,
                "source": "official_kaggle_api"
            }
        except Exception:
            pass

    benchmarks = [
        {"ref": "titanic", "title": "Titanic: Machine Learning from Disaster", "url": "https://www.kaggle.com/c/titanic"},
        {"ref": "tabular-playground-series", "title": "Kaggle Tabular Playground Benchmark", "url": "https://www.kaggle.com/competitions/tabular-playground-series"},
        {"ref": "california-housing-prices", "title": "California Housing Prices", "url": "https://www.kaggle.com/datasets/camnugent/california-housing-prices"},
        {"ref": "digit-recognizer", "title": "Digit Recognizer (MNIST Computer Vision)", "url": "https://www.kaggle.com/c/digit-recognizer"}
    ]
    matched = [b for b in benchmarks if query.lower() in b["title"].lower() or query.lower() in b["ref"].lower()]
    return {
        "success": True,
        "authenticated": False,
        "count": len(matched) if matched else len(benchmarks),
        "datasets": matched if matched else benchmarks[:max_results],
        "source": "kaggle_benchmark_catalog"
    }

def inspect_kaggle_and_local_compute() -> Dict[str, Any]:
    """Profiles Kaggle Cloud GPU hardware and local sandbox cores."""
    api = get_kaggle_api()
    return {
        "kaggle_remote_compute": {
            "status": "AUTHENTICATED_AND_ACTIVE" if api else "UNAUTHENTICATED",
            "gpu_hardware": "NVIDIA T4 Dual-GPU (16GB VRAM each) / NVIDIA P100",
            "tpu_hardware": "Google TPU v3-8",
            "weekly_quota": "30 Hours/week free cloud GPU acceleration",
            "tools": ["run_experiment_on_kaggle_gpu", "get_kaggle_experiment_logs"]
        },
        "local_sandbox": {
            "cpu_cores": multiprocessing.cpu_count(),
            "environment": "TrueForge Container Sandbox"
        }
    }

if __name__ == "__main__":
    mcp.tool()(search_kaggle_datasets)
    mcp.tool()(run_experiment_on_kaggle_gpu)
    mcp.tool()(get_kaggle_experiment_logs)
    mcp.tool()(inspect_kaggle_and_local_compute)
    mcp.run()
