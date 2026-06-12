import cv2
from src.detection.detector import VehicleDetector
from src.detection.ambient_sensor import AmbientLightSensor
from src.lighting.lighting_controller import LightingController
from src.communication.mqtt_publisher import MQTTPublisher
from src.utils.logger import setup_logger

logger = setup_logger("main")

def main():
    detector = VehicleDetector()
    ambient_sensor = AmbientLightSensor()
    controller = LightingController()
    publisher = MQTTPublisher()

    # Connect to MQTT broker
    logger.info("Connecting to MQTT broker...")
    connected = publisher.connect()
    if not connected:
        logger.warning("MQTT unavailable — running without publishing")

    frame = cv2.imread("assets/videos/test_image.jpg")
    if frame is None:
        logger.error("Could not load test image")
        return

    # Full pipeline
    detections, inference_ms = detector.detect(frame)
    ambient_condition = ambient_sensor.get_condition(frame)
    lighting_state = controller.update(detections, ambient_condition)

    # Publish to MQTT
    if connected:
        publisher.publish_lighting_state(lighting_state, detections, ambient_condition)

    # Report
    print("\n── SYSTEM REPORT ──────────────────────")
    print(f"Inference time : {inference_ms:.1f}ms")
    print(f"Detections     : {len(detections)}")
    for d in detections:
        print(f"  → {d['class']} ({d['confidence']})")
    print(f"Ambient        : {ambient_condition}")
    print(f"High beam      : {lighting_state['high_beam']}")
    print(f"Low beam       : {lighting_state['low_beam']}")
    print(f"Floor light    : {lighting_state['floor_light']}")
    print(f"MQTT published : {connected}")
    print("───────────────────────────────────────\n")

    publisher.disconnect()

if __name__ == "__main__":
    main()