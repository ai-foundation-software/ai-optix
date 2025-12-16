# Model Efficiency Benchmark Suite (MEBS) Guide

MEBS is the standard benchmarking infrastructure for `ai_optix`. It ensures that all performance numbers we report are:
1.  **Correct**: Handling GPU synchronization and timer resolution automatically.
2.  **Reproducible**: Enforcing warmup cycles and statistical aggregation.
3.  **Hardware-Aware**: Automatically detecting CUDA, MPS, or CPU environments.

## 🚀 Quick Start

### Using the `@benchmark` Decorator

The easiest way to measure a function is to decorate it.

```python
from ai_optix.mebs import benchmark

@benchmark("My Operation", warmup=10, measure=100)
def my_op():
    # Your code here
    # If using GPU, PyTorch ops are automatically synchronized by MEBS
    torch.matmul(a, b)

# Running the function triggers the benchmark and returns stats
stats = my_op() 
print(f"Mean Latency: {stats.mean_ms:.4f} ms")
```

### Manual Runner API

For more control (e.g., changing config dynamically), use `LatencyRunner`.

```python
from ai_optix.mebs import BenchmarkConfig, LatencyRunner

def my_op():
    pass

config = BenchmarkConfig(
    name="Dynamic Bench",
    warmup_iters=5,
    measure_iters=20,
    device="cuda" # Force a specific device
)

runner = LatencyRunner(config)
stats = runner.run(my_op)
```

## 📊 Understanding Requirements

When contributing to `ai_optix`, you **MUST** use MEBS for any performance claims.

### Why not `time.time()`?
Standard Python timers do not account for:
-   **Asynchronous GPU Execution**: GPU kernels return control to Python immediately. `time.time()` measures launch time, not execution time. MEBS uses `torch.cuda.Event` for correct timing.
-   **Cold Start**: The first few iterations of any ML op include allocator overhead, kernel compilation, or cache warming. MEBS enforces warmup.
-   **OS Noise**: A single run can be affected by context switches. MEBS reports P50/P99 to show stability.

## 🛠 Advanced Usage

### Throughput Benchmarking
For extremely fast operations (nanoseconds), per-iteration timing overhead is too high. Use `ThroughputRunner` to measure a batch.

```python
from ai_optix.mebs.runners.throughput import ThroughputRunner, ThroughputConfig

config = ThroughputConfig("Tiny Op", measure_iters=10000)
runner = ThroughputRunner(config)
stats = runner.run(tiny_op)
print(f"Throughput: {stats.throughput_per_sec:.2f} ops/sec")
```
