# AI Optix Architecture

This document outlines the high-level architecture of `ai_optix`, a hybrid Python/Rust/C++ library designed for high-performance AI optimization on CPU.

## 🏗 High-Level Overview

`ai_optix` follows a "sandwich" architecture similar to modern high-performance libraries (like `polars` or `pydantic-core`), but with a dedicated C++ kernel layer for raw computational throughput.

```mermaid
graph TD
    User[User Python Script] --> API[ai_optix (Python)]
    API --> Rust[Rust Extension (_core)]
    
    subgraph "Native Execution Layer"
        Rust --> |FFI / Unsafe| Cpp[C++ Kernels]
        Cpp --> |OpenMP| CPU[CPU Cores]
        Cpp --> |CUDA (Optional)| GPU[NVIDIA GPU]
    end

    subgraph "Memory Management"
        Rust -- Borrow --> PyMem[Python Memory (NumPy)]
        Cpp -- Pointer --> PyMem
    end
```

## 📂 Directory Structure & Responsibilities

| Path | Responsibility | Language |
|------|---------------|----------|
| `ai_optix/` | **Public API Surface**. Pure Python. Handles type validation, high-level orchestration, and user-facing errors. | Python |
| `src/rust/` | **System Glue & Safety**. Handles Python C-API interaction (via PyO3), memory safety, concurrent data loading, and orchestration of C++ kernels. | Rust |
| `src/cpp/` | **Computational Core**. Raw bare-metal loops, OpenMP parallelization, and SIMD intrinsics. No Python awareness here. | C++ |
| `cmake/` | **Build Logic**. Configuration for compiling C++ kernels across Linux/macOS/Windows. | CMake |

## 🔌 The Interface Boundary

### Python ↔ Rust (`maturin` + `pyo3`)
We use `maturin` to build the Rust extension. The Rust layer (`src/rust/src/lib.rs`) exposes classes like `Optimizer` directly to Python. 
- **Zero-Copy**: We aim to pass NumPy array pointers directly to Rust/C++ without copying data, using the Buffer Protocol.

### Rust ↔ C++ (`cc` / `cmake`)
Rust links against the static or shared C++ library (`kernels_cpu`).
- **bindgen** (conceptual): Rust defines `extern "C"` blocks to call C++ functions.
- **Safety**: Rust encapsulates the `unsafe` calls to C++, ensuring that pointers are valid and arrays are locked before C++ touches them.

## 🛠 Build System

The build is a hybrid process:
1. **Pip/Build**: Invokes `maturin`.
2. **Maturin**: Compiles the Rust crate.
3. **Rust Build Script (`build.rs`)**: Invokes `cmake`.
4. **CMake**: Compiles `src/cpp/kernels.cpp` into `libkernels_cpu.a`.
5. **Linker**: Statically links C++ kernels into the Rust extension, which is loaded by Python.
