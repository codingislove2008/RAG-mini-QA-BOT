#!/usr/bin/env bash
set -e

# Change directory to script folder
cd "$(dirname "$0")"

echo "==================================================="
echo "            NimbusNote RAG Mini Bot"
echo "==================================================="
echo ""

# 1. Check for virtual environment and create if missing
if [ ! -f ".venv/bin/python" ]; then
    echo "[INFO] Virtual environment not found. Creating .venv..."
    python3 -m venv .venv 2>/dev/null || python -m venv .venv
    echo "[INFO] Installing required dependencies..."
    ./.venv/bin/pip install -r requirements.txt
fi

# 2. Choose Mode
echo "Select how you want to run the bot:"
echo "[1] Streamlit Web UI (Default / Browser)"
echo "[2] Terminal CLI (Console Chat)"
echo ""
read -p "Enter choice (1/2, default 1): " choice

choice=${choice:-1}

if [ "$choice" = "2" ]; then
    echo ""
    echo "==================================================="
    echo "Starting Terminal CLI..."
    echo "==================================================="
    ./.venv/bin/python cli.py
else
    echo ""
    echo "==================================================="
    echo "Starting Streamlit Web UI..."
    echo "==================================================="
    ./.venv/bin/streamlit run app.py
fi
