import numpy as np
import time
from .hardware_interface import MotorController, SensorInterface

class SimulatedMotor(MotorController):
    def __init__(self, initial_angle=0.0):
        self.current_angle = initial_angle

    def set_angle(self, angle: float):
        # In simulation, we move immediately to the angle
        # In a more advanced sim, we could add noise or delay
        self.current_angle = angle

    def get_angle(self) -> float:
        return self.current_angle

class SimulatedSensors(SensorInterface):
    def __init__(self):
        self.start_time = time.time()
        
    def get_orientation(self) -> tuple:
        """
        Simulates a Stewart platform movement.
        Roll/Pitch: ±8 degrees with a 10s period.
        """
        t = time.time() - self.start_time
        period = 10.0
        roll = 8.0 * np.sin(2 * np.pi * t / period)
        pitch = 8.0 * np.cos(2 * np.pi * t / period)
        yaw = 0.0 # Keeping yaw stable for now
        return roll, pitch, yaw

    def get_gps(self) -> tuple:
        # Static GPS for Teknofest site (Example)
        return 41.2612, 28.7419, 10.0
