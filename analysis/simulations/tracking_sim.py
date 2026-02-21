import numpy as np
import time
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.kinematics import SOTMKinematics
from src.stabilization import SOTMStabilizer

def run_verification_sim(duration=10.0, step=0.02):
    """
    Simulates the platform movement and measures tracking error.
    """
    target_az, target_el = 180.0, 30.0
    stabilizer = SOTMStabilizer(target_az=target_az, target_el=target_el)
    
    # Initial state
    current_az, current_el = target_az, target_el
    errors = []
    
    print(f"Starting Simulation: Target Az={target_az}, El={target_el}")
    print("-" * 50)
    
    for t in np.arange(0, duration, step):
        # Platform motion (Stewart platform envelope: ±8 degrees)
        roll = 8.0 * np.sin(2 * np.pi * t / 10.0)
        pitch = 8.0 * np.cos(2 * np.pi * t / 10.0)
        yaw = 0.0
        
        # Stabilizer update (PID)
        az_cmd, el_cmd = stabilizer.update(roll, pitch, yaw, current_az, current_el, dt=step)
        
        # Update current position (Simple integrator simulation)
        current_az += az_cmd
        current_el += el_cmd
        
        # Calculate Ideal Target for this moment
        ideal_az, ideal_el = stabilizer.kinematics.get_antenna_angles(roll, pitch, yaw)
        
        # Tracking Error
        err_az = abs(ideal_az - current_az)
        err_el = abs(ideal_el - current_el)
        if err_az > 180: err_az = abs(err_az - 360)
        
        total_err = np.sqrt(err_az**2 + err_el**2)
        errors.append(total_err)
        
        if int(t/step) % 50 == 0:
            print(f"T={t:.2f}s | Roll={roll:5.2f}° | Ideal Az={ideal_az:6.2f} | Current Az={current_az:6.2f} | Error={total_err:5.4f}°")

    avg_error = np.mean(errors)
    max_error = np.max(errors)
    
    print("-" * 50)
    print(f"Simulation Complete over {duration}s")
    print(f"Average Tracking Error: {avg_error:.6f}°")
    print(f"Maximum Tracking Error: {max_error:.6f}°")
    
    if max_error < 0.5:
        print("VERIFICATION SUCCESS: Tracking error is within Teknofest limits (< 0.5°)")
    else:
        print("VERIFICATION FAILED: Maximum error exceeds 0.5°")

if __name__ == "__main__":
    run_verification_sim()
