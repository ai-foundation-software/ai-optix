import pytest
from ai_optix.api.optimizer import AIModelOptimizer
from ai_optix.api.profiler import Profiler

def test_optimizer_flow():
    opt = AIModelOptimizer("test-opt")
    # Small data
    res = opt.optimize([1.0, 2.0, 3.0, 4.0], 2, 2)
    assert res.optimized is True
    assert res.device.startswith("cpu")
    
    # Suggestion
    assert opt.suggest_backend(100) == "cpu"
    assert opt.suggest_backend(10**9) == "gpu"

def test_profiler_flow():
    prof = Profiler()
    snap = prof.snapshot()
    assert "cpu_usage_percent" in snap
    assert "memory_used_bytes" in snap
