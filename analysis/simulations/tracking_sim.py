import numpy as np
import time
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.kinematics import SOTMKinematics
from src.stabilization import SOTMStabilizer

def run_verification_sim(duration=10.0, step=0.02, headless=False):
    """
    Simulates the platform movement and measures tracking error.
    """
    target_az, target_el = 180.0, 30.0
    stabilizer = SOTMStabilizer(target_az=target_az, target_el=target_el)
    
    # Initial state
    current_az, current_el = target_az, target_el
    log_data = []
    
    if not headless:
        print(f"Starting Simulation: Target Az={target_az}, El={target_el}")
        print("-" * 50)
    
    for t in np.arange(0, duration, step):
        # Platform motion (Stewart platform envelope: ±8 degrees)
        roll = 8.0 * np.sin(2 * np.pi * t / 10.0)
        pitch = 8.0 * np.cos(2 * np.pi * t / 10.0)
        yaw = 0.0
        
        # Stabilizer update (returns state dict)
        state = stabilizer.update(roll, pitch, yaw, current_az, current_el, dt=step)
        
        # Update current position (Simple integrator simulation)
        current_az += state["az_cmd"]
        current_el += state["el_cmd"]
        
        # Logging for analysis
        log_entry = {
            "timestamp": t,
            "roll": roll,
            "pitch": pitch,
            "actual_az": current_az,
            "actual_el": current_el,
            "target_az": state["target_az"],
            "target_el": state["target_el"],
            "az_error": state["az_error"],
            "el_error": state["el_error"]
        }
        log_data.append(log_entry)
        
        if not headless and int(t/step) % 50 == 0:
            print(f"T={t:.2f}s | Roll={roll:5.2f}° | Ideal Az={state['target_az']:6.2f} | Current Az={current_az:6.2f} | Error={np.sqrt(state['az_error']**2 + state['el_error']**2):5.4f}°")

    # Save to CSV for CI/CD 'Gökbörü Guardian'
    import pandas as pd
    df = pd.DataFrame(log_data)
    df.to_csv("mission_log.csv", index=False)
    
    max_error = np.sqrt(df['az_error']**2 + df['el_error']**2).max()
    
    if not headless:
        print("-" * 50)
        print(f"Simulation Complete. Log saved to mission_log.csv")
        print(f"Maximum Tracking Error: {max_error:.6f}°")
    
    return max_error

if __name__ == "__main__":
    is_headless = "--headless" in sys.argv
    max_err = run_verification_sim(headless=is_headless)
    if max_err > 0.5:
        sys.exit(1)
    else:
        sys.exit(0)
