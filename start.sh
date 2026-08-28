#!/usr/bin/env bash
# ==============================================================================
# ForgeResearcher 🔬⚡ — 1-Command Automated Setup & Guided Wizard
# ==============================================================================
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=================================================================="
echo "🔬 Welcome to ForgeResearcher Studio (Best UI & Guided Autonomy)"
echo "=================================================================="

# ------------------------------------------------------------------------------
# STEP 1: Ensure uv Package Manager
# ------------------------------------------------------------------------------
if ! command -v uv &> /dev/null; then
    echo "📦 [1/8] Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# ------------------------------------------------------------------------------
# STEP 2: Python Environment Setup
# ------------------------------------------------------------------------------
if [ ! -d ".venv" ]; then
    echo "⚙️  [2/8] Setting up Python virtual environment with uv..."
    uv venv .venv
    source .venv/bin/activate
    uv pip install pytest fastmcp uvicorn starlette fastapi pydantic pandas matplotlib scikit-learn numpy kaggle huggingface_hub datasets
else
    source .venv/bin/activate
fi

# ------------------------------------------------------------------------------
# STEP 3: Frontend Studio UI Dependencies & Build
# ------------------------------------------------------------------------------
echo "🎨 [3/8] Setting up ForgeResearcher Studio UI Frontend..."
cd "$DIR/frontend"
if [ ! -d "node_modules" ]; then
    echo "  📦 Installing frontend dependencies (npm install)..."
    npm install --silent
fi
echo "  ⚡ Building production bundle (npm run build)..."
npm run build --silent || true
cd "$DIR"

# ------------------------------------------------------------------------------
# STEP 4: Interactive Auth & Configuration Guide (Model Providers, Daytona, Kaggle)
# ------------------------------------------------------------------------------
echo ""
echo "=================================================================="
echo "🔑 [4/8] ENVIRONMENT & AUTHENTICATION CHECK"
echo "=================================================================="

# 1. Model Provider Check (OpenAI / Anthropic / DeepSeek / Ollama / OpenRouter)
if [ -n "$OPENAI_API_KEY" ] || [ -n "$ANTHROPIC_API_KEY" ] || [ -n "$DEEPSEEK_API_KEY" ] || [ -n "$OPENROUTER_API_KEY" ]; then
    echo "  ✓ Model Provider API Key detected."
else
    echo "  ⚠️  MODEL PROVIDER SETUP:"
    echo "     TrueForge requires an LLM provider to power the agent."
    echo "     Export your key in your terminal or .env:"
    echo "       • export DEEPSEEK_API_KEY=\"your_key\""
    echo "       • export OPENAI_API_KEY=\"your_key\""
    echo "       • export ANTHROPIC_API_KEY=\"your_key\""
    echo "       • Or configure providers inside TrueForge UI: http://localhost:8790/settings"
fi

# 2. Daytona Cloud Sandbox Workspace Check (Optional/Recommended for TrueForge)
if [ -n "$DAYTONA_API_KEY" ] || [ -n "$DAYTONA_SERVER_URL" ] || command -v daytona &> /dev/null; then
    echo "  ✓ Daytona workspace runtime detected (Isolated Cloud Sandbox active)."
else
    echo "  ℹ️  DAYTONA CLOUD WORKSPACE (Optional):"
    echo "     For isolated cloud sandbox environments in TrueForge:"
    echo "     1. Sign up at https://daytona.io and generate an API key."
    echo "     2. Run: export DAYTONA_API_KEY=\"your_daytona_key\""
    echo "     (Local TrueForge container sandbox will be used as fallback)"
fi

# 3. Kaggle Cloud GPU Authentication Check
if [ -f "$HOME/.kaggle/kaggle.json" ] || [ -n "$KAGGLE_KEY" ]; then
    echo "  ✓ Kaggle credentials found (Cloud GPU acceleration active)."
else
    echo "  ℹ️  KAGGLE CLOUD GPU SETUP (Dual-T4 / Tesla P100):"
    echo "     To enable free Kaggle Cloud GPU execution:"
    echo "     1. Go to https://www.kaggle.com/settings -> Click 'Create New Token'"
    echo "     2. Place the downloaded 'kaggle.json' in ~/.kaggle/kaggle.json"
    echo "        (or run: export KAGGLE_USERNAME=... and export KAGGLE_KEY=...)"
    echo "        (or run: chmod 600 ~/.kaggle/kaggle.json)"
fi
echo "=================================================================="
echo ""

# ------------------------------------------------------------------------------
# STEP 5: TrueForge Engine Runtime Launch
# ------------------------------------------------------------------------------
echo "🌐 [5/8] Checking TrueForge runtime on port 8790..."
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

# ------------------------------------------------------------------------------
# STEP 6: FastMCP Gateway Launch
# ------------------------------------------------------------------------------
echo "⚡ [6/8] Starting FastMCP Research Tool Gateway on port 8795..."
fuser -k 8795/tcp > /dev/null 2>&1 || true
sleep 1
nohup "$DIR/.venv/bin/python" "$DIR/run_mcp_gateway.py" > /tmp/mcp_gateway.log 2>&1 &
MCP_PID=$!
sleep 2

# ------------------------------------------------------------------------------
# STEP 7: Register Agent & MCP Servers in TrueForge
# ------------------------------------------------------------------------------
echo "🤖 [7/8] Registering 'forge-researcher' with TrueForge..."
"$DIR/.venv/bin/python" "$DIR/register_with_trueforge.py"

# ------------------------------------------------------------------------------
# STEP 8: Start Telemetry API & Launch Studio UI
# ------------------------------------------------------------------------------
echo "🚀 [8/8] Starting Telemetry API & Launching Studio UI..."
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
