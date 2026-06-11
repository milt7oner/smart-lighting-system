import time
import cv2
import numpy as np
from src.utils.logger import setup_logger

logger = setup_logger("benchmarker")

class ModelBenchmarker:
    def __init__(self, test_image_path: str = "assets/videos/test_image.jpg"):
        self.image_path = test_image_path
        self.frame = cv2.imread(test_image_path)
        if self.frame is None:
            raise FileNotFoundError(f"Test image not found: {test_image_path}")
        logger.info(f"Benchmarker initialized | image={test_image_path}")

    def benchmark_yolov8(self, model_path: str, runs: int = 10) -> dict:
        """
        Benchmark YOLOv8 .pt model inference speed.
        Runs multiple times and returns average latency.
        """
        from ultralytics import YOLO
        model = YOLO(model_path)

        # Warm-up run — not counted
        model(self.frame, verbose=False)

        latencies = []
        for _ in range(runs):
            start = time.time()
            model(self.frame, verbose=False)
            latencies.append((time.time() - start) * 1000)

        return {
            "model": model_path,
            "runs": runs,
            "avg_ms": round(np.mean(latencies), 1),
            "min_ms": round(np.min(latencies), 1),
            "max_ms": round(np.max(latencies), 1),
        }

    def print_report(self, results: list):
        """Print a formatted comparison report."""
        print("\n── BENCHMARK REPORT ────────────────────")
        for r in results:
            print(f"\nModel  : {r['model']}")
            print(f"Runs   : {r['runs']}")
            print(f"Avg    : {r['avg_ms']} ms")
            print(f"Min    : {r['min_ms']} ms")
            print(f"Max    : {r['max_ms']} ms")
        print("\n────────────────────────────────────────\n")