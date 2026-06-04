from src.detection.detector import VehicleDetector

detector = VehicleDetector()
results, ms = detector.detect("assets/videos/test_image.jpg")

print(f"\nInference time: {ms:.1f}ms")
print(f"Detections found: {len(results)}")
for d in results:
    print(f"  - {d['class']} ({d['confidence']})")