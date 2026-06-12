import json
import time
import paho.mqtt.client as mqtt
from src.utils.logger import setup_logger

logger = setup_logger("mqtt_publisher")

class MQTTPublisher:
    def __init__(self, broker: str = "test.mosquitto.org", port: int = 1883, client_id: str = "smart-lighting-publisher"):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.topic_base = "smart-lighting/vehicle"
        self.connected = False

        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect

        logger.info(f"MQTT Publisher initialized | broker={broker}:{port}")

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            logger.info(f"Connected to MQTT broker | {self.broker}:{self.port}")
        else:
            logger.error(f"Connection failed | rc={rc}")

    def _on_disconnect(self, client, userdata, rc):
        self.connected = False
        logger.warning(f"Disconnected from MQTT broker | rc={rc}")

    def connect(self):
        """Connect to MQTT broker."""
        self.client.connect(self.broker, self.port, keepalive=60)
        self.client.loop_start()
        time.sleep(1)  # Wait for connection
        return self.connected

    def publish_lighting_state(self, lighting_state: dict, detections: list, ambient: str):
        """
        Publish lighting decision to MQTT broker.
        Topic: smart-lighting/vehicle/lighting/state
        """
        if not self.connected:
            logger.warning("Not connected — skipping publish")
            return False

        payload = {
            "timestamp": time.time(),
            "ambient_condition": ambient,
            "detections_count": len(detections),
            "detected_agents": [d["class"] for d in detections],
            "lighting": {
                "high_beam": lighting_state["high_beam"],
                "low_beam": lighting_state["low_beam"],
                "floor_light": lighting_state["floor_light"]
            }
        }

        topic = f"{self.topic_base}/lighting/state"
        self.client.publish(topic, json.dumps(payload), qos=1)
        logger.info(f"Published | topic={topic} | agents={payload['detected_agents']} | high={lighting_state['high_beam']}")
        return True

    def disconnect(self):
        """Cleanly disconnect from broker."""
        self.client.loop_stop()
        self.client.disconnect()
        logger.info("Disconnected from MQTT broker")