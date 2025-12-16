import typer
from rich.console import Console
import time
import sys
from rich.markdown import Markdown

app = typer.Typer(help="ai-optix: AI Performance Profiler")
console = Console()

@app.command()
def profile(
    script: str = typer.Argument(..., help="Path to the python script to profile"),
    duration: int = typer.Option(10, help="Duration to profile in seconds"),
    interval: float = typer.Option(1.0, help="Sampling interval in seconds")
):
    """
    Profile a Python script and report performance metrics.
    """
    console.print(f"[green]Starting profiling for {script}...[/green]")
    
    from ai_optix.optix import AutoOptimizer
    from ai_optix.detector.dataloader import DataLoaderDetector
    from ai_optix.detector.gpu_idle import GpuIdleDetector
    from ai_optix.reports.markdown_report import generate_markdown_report
    
    import runpy
    
    optimizer = AutoOptimizer()
    optimizer.start()
    
    start_time = time.time()
    try:
        # Run user script in-process
        # Clean sys.argv to hide our own arguments
        sys.argv = [script]
        runpy.run_path(script, run_name="__main__")
    except SystemExit:
        pass # Script called sys.exit(), expected behavior
    except KeyboardInterrupt:
        console.print("[yellow]Script stopped by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]Script failed with error: {e}[/red]")
        # We still generate report up to crash
    finally:
        metrics = optimizer.stop()
        end_time = time.time()
        
    # Analysis
    detectors = [DataLoaderDetector(), GpuIdleDetector()]
    issues = []
    for d in detectors:
        issues.extend(d.detect(metrics))
        
    # Summary Props
    summary = {
        "duration": end_time - start_time,
        "avg_cpu": sum(m["cpu_percent"] for m in metrics)/len(metrics) if metrics else 0,
        "avg_gpu": sum(m.get("gpu_util",0) for m in metrics)/len(metrics) if metrics else 0,
        "peak_ram": max(m["ram_used_mb"] for m in metrics) if metrics else 0
    }
    
    # Report
    report = generate_markdown_report(issues, summary)
    console.print(Markdown(report))
    
    # Save Report
    with open("ai_optix_report.md", "w") as f:
        f.write(report)
    console.print("\n[blue]Report saved to ai_optix_report.md[/blue]")

@app.command()
def optimize(
    rows: int = typer.Option(100, help="Number of rows"),
    cols: int = typer.Option(100, help="Number of columns"),
    backend: str = typer.Option(None, help="Force backend (cpu/gpu)")
):
    """
    Run a demo optimization task.
    """
    from ai_optix.api.optimizer import AIModelOptimizer
    
    opt = AIModelOptimizer("cli-optimizer")
    
    total_elements = rows * cols
    # Safety check: Warn if > 100M elements (approx 800MB - 1GB RAM)
    if total_elements > 100_000_000:
        console.print(f"[bold red]Error:[/bold red] Requested size ({total_elements:,} elements) is too large for this demo.")
        console.print(f"This would require allocating > {total_elements * 8 / 1024 / 1024 / 1024:.2f} GB of RAM.")
        raise typer.Exit(code=1)

    try:
        data = [1.0] * total_elements
        
        start = time.time()
        result = opt.optimize(data, rows, cols)
        end = time.time()
    except MemoryError:
        console.print("[bold red]Error:[/bold red] System ran out of memory while allocating data.")
        raise typer.Exit(code=1)
    
    if backend is None:
        suggestion = opt.suggest_backend(rows * cols * 8)
        console.print(f"[blue]Suggested Backend: {suggestion}[/blue]")

    console.print("[green]Optimization Complete[/green]")
    console.print(f"Device: {result.device}")
    console.print(f"Optimized: {result.optimized}")
    console.print(f"Rust Execution Time: {result.execution_time_ms:.2f} ms")
    console.print(f"Total Python Time: {(end - start)*1000:.2f} ms")

@app.command()
def analyze(run_id: str):
    """
    Analyze a past run (placeholder).
    """
    console.print(f"Analyzing run {run_id} (Not implemented yet)")

def main():
    app()

if __name__ == "__main__":
    main()
