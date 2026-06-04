# Smart Lighting Edge AI System

An edge AI system that uses computer vision to detect road agents
(vehicles, pedestrians) and dynamically adjusts vehicle headlight
intensity in real time — running on embedded hardware without
cloud dependency.

## Problem
Traditional vehicle lighting systems use static rules.
This system uses real-time object detection to make intelligent
decisions at the edge, reducing glare for oncoming drivers
and improving pedestrian safety.

## Architecture
> Diagram coming in Week 1

## Tech Stack
- YOLOv8 (object detection)
- TensorFlow Lite (edge optimization)
- OpenCV (video processing)
- MQTT (IoT communication)
- Python 3.11
- Target hardware: Raspberry Pi 4

## Status
🚧 Active development — Week 1 of 4

## Roadmap
- [x] Project structure and configuration
- [ ] Object detection module with YOLOv8
- [ ] Lighting decision engine
- [ ] TFLite model optimization
- [ ] MQTT communication layer
- [ ] Raspberry Pi deployment