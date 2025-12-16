use pyo3::prelude::*;
use std::sync::{Arc, Mutex};
use sysinfo::{CpuRefreshKind, RefreshKind, System};

#[pyclass]
pub struct SystemProfiler {
    sys: Arc<Mutex<System>>,
}

#[pymethods]
impl SystemProfiler {
    #[new]
    fn new() -> Self {
        let sys =
            System::new_with_specifics(RefreshKind::new().with_cpu(CpuRefreshKind::everything()));
        SystemProfiler {
            sys: Arc::new(Mutex::new(sys)),
        }
    }

    fn snapshot(&self) -> (f32, u64) {
        let mut sys = self.sys.lock().unwrap();
        sys.refresh_cpu();

        let cpu_usage = sys.global_cpu_info().cpu_usage();
        let memory_used = sys.used_memory();

        (cpu_usage, memory_used)
    }
}
