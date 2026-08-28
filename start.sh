#!/usr/bin/env bash
# ForgeResearcher 1-Command Startup
# Starts the FastMCP HTTP Gateway persistently and registers the agent with TrueForge

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Ensure venv exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment via uv..."
    uv venv .venv
    source .venv/bin/activate
    uv pip install pytest fastmcp uvicorn starlette pandas matplotlib scikit-learn numpy kaggle huggingface_hub datasets
else
    source .venv/bin/activate
fi

echo "Ensuring FastMCP Gateway is running on port 8795..."
fuser -k 8795/tcp || true
sleep 1
nohup "$DIR/.venv/bin/python" "$DIR/run_mcp_gateway.py" > /tmp/mcp_gateway.log 2>&1 &
MCP_PID=$!

sleep 3

echo "Registering tools and agent in TrueForge..."
"$DIR/.venv/bin/python" "$DIR/register_with_trueforge.py"

echo ""
echo "🚀 Everything is running!"
echo "MCP Gateway PID: $MCP_PID (logs in /tmp/mcp_gateway.log)"
echo "Go to http://localhost:8790 to see the agent 'forge-researcher' in action!"
