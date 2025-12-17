# SPDX-FileCopyrightText: 2025 ai-foundation-software
# SPDX-License-Identifier: Apache-2.0

try:
    from ._core import Optimizer, SystemProfiler, OptimizationResult
    __all__ = ["Optimizer", "SystemProfiler", "OptimizationResult"]
except ImportError:
    # Allow package to be imported even if extension isn't built yet
    # This is critical for running python-only benchmarks/tests in dev environment
    pass
