from src.utils.benchmarker import ModelBenchmarker

benchmarker = ModelBenchmarker()

print("Benchmarking original FP32 model...")
fp32_results = benchmarker.benchmark_yolov8("yolov8n.pt", runs=10)

benchmarker.print_report([fp32_results])