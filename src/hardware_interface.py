from abc import ABC, abstractmethod

class MotorController(ABC):
    @abstractmethod
    def set_angle(self, angle: float):
        pass

    @abstractmethod
    def get_angle(self) -> float:
        pass

class SensorInterface(ABC):
    @abstractmethod
    def get_orientation(self) -> tuple:
        """Returns (roll, pitch, yaw) in degrees."""
        pass

    @abstractmethod
    def get_gps(self) -> tuple:
        """Returns (lat, lon, alt)."""
        pass

class HardwareAbstrationLayer:
    """
    Combines Azimuth, Elevation motors and IMU/GPS sensors.
    """
    def __init__(self, az_motor: MotorController, el_motor: MotorController, sensors: SensorInterface):
        self.az_motor = az_motor
        self.el_motor = el_motor
        self.sensors = sensors

    def update_antenna(self, az_cmd, el_cmd):
        # Apply PID outputs or direct angle commands
        # For simplicity in this demo, we'll assume these are set_angle targets
        self.az_motor.set_angle(self.az_motor.get_angle() + az_cmd)
        self.el_motor.set_angle(self.el_motor.get_angle() + el_cmd)
