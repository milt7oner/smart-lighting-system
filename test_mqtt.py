from src.communication.mqtt_publisher import MQTTPublisher

publisher = MQTTPublisher()

print("Connecting to MQTT broker...")
connected = publisher.connect()

if connected:
    print("Connected successfully!")
    
    # Test publish
    test_state = {
        "high_beam": False,
        "low_beam": True,
        "floor_light": True
    }
    test_detections = [
        {"class": "car", "confidence": 0.87},
        {"class": "person", "confidence": 0.83}
    ]
    
    publisher.publish_lighting_state(test_state, test_detections, "night")
    print("Message published!")
else:
    print("Connection failed")

publisher.disconnect()