#!/usr/bin/env bash
# ==============================================================================
# ForgeResearcher 🔬⚡ — 1-Command Automated Setup & Launcher
# ==============================================================================
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=================================================================="
echo "🔬 Welcome to ForgeResearcher Studio (Best UI & Guided Autonomy)"
echo "=================================================================="

# Step 1: Ensure uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 [1/7] Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Step 2: Set up virtual environment
if [ ! -d ".venv" ]; then
    echo "⚙️  [2/7] Setting up Python virtual environment with uv..."
    uv venv .venv
    source .venv/bin/activate
    uv pip install pytest fastmcp uvicorn starlette fastapi pydantic pandas matplotlib scikit-learn numpy kaggle huggingface_hub datasets
else
    source .venv/bin/activate
fi

# Step 3: Install & Build Studio UI Frontend Dependencies
echo "🎨 [3/7] Setting up ForgeResearcher Studio UI Frontend..."
cd "$DIR/frontend"
if [ ! -d "node_modules" ]; then
    echo "  📦 Installing frontend dependencies (npm install)..."
    npm install --silent
fi
echo "  ⚡ Building production bundle (npm run build)..."
npm run build --silent || true
cd "$DIR"

# Step 4: Check for Kaggle Credentials
echo "🔑 [4/7] Checking Kaggle Authentication..."
if [ -f "$HOME/.kaggle/kaggle.json" ] || [ -n "$KAGGLE_KEY" ]; then
    echo "  ✓ Kaggle credentials found (Cloud GPU acceleration active)."
else
    echo "  ℹ️  Optional: To enable Kaggle Cloud GPU execution, set up your Kaggle API key:"
    echo "     1. Go to https://www.kaggle.com/settings -> Click 'Create New Token'"
    echo "     2. Place kaggle.json in ~/.kaggle/kaggle.json (or run: export KAGGLE_KEY=...)"
fi

# Step 5: Ensure TrueForge is running
echo "🌐 [5/7] Checking TrueForge runtime on port 8790..."
if ! curl -s http://localhost:8790/api/v1/settings/mcp-servers > /dev/null 2>&1; then
    echo "  🚀 Starting TrueForge runtime (npx @truefoundry/trueforge)..."
    nohup npx @truefoundry/trueforge > /tmp/trueforge.log 2>&1 &
    
    echo "  ⏳ Waiting for TrueForge server to become ready..."
    for i in {1..30}; do
        if curl -s http://localhost:8790/api/v1/settings/mcp-servers > /dev/null 2>&1; then
            echo "  ✓ TrueForge is live at http://localhost:8790!"
            break
        fi
        sleep 1
    done
else
    echo "  ✓ TrueForge is already running on http://localhost:8790."
fi

# Step 6: Start FastMCP Gateway
echo "⚡ [6/7] Starting FastMCP Research Tool Gateway on port 8795..."
fuser -k 8795/tcp > /dev/null 2>&1 || true
sleep 1
nohup "$DIR/.venv/bin/python" "$DIR/run_mcp_gateway.py" > /tmp/mcp_gateway.log 2>&1 &
MCP_PID=$!
sleep 2

# Register Agent & MCP Servers in TrueForge
"$DIR/.venv/bin/python" "$DIR/register_with_trueforge.py"

# Step 7: Start Telemetry API & Launch Studio UI
echo "🚀 [7/7] Starting Telemetry API & Launching Studio UI..."
fuser -k 8796/tcp > /dev/null 2>&1 || true
nohup "$DIR/.venv/bin/python" "$DIR/mcp_servers/workspace_api/server.py" > /tmp/workspace_api.log 2>&1 &

fuser -k 5173/tcp > /dev/null 2>&1 || true
cd "$DIR/frontend"
nohup "$DIR/frontend/node_modules/.bin/vite" --port 5173 --host 0.0.0.0 > /tmp/frontend_dev.log 2>&1 &
cd "$DIR"

echo ""
echo "=================================================================="
echo "🎉 FORGERESEARCHER STUDIO IS FULLY LIVE & OPERATIONAL!"
echo "=================================================================="
echo "👉 🌟 Modern Custom Research Studio UI: http://localhost:5173"
echo "👉 ⚡ TrueForge Core Engine:             http://localhost:8790"
echo "=================================================================="
