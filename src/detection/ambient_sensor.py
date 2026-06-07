import cv2
import numpy as np
from src.utils.logger import setup_logger

logger = setup_logger("ambient_sensor")

# Brightness thresholds (0-255 scale)
DAY_THRESHOLD = 100    # Above this = daytime
NIGHT_THRESHOLD = 60   # Below this = nighttime

class AmbientLightSensor:
    def __init__(self):
        logger.info("Ambient light sensor initialized")

    def get_brightness(self, frame) -> float:
        """
        Calculate average brightness of a frame.
        Converts to grayscale and returns mean pixel value (0-255).
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = float(np.mean(gray))
        return round(brightness, 2)

    def get_condition(self, frame) -> str:
        """
        Returns 'day', 'night', or 'transition' based on frame brightness.
        Transition zone avoids flickering between states.
        """
        brightness = self.get_brightness(frame)

        if brightness >= DAY_THRESHOLD:
            condition = "day"
        elif brightness <= NIGHT_THRESHOLD:
            condition = "night"
        else:
            condition = "transition"

        logger.info(f"Brightness: {brightness} | Condition: {condition}")
        return condition