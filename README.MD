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
## Performance Benchmarks

> Measured on laptop CPU (steady state, 10 runs average)

| Model | Format | Size | Avg Inference | Min | Max |
|-------|--------|------|---------------|-----|-----|
| YOLOv8n | FP32 (.pt) | 6.23 MB | 66.1 ms | 60.4 ms | 76.5 ms |
| YOLOv8n | INT8 (.tflite) | 3.34 MB | TBD on RPi | - | - |

> Raspberry Pi 4 benchmarks coming after hardware deployment.
> Target: < 200ms avg inference on edge hardware.
## Roadmap
- [x] Project structure and configuration
- [ ] Object detection module with YOLOv8
- [ ] Lighting decision engine
- [ ] TFLite model optimization
- [ ] MQTT communication layer
- [ ] Raspberry Pi deployment