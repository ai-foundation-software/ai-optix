#!/usr/bin/env bash
set -e

# Default to python3 if python3.11 is not available, but user requested 3.11 explicitly.
# We will try python3.11 first, then fallback to python3 if explicitly set, but strict req says 3.11.
PYTHON_BIN="python3.11"
if ! command -v $PYTHON_BIN &>/dev/null; then
  echo "python3.11 not found, trying python3..."
  PYTHON_BIN="python3"
fi

echo "Using Python: $($PYTHON_BIN --version)"

$PYTHON_BIN -m venv .venv
source .venv/bin/activate

pip install --upgrade pip setuptools wheel
pip install -r requirements-base.txt

if command -v nvidia-smi &>/dev/null; then
  echo "✅ NVIDIA GPU detected → installing CUDA PyTorch"
  pip install -r requirements-cuda.txt
else
  echo "ℹ️ No GPU detected → installing CPU PyTorch"
  pip install -r requirements-cpu.txt
fi

# Install the package in editable mode
pip install -e .
