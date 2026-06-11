import os
from ultralytics import YOLO
from src.utils.logger import setup_logger

logger = setup_logger("model_exporter")

class ModelExporter:
    def __init__(self, model_path: str = "yolov8n.pt"):
        self.model_path = model_path
        self.model = YOLO(model_path)
        logger.info(f"Model loaded for export: {model_path}")

    def export_tflite(self, int8: bool = True) -> str:
        """
        Export YOLOv8 model to TFLite format.
        int8=True applies INT8 quantization.
        Returns path to exported model.
        """
        logger.info(f"Exporting to TFLite | int8={int8}")

        self.model.export(
            format="tflite",
            int8=int8,
            imgsz=640
        )

        model_name = self.model_path.replace(".pt", "")
        exported_path = f"{model_name}_saved_model/{model_name}_int8.tflite"
        logger.info(f"Export complete | path={exported_path}")
        return exported_path

    def compare_sizes(self) -> dict:
        """
        Compare original model size vs exported TFLite INT8 size.
        """
        original_size = os.path.getsize(self.model_path) / (1024 * 1024)

        model_name = self.model_path.replace(".pt", "")
        tflite_path = f"{model_name}_saved_model/{model_name}_int8.tflite"

        result = {
            "original_pt": round(original_size, 2),
            "tflite_int8": None,
            "tflite_path": tflite_path
        }

        if os.path.exists(tflite_path):
            tflite_size = os.path.getsize(tflite_path) / (1024 * 1024)
            result["tflite_int8"] = round(tflite_size, 2)
            reduction = ((original_size - tflite_size) / original_size) * 100
            logger.info(f"Size reduction: {reduction:.1f}%")
        else:
            logger.warning(f"TFLite file not found at: {tflite_path}")

        return result