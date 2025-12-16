# Performance Notes & Limitations

An honest assessment of the current performance characteristics of `ai_optix`.

## 🛑 Known Bottlenecks

### 1. The Python Call Overhead
Even with Rust, every call from Python incurs a small overhead (argument parsing, type checking, pointer extraction).
-   **Impact**: Operations taking < 5 microseconds are dominated by Python overhead.
-   **Mitigation**: "Fuse" operations. Instead of calling `add()` then `mul()`, call a single `fused_add_mul()` kernel to pay the call tax once.

### 2. Thread Oversubscription
If you run `ai_optix` (which uses OpenMP) inside a `multiprocessing` pool or a web server (Gunicorn/Uvicorn) with multiple workers:
-   **Scenario**: 8 Workers x 8 OpenMP Threads = 64 Threads.
-   **Result**: Context switching thrashing. Performance typically degrades by 10-50%.
-   **Fix**: Set `OMP_NUM_THREADS=1` if running in a multi-process environment.

### 3. Non-Contiguous Memory
Passing a sliced array (e.g., `data[:, ::2]`) forces a memory copy in the Rust layer before C++ can touch it.
-   **Cost**: `malloc` + `memcpy` proportional to data size.
-   **Detection**: Profiling shows valid time spent in `pyarray.to_vec()` or similar fallback logic.

## 🔍 Profiling Tips

Do not use `time.time()` for micro-benchmarks. Use our built-in profiler or `cProfile`.

### CPU Cache Locality
Our C++ kernels currently use a simple nested loop (naive implementation).
```cpp
// Current Naive Implementation
for (i...) for (j...) for (k...)
```
This causes inefficient L1/L2 cache usage for large matrices.
**TODO**: Implement Blocked Matrix Multiplication (Tiling) to improve cache hit rates.

## 📉 Hardware Specifics

-   **Apple Silicon (M1/M2/M3)**: 
    -   Excellent SIMD (NEON) performance.
    -   OpenMP support can be tricky with the default Clang; verify `libomp` is linked.
-   **Intel/AMD w/ AVX-512**:
    -   Highest theoretical CPU throughput, but may cause "frequency scaling" (downclocking) on older Intel chips.
