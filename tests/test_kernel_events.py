
import time
import pytest
from ai_optix.api.optimizer import AIModelOptimizer
from ai_optix.api.profiler import Profiler

def test_kernel_events_captured():
    """
    Verify that running a matrix optimization (C++ kernel)
    generates 'kernel_start' and 'kernel_end' events in the Rust profiler.
    """
    # 1. Setup Profiler (starts Rust session)
    # We use the lower-level Session directly or the API wrapper if it supports start/stop control
    # API wrapper's snapshot() is one-shot. We need manual control.
    # So we access the inner RustProfiler from the API wrapper or use _core directly.
    
    from ai_optix._core import ProfilerSession
    session = ProfilerSession()
    session.start()
    
    # 2. Run C++ Workload (Optimizer)
    # This calls mat_mul_cpu in C++, which triggers the callback to Rust
    opt = AIModelOptimizer("test-kernel-tracer")
    # Size 100x100 is enough to be > 0ms but fast
    data = [1.0] * (100 * 100) 
    opt.optimize(data, 100, 100)
    
    # Allow small buffer time for things to settle (channel is fast though)
    time.sleep(0.05)
    
    # 3. Stop and Poll
    session.stop()
    events = session.poll()
    
    # 4. Verify Events
    # We expect kernel_start (kind="kernel_start") and kernel_end
    kernel_starts = [e for e in events if e[1] == "kernel_start"]
    kernel_ends = [e for e in events if e[1] == "kernel_end"]
    
    assert len(kernel_starts) > 0, "No C++ kernel start events captured!"
    assert len(kernel_ends) > 0, "No C++ kernel end events captured!"
    assert len(kernel_starts) == len(kernel_ends), "Mismatch in start/end events"
    
    # Verify timestamp ordering
    for start, end in zip(kernel_starts, kernel_ends):
        # start time <= end time
        assert start[0] <= end[0], "Kernel end timestamp came before start!"

if __name__ == "__main__":
    test_kernel_events_captured()
