# Installation Guide

This guide covers the setup process for **AI Optix** on Linux, macOS, and Windows.

## System Requirements

- **Python**: 3.9 or higher
- **Rust Toolchain**: Stable (1.70+)
- **C++ Compiler**: GCC 9+, Clang 10+, or MSVC 2019+
- **Builder**: `maturin` (installed via pip)

## Prerequisites

### 1. Install Rust
We recommend using `rustup`:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### 2. Install Build Tools
**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install build-essential cmake
```

**macOS:**
```bash
xcode-select --install
brew install cmake
```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/ai-optix.git
cd ai-optix
```

### 2. Create Virtual Environment
It is critical to rely on a virtual environment to avoid conflicts.
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install maturin patchelf
pip install -r requirements.txt  # If available, or minimal deps:
pip install torch numpy
```

### 4. Build and Install
Compile the Rust/C++ extensions and install the package in editable mode:
```bash
maturin develop --release
```
*Note: The `--release` flag enables high-performance optimizations. Omit it for faster incremental builds during debugging.*

## GPU Support

AI Optix attempts to auto-detect CUDA or MPS.
- **NVIDIA GPU**: Ensure `nvcc` is in your PATH.
- **Apple Silicon**: No extra steps required (uses `MPS` backend in PyTorch).

## Troubleshooting

### "Missing Python.h"
Ensure you have python development headers installed:
```bash
sudo apt install python3-dev
```

### "Linker errors"
Cleaning the build artifacts often resolves linking issues after dependency updates:
```bash
cargo clean --manifest-path src/rust/Cargo.toml
```

### "ModuleNotFoundError: ai_optix._core"
This means the binary extension was not built.
- Run `maturin develop`.
- Ensure you are in the virtual environment.
