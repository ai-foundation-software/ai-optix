from ai_optix.benchmarks.mebs import BenchmarkRunner, BenchmarkConfig

def my_model_op():
    # Your model code here
    pass

config = BenchmarkConfig(name="MyModel", warmup_iters=10000, measure_iters=50000)
runner = BenchmarkRunner(config)
runner.run(my_model_op)
