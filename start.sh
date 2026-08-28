#!/usr/bin/env bash
# ==============================================================================
# ForgeResearcher 🔬⚡ — 1-Command Automated Setup & Launcher
# ==============================================================================
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=================================================================="
echo "🔬 Welcome to ForgeResearcher (TrueForge Research Agent Harness)"
echo "=================================================================="

# Step 1: Ensure uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Step 2: Set up virtual environment
if [ ! -d ".venv" ]; then
    echo "⚙️  [1/4] Setting up Python virtual environment with uv..."
    uv venv .venv
    source .venv/bin/activate
    uv pip install pytest fastmcp uvicorn starlette pandas matplotlib scikit-learn numpy kaggle huggingface_hub datasets
else
    source .venv/bin/activate
fi

# Step 3: Check for Kaggle Credentials
echo "🔑 [2/4] Checking Kaggle Authentication..."
if [ -f "$HOME/.kaggle/kaggle.json" ] || [ -n "$KAGGLE_KEY" ]; then
    echo "  ✓ Kaggle credentials found (Cloud GPU acceleration active)."
else
    echo "  ℹ️  Optional: To enable Kaggle Cloud GPU execution, set up your Kaggle API key:"
    echo "     1. Go to https://www.kaggle.com/settings -> Click 'Create New Token'"
    echo "     2. Place kaggle.json in ~/.kaggle/kaggle.json (or run: export KAGGLE_KEY=...)"
    echo "     (Proceeding with local container sandbox mode for now...)"
fi

# Step 4: Ensure TrueForge is running
echo "🌐 [3/4] Checking TrueForge runtime on port 8790..."
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

# Step 5: Start FastMCP Gateway
echo "⚡ [4/4] Starting FastMCP Research Tool Gateway on port 8795..."
fuser -k 8795/tcp > /dev/null 2>&1 || true
sleep 1
nohup "$DIR/.venv/bin/python" "$DIR/run_mcp_gateway.py" > /tmp/mcp_gateway.log 2>&1 &
MCP_PID=$!
sleep 2

# Step 6: Auto-register Agent and Tools
"$DIR/.venv/bin/python" "$DIR/register_with_trueforge.py"

echo ""
echo "=================================================================="
echo "🚀 FORGERESEARCHER IS RUNNING AND READY!"
echo "👉 Open your browser to: http://localhost:8790"
echo "👉 Select 'forge-researcher' and start your research inquiry!"
echo "=================================================================="
