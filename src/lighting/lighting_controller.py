from src.utils.logger import setup_logger

logger = setup_logger("lighting_controller")

# Agent priority for lighting decisions
ONCOMING_VEHICLES = {"car", "bus", "truck"}
VULNERABLE_AGENTS = {"person", "bicycle", "motorcycle"}

class LightingController:
    def __init__(self):
        self.state = {
            "high_beam": False,
            "low_beam": False,
            "floor_light": False,
            "auto_mode": True
        }
        logger.info("Lighting controller initialized")

    def _set_state(self, high: bool, low: bool, floor: bool, reason: str):
        """Update lighting state and log only when something changes."""
        new_state = {"high_beam": high, "low_beam": low, "floor_light": floor}
        changed = any(self.state[k] != v for k, v in new_state.items())

        if changed:
            self.state.update(new_state)
            logger.info(
                f"Lighting changed | high={high} low={low} floor={floor} | reason={reason}"
            )

    def update(self, detections: list, ambient_condition: str) -> dict:
        """
        Main decision engine.
        Receives detections from VehicleDetector and condition from AmbientLightSensor.
        Returns current lighting state.
        """
        # Daytime logic
        if ambient_condition == "day":
            self._set_state(False, False, False, "daytime_auto_off")
            return self.state

        # Nighttime logic — analyze detections
        detected_classes = {d["class"] for d in detections}

        has_oncoming = bool(detected_classes & ONCOMING_VEHICLES)
        has_vulnerable = bool(detected_classes & VULNERABLE_AGENTS)

        if has_oncoming or has_vulnerable:
            self._set_state(False, True, True, f"agents_detected: {detected_classes}")
        else:
            self._set_state(True, False, False, "clear_road")

        return self.state