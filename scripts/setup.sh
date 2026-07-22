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

uv upgrade
uv install --upgrade setuptools wheel
uv install -r requirements-base.txt
MODE="$1"
if [ "$MODE" = "cpu" ] || [ "$MODE" = "gpu" ]; then
  echo "Install mode override: $MODE"
fi

# Determine mode: explicit arg, otherwise auto-detect
if [ -z "$MODE" ]; then
  if command -v nvidia-smi &>/dev/null; then
    MODE="gpu"
  else
    MODE="cpu"
  fi
fi

if [ "$MODE" = "gpu" ]; then
  echo "✅ NVIDIA GPU path selected → installing CUDA extras"
  if command -v apt-get &>/dev/null; then
    echo "Attempting to install system CUDA toolkit via apt-get (optional)"
    sudo apt-get update && sudo apt-get install -y nvidia-cuda-toolkit || \
      echo "Warning: failed to install nvidia-cuda-toolkit via apt-get; continuing"
  fi
  # Prefer installing package extras which include CUDA-specific deps.
  uv install -e ".[cuda]" || uv install -r requirements-cuda.txt
  echo "Installed CUDA extras (or fell back to requirements-cuda.txt)"
else
  echo "ℹ️ CPU-only path selected → installing CPU PyTorch"
  uv install -r requirements-cpu.txt
  # Install editable package for CPU mode
  uv install -e .
fi

echo "Setup complete. Activate the venv with: source .venv/bin/activate"
