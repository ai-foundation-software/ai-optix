import psutil
import os
from typing import Dict

class CpuProfiler:
    def snapshot(self) -> Dict[str, float]:
        process = psutil.Process(os.getpid())
        return {
            "cpu_percent": psutil.cpu_percent(interval=None),
            "ram_used_mb": process.memory_info().rss / 1024 / 1024,
            "ram_percent": process.memory_percent()
        }
