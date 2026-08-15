// SPDX-FileCopyrightText: 2025 ai-foundation-software
// SPDX-License-Identifier: Apache-2.0

use numpy::PyReadonlyArrayDyn;
use pyo3::prelude::*;
use rayon::prelude::*;
use serde::{Deserialize, Serialize};

#[pyclass]
#[derive(Debug, Serialize, Deserialize)]
pub struct OptimizationResult {
    #[pyo3(get)]
    pub execution_time_ms: f64,
    #[pyo3(get)]
    pub optimized: bool,
    #[pyo3(get)]
    pub device: String,
}

#[pyclass]
pub struct Optimizer {
    name: String,
}

const fn fnv1a_hash(bytes: &[u8]) -> u64 {
    let mut hash = 14695981039346656037u64;
    let mut i = 0;
    while i < bytes.len() {
        hash ^= bytes[i] as u64;
        hash = hash.wrapping_mul(1099511628211u64);
        i += 1;
    }
    hash
}

const KERNEL_ID: u64 = fnv1a_hash(b"mat_mul_cpu");

#[pymethods]
impl Optimizer {
    #[new]
    pub fn new(name: String) -> Self {
        Optimizer { name }
    }

    /// Optimizes matrix (MatMul simulation via parallelized Rust kernel)
    /// Accepts a 2D numpy array (flattened or not) and treats it as Square Matrix of side `rows`
    /// Current demo assumes input `data` is A, and we multiply A * A for demo purposes.
    pub fn optimize_matrix(
        &self,
        _py: Python,
        rows: usize,
        cols: usize,
        data: PyReadonlyArrayDyn<f32>,
    ) -> PyResult<OptimizationResult> {
        let start = std::time::Instant::now();

        let a_slice = data.as_slice()?;
        let len = a_slice.len();

        if len != rows * cols {
            return Err(pyo3::exceptions::PyValueError::new_err(format!(
                "Data size {} does not match rows*cols {}",
                len,
                rows * cols
            )));
        }

        // Trace start event
        let grid_size = (rows * cols) as u64;
        let block_size = 1u64;
        let payload = (block_size << 32) | (grid_size & 0xFFFFFFFF);
        crate::profiler::ffi::ai_optix_trace_callback(KERNEL_ID, payload, 0);

        // Allocate result buffer and compute matrix multiplication using Rayon
        let mut _c = vec![0.0f32; rows * cols];
        _c.par_chunks_exact_mut(cols)
            .enumerate()
            .for_each(|(i, c_row)| {
                let a_row = &a_slice[i * cols..(i + 1) * cols];
                for j in 0..cols {
                    let mut sum = 0.0f32;
                    for k in 0..cols {
                        sum += a_row[k] * a_slice[k * cols + j];
                    }
                    c_row[j] = sum;
                }
            });

        // Trace end event
        crate::profiler::ffi::ai_optix_trace_callback(KERNEL_ID, payload, 1);

        let duration = start.elapsed();

        Ok(OptimizationResult {
            execution_time_ms: duration.as_secs_f64() * 1000.0,
            optimized: true,
            device: "cpu (rust_kernel)".to_string(),
        })
    }

    /// Suggests best backend based on data size
    pub fn suggest_backend(&self, size_bytes: u64) -> String {
        if size_bytes > 1024 * 1024 * 100 {
            // 100 MB
            "gpu".to_string()
        } else {
            "cpu".to_string()
        }
    }

    pub fn __repr__(&self) -> String {
        format!("<Optimizer name='{}'>", self.name)
    }
}
