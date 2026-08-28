"""
Subagent Delegation & Prompt Telemetry Logger
Tracks parent agent delegations, task prompts, worker status, and results.
"""
from typing import Dict, Any, List, Optional
import os
import json
import time
from fastmcp import FastMCP

mcp = FastMCP("SubagentTelemetryGateway")

CACHE_DIR = "/tmp/forge_telemetry"
os.makedirs(CACHE_DIR, exist_ok=True)
SUBAGENT_LOG_FILE = os.path.join(CACHE_DIR, "subagents.json")

def record_subagent_delegation(
    worker_name: str,
    role: str,
    task_prompt: str,
    status: str = "RUNNING",
    result_summary: Optional[str] = None
) -> Dict[str, Any]:
    """Records a task delegated to a subagent with its explicit prompt and status."""
    existing = []
    if os.path.exists(SUBAGENT_LOG_FILE):
        try:
            with open(SUBAGENT_LOG_FILE, "r") as f:
                existing = json.load(f)
        except Exception:
            existing = []

    updated = False
    for item in existing:
        if item.get("worker_name") == worker_name and item.get("status") == "RUNNING":
            item["status"] = status
            if result_summary:
                item["result_summary"] = result_summary
            item["updated_at"] = time.strftime("%X")
            updated = True
            break
    
    if not updated:
        existing.insert(0, {
            "id": f"task-{int(time.time() * 1000)}",
            "worker_name": worker_name,
            "role": role,
            "task_prompt": task_prompt,
            "status": status,
            "result_summary": result_summary or "Worker executing assigned bounded contract...",
            "timestamp": time.strftime("%X"),
            "updated_at": time.strftime("%X")
        })

    with open(SUBAGENT_LOG_FILE, "w") as f:
        json.dump(existing[:20], f, indent=2)

    return {"success": True, "worker_name": worker_name, "status": status}

def delegate_subagent_task(
    target_worker: str,
    role_description: str,
    explicit_prompt: str,
    expected_output_contract: str
) -> Dict[str, Any]:
    """Delegates a contract-bounded research sub-task to a specialized worker (eval-worker, plot-worker, write-worker, rigor-worker)."""
    record_subagent_delegation(
        worker_name=target_worker,
        role=role_description,
        task_prompt=f"PROMPT:\n{explicit_prompt}\n\nCONTRACT:\n{expected_output_contract}",
        status="RUNNING"
    )
    return {
        "success": True,
        "worker_name": target_worker,
        "status": "DISPATCHED",
        "message": f"Subagent '{target_worker}' successfully launched with contract instructions."
    }

def complete_subagent_task(
    target_worker: str,
    execution_summary: str
) -> Dict[str, Any]:
    """Reports completion of a subagent task back to the parent research manager."""
    record_subagent_delegation(
        worker_name=target_worker,
        role="Specialized Subagent",
        task_prompt="Completed assigned contract.",
        status="COMPLETED",
        result_summary=execution_summary
    )
    return {"success": True, "worker_name": target_worker, "status": "COMPLETED"}

if __name__ == "__main__":
    mcp.tool()(delegate_subagent_task)
    mcp.tool()(complete_subagent_task)
    mcp.run()
