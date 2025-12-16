# CPU Execution Logic

This document details how `ai_optix` achieves performance on the CPU, contrasting it with pure Python implementations.

## ⚡ Execution Flow

When a user calls `optimizer.optimize(data)`:

1.  **Python Layer**: Accepts a NumPy array.
2.  **Rust Layer**:
    -   Receives the `PyReadBuffer` or `PyArray`.
    -   **Gil Release**: Immediately releases the Global Interpreter Lock (GIL) to allow parallelism.
    -   **Pointer Extraction**: Obtains the raw memory address (`float*`) and dimensions.
3.  **C++ Layer**:
    -   Function: `mat_mul_cpu` (or similiar).
    -   **OpenMP Dispatch**: Spawns threads based on `OMP_NUM_THREADS`.
    -   **SIMD Execution**: Compiler auto-vectorizes loops (AVX2/AVX-512).

## 🧵 Threading Model

We use **OpenMP** (via C++) rather than Rust's `rayon` for kernel parallelism.
-   **Why?** Legacy stability with mathematical libraries (BLAS/LAPACK) and fine-grained control over thread affinity.
-   **Structure**:
    ```cpp
    #pragma omp parallel for collapse(2)
    for (int i = 0; i < N; ++i) { ... }
    ```
-   **Oversubscription Risk**: Users must be careful not to nest `ai_optix` calls inside `multiprocessing` pools without setting `OMP_NUM_THREADS=1`.

## 🧠 Memory Layout

`ai_optix` relies on **Contiguous Memory**.
-   **Row-Major (C-style)**: We assume `data[i * stride + j]` layout.
-   **Strides**: Currently, we typically enforce `C_CONTIGUOUS` arrays. If a user passes a sliced (non-contiguous) array, Rust should behave in one of two ways (currently implementation dependent):
    1.  *Reject*: Raise `ValueError`. (Preferred for performance)
    2.  *Copy*: Create a contiguous copy. (Easier for users, slower)

## 🏎 Optimization Techniques

### 1. Loop Blocking (Tiling)
(Planned/Partial)
To minimize cache misses, we iterate over small "blocks" of the matrix that fit into L1/L2 cache, rather than scanning full rows/columns.

### 2. No-GIL Execution
Because the heavy lifting happens in C++, the Python main thread is free. This allows `ai_optix` to run in a background thread while the main Python thread handles I/O or GUI tasks.

### 3. Static Linking
We verify at compile time (via CMake) whether to compile AVX-512 or AVX2 paths, ensuring the binary is optimized for the host architecture (when built locally).
