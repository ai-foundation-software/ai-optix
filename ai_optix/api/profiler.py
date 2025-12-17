# SPDX-FileCopyrightText: 2025 ai-foundation-software
# SPDX-License-Identifier: Apache-2.0

from .._core import SystemProfiler as RustProfiler

class Profiler:
    """ High-level wrapper for SystemProfiler. """
    def __init__(self):
        self._inner = RustProfiler()

    def snapshot(self) -> dict:
        """ Returns a snapshot of system metrics. """
        cpu, mem = self._inner.snapshot()
        return {
            "cpu_usage_percent": cpu,
            "memory_used_bytes": mem
        }
