import time
from .kinematics import SOTMKinematics

class PID:
    """A simple PID controller."""
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.last_error = None
        self.integral = 0
        self.last_time = time.time()

    def update(self, setpoint, measured_value, dt=None):
        if dt is None:
            now = time.time()
            dt = now - self.last_time
            self.last_time = now

        if dt <= 0: return 0
        
        error = setpoint - measured_value
        
        # Simple error normalization for angles (wrapping)
        if error > 180: error -= 360
        if error < -180: error += 360
        
        if self.last_error is None:
            self.last_error = error
            
        self.integral += error * dt
        derivative = (error - self.last_error) / dt
        
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        
        self.last_error = error
        return output

class SOTMStabilizer:
    """
    Main stabilization logic that combines kinematics and PID control.
    """
    def __init__(self, target_az=180.0, target_el=45.0):
        self.kinematics = SOTMKinematics()
        self.kinematics.set_target_satellite(target_az, target_el)
        
        # Separate PIDs for Azimuth and Elevation
        # For a discrete integrator with step 0.02, total gain (Kp + Kd/dt) should be < 1.0
        # 0.15 + (0.002 / 0.02) = 0.15 + 0.1 = 0.25 (Stable)
        self.pid_az = PID(kp=0.15, ki=0.01, kd=0.002)
        self.pid_el = PID(kp=0.15, ki=0.01, kd=0.002)
        
        # State
        self.current_az = 0.0
        self.current_el = 0.0
        
    def update(self, roll, pitch, yaw, feedback_az, feedback_el, dt=None):
        """
        Runs one iteration of the control loop.
        
        Args:
            roll, pitch, yaw: From IMU (Body Frame)
            feedback_az, feedback_el: From motor encoders (Current position)
            dt: Optional time step
            
        Returns:
            tuple: (az_command, el_command) to the motor drivers.
        """
        # 1. Get the ideal target angles from kinematics
        target_az, target_el = self.kinematics.get_antenna_angles(roll, pitch, yaw)
        
        # 2. Run PID to get motor correction
        az_output = self.pid_az.update(target_az, feedback_az, dt)
        el_output = self.pid_el.update(target_el, feedback_el, dt)
        
        # In a real system, these would be velocity or position commands
        return az_output, el_output

if __name__ == "__main__":
    # Integration test snippet
    stabilizer = SOTMStabilizer(target_az=180, target_el=30)
    
    # Simulate a movement
    # Platform tilts 5 degrees roll
    az_cmd, el_cmd = stabilizer.update(roll=5.0, pitch=0, yaw=0, feedback_az=180, feedback_el=30)
    print(f"Az Command: {az_cmd:.2f}, El Command: {el_cmd:.2f}")
