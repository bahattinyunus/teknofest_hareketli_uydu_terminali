import numpy as np

class KalmanFilter:
    """
    A simple 1D Kalman Filter for sensor fusion (e.g. Accelerometer + Gyroscope).
    """
    def __init__(self, process_variance=0.01, measurement_variance=0.1):
        self.q = process_variance      # Process noise variance
        self.r = measurement_variance  # Measurement noise variance
        self.p = 1.0                   # Estimated error covariance
        self.x = 0.0                   # Estimated state (angle)
        self.k = 0.0                   # Kalman gain

    def update(self, measurement):
        """
        Updates the filter with a new measurement from the sensor.
        Includes GNSS/IMU Anti-Spoofing (Kinematic Plausibility Gate).
        """
        # Anti-Spoofing Check: Physical limit for sudden angular change (e.g., max 10 degrees per frame)
        MAX_DELTA = 10.0
        if abs(measurement - self.x) > MAX_DELTA and self.p < 5.0: # Using self.p for uncertainty
            # Plausibility Gate Failed! Likely a spoofing attack or sensor glitch.
            # Reject measurement, rely on prediction (Inertial Dead-Reckoning)
            # We purposely do NOT update self.x with the measurement.
            return self.x

        # Standard Update (Kalman Gain)
        # Prediction update for covariance (assuming dt=1 for simplicity or integrated into process_variance)
        self.p = self.p + self.q # Re-added prediction step for covariance

        kalman_gain = self.p / (self.p + self.r)
        self.x = self.x + kalman_gain * (measurement - self.x)
        self.p = (1 - kalman_gain) * self.p
        
        return self.x

class SOTMSensorFusion:
    """
    Fuses orientation data for the SOTM terminal.
    In a real system, this would fuse Accel and Gyro. Here it cleans noise.
    """
    def __init__(self):
        self.roll_filt = KalmanFilter(process_variance=0.005, measurement_variance=0.05)
        self.pitch_filt = KalmanFilter(process_variance=0.005, measurement_variance=0.05)

    def process(self, roll_raw, pitch_raw):
        """
        Filters raw Roll and Pitch data.
        """
        roll_clean = self.roll_filt.update(roll_raw)
        pitch_clean = self.pitch_filt.update(pitch_raw)
        return roll_clean, pitch_clean

if __name__ == "__main__":
    # Test: Noise reduction
    fusion = SOTMSensorFusion()
    for i in range(10):
        raw = 5.0 + np.random.normal(0, 1) # 5 degrees + noise
        clean, _ = fusion.process(raw, 0)
        print(f"Raw: {raw:5.2f} | Clean: {clean:5.2f}")
