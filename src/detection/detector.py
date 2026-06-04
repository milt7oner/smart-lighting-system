from ultralytics import YOLO
import cv2
import yaml
import time
from src.utils.logger import setup_logger

logger = setup_logger("detector")

# COCO classes we care about
ROAD_AGENTS = {
    0: "person",
    1: "bicycle", 
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck"
}

class VehicleDetector:
    def __init__(self, config_path: str = "config/settings.yaml"):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        
        self.model = YOLO(config["model"]["name"])
        self.confidence = config["model"]["confidence_threshold"]
        self.device = config["model"]["device"]
        logger.info(f"Model loaded | confidence={self.confidence}")

    def detect(self, frame):
        """
        Run detection on a single frame.
        Returns list of detected road agents with class, confidence and bbox.
        """
        start = time.time()
        results = self.model(frame, conf=self.confidence, device=self.device, verbose=False)
        inference_time = (time.time() - start) * 1000  # ms

        detections = []
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                if class_id in ROAD_AGENTS:
                    detections.append({
                        "class": ROAD_AGENTS[class_id],
                        "confidence": round(float(box.conf[0]), 2),
                        "bbox": box.xyxy[0].tolist()
                    })

        logger.info(f"Inference: {inference_time:.1f}ms | Detections: {len(detections)}")
        return detections, inference_time