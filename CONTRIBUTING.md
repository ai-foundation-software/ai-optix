# Contributing to AI Optix

Thank you for your interest in improving AI Optix! We are a research-focused project that values code quality, collaboration, and technical rigor.

## Code Style & Standards

### Python
- We follow **PEP 8**.
- Use type hints (`typing` module) for all public APIs.
- Formatter: `black`
- Linter: `ruff` or `flake8`

### Rust
- Follow standard Rust idioms.
- Formatter: `cargo fmt`
- Linter: `cargo clippy`

### C++
- Standard: C++17
- Formatting: Google Style (approx. `clang-format -style=Google`)

## Development Workflow

1. **Fork & Branch**: Create a feature branch from `main`.
   ```bash
   git checkout -b feature/my-optimization
   ```
2. **Implement**: Write your code.
3. **Test**:
   - Run Python tests: `pytest`
   - Run Rust tests: `cargo test --manifest-path src/rust/Cargo.toml`
4. **Docs**: Update docstrings and markdown files if needed.
5. **PR**: Open a Pull Request.

## Commit Messages
We use conventional commits:
- `feat: ...` for new capabilities.
- `fix: ...` for bug fixes.
- `docs: ...` for documentation updates.
- `perf: ...` for performance improvements.

*Example*: `feat(profiler): add L2 cache miss tracking on Linux`

## Adding a New Optimization Kernel

1. **Implement C++ Kernel**: Add source in `src/cpp/`.
2. **Expose via Rust**: Add FFI binding in `src/rust/src/optimizer.rs`.
3. **Update Python API**: Ensure `ai_optix.Optimizer` exposes the method.
4. **Benchmark**: Add a case in `ai_optix/benchmarks/mebs/` to prove the speedup.

## License
By contributing, you agree that your code will be licensed under the project's MIT License.
