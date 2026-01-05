# Automated Kernel Tuning - Observation Layer

The Observation Layer is the foundation of the Automated Kernel Tuning subsystem in AI-Optix. It provides low-overhead, high-fidelity monitoring of GPU kernel executions, enabling the discovery of optimization opportunities.

## Overview

The Observation Layer operates by injecting lightweight instrumentation points into the C++ kernel execution path. These points emit structured events that are captured, aggregated, and analyzed by the Rust-based profiling core.

### Key Features

- **Kernel ID Hashing**: Stable, unique identifiers for kernels based on their source code and parameters.
- **Structured Event Tracing**: Capture of rich execution metadata including execution time, grid/block dimensions, and dynamic shared memory usage.
- **Low Overhead**: Minimized interference with actual kernel execution through efficient event buffering and asynchronous processing.

## Architecture

The system consists of three main components:

1.  **C++ Instrumentation**: Macros and helper functions in `src/cpp/kernels.cpp` that emit events.
2.  **Rust Core (`ai_optix_rust`)**: A high-performance library that handles event ingestion, aggregation, and metrics calculation.
3.  **Python API**: The user-facing `GpuProfiler` class that exposes aggregated metrics and tuning suggestions.

## Usage

### Python API

```python
from ai_optix.api.profiler import Profiler

# Initialize profiler
prof = Profiler()

# Run your workload
run_my_gpu_workload()

# Get a snapshot of metrics
metrics = prof.snapshot()

# Access kernel-specific stats
for kernel_id, stats in metrics.get("kernels", {}).items():
    print(f"Kernel {kernel_id}: avg_duration={stats['avg_ms']}ms")
```

### Event Structure

Events are defined in `src/rust/src/profiler/events.rs` and include:

- `KernelStart`: Timestamp, Kernel ID.
- `KernelEnd`: Timestamp, Kernel ID.
- `MetricUpdate`: Updates to counters (e.g., cache hits, memory usage).

## Kernel ID Hashing

To track kernels across different runs, we generate a stable hash using the kernel name and its launch configuration. This ensures that even if the order of execution changes, performance data can be correctly attributed to the specific kernel variant.
