#!/usr/bin/env bash
set -e

echo "[1/6] Checking Homebrew..."
if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew not found. Install from https://brew.sh first."
  exit 1
fi

echo "[2/6] Installing Python 3.11 and git..."
brew install python@3.11 git

echo "[3/6] Creating virtual environment..."
python3.11 -m venv .venv
source .venv/bin/activate

echo "[4/6] Upgrading pip..."
pip install --upgrade pip

echo "[5/6] Installing Python dependencies..."
pip install -r requirements.txt

echo "[6/6] Preparing env file..."
if [ ! -f .env ]; then
  cp .env.example .env
fi

echo "Done. Next:"
echo "1) Open .env and fill in DEEPSEEK_API_KEY"
echo "2) Run: source .venv/bin/activate"
echo "3) Run: python src/main.py --goal '为交易页写 PRD 和技术方案'"
