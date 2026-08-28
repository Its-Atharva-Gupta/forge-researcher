#!/usr/bin/env bash
# ForgeResearcher 1-Command Startup
# Starts the FastMCP HTTP Gateway in background and registers the agent with TrueForge

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Ensure venv exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment via uv..."
    uv venv .venv
    source .venv/bin/activate
    uv pip install -r <(echo "pytest mcp uvicorn starlette pandas matplotlib scikit-learn numpy")
else
    source .venv/bin/activate
fi

echo "Starting FastMCP Gateway on port 8795..."
PYTHONPATH=. .venv/bin/python launch_mcp_streamable_gateway.py > /tmp/mcp_gateway.log 2>&1 &
MCP_PID=$!

sleep 2

echo "Registering tools and agent in TrueForge..."
.venv/bin/python register_with_trueforge.py

echo ""
echo "🚀 Everything is running!"
echo "MCP Gateway PID: $MCP_PID (logs in /tmp/mcp_gateway.log)"
echo "Go to http://localhost:8790 to see the agent 'forge-researcher' in action!"
