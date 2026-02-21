import numpy as np
from scipy.optimize import differential_evolution
import sys
import os

# Internal imports
from src.stabilization import SOTMStabilizer

class PIDTuner:
    """
    Auto-tuner for SOTM PID gains using simulation-based optimization.
    """
    def __init__(self, target_az=180.0, target_el=30.0):
        self.target_az = target_az
        self.target_el = target_el
        self.sim_duration = 5.0 # seconds
        self.dt = 0.02 # 50Hz

    def simulate(self, kp, ki, kd):
        """Runs a 5-second simulation with specific gains."""
        stabilizer = SOTMStabilizer(self.target_az, self.target_el)
        stabilizer.pid_az.kp = kp
        stabilizer.pid_az.ki = ki
        stabilizer.pid_az.kd = kd
        
        # We'll use the same gains for Elevation for simplicity or expand later
        stabilizer.pid_el.kp = kp
        stabilizer.pid_el.ki = ki
        stabilizer.pid_el.kd = kd

        error_sum = 0
        max_error = 0
        
        # Simulation scenario: Sine wave disturbance on platform
        steps = int(self.sim_duration / self.dt)
        for i in range(steps):
            t = i * self.dt
            # Disturbances: Roll/Pitch tilting up to 8 degrees
            roll = 8.0 * np.sin(2 * np.pi * 0.5 * t)
            pitch = 8.0 * np.cos(2 * np.pi * 0.3 * t)
            
            # Start slightly off-target to test settling
            current_az = self.target_az + (5.0 if i == 0 else 0)
            current_el = self.target_el + (5.0 if i == 0 else 0)
            
            state = stabilizer.update(roll, pitch, 0, current_az, current_el, self.dt)
            
            err = np.sqrt(state["az_error"]**2 + state["el_error"]**2)
            error_sum += (err**2) * self.dt # Integrated Squared Error (ISE)
            max_error = max(max_error, err)

        return error_sum + (max_error * 10) # Heavy penalty for peak error

    def objective(self, x):
        """Scipy objective function: x = [kp, ki, kd]"""
        return self.simulate(x[0], x[1], x[2])

    def optimize(self):
        print(f"🚀 Starting AI PID Optimization for GÖKBÖRÜ SOTM...")
        print(f"Target: Minimize Tracking Error under 8° dynamic oscillation.")
        
        # Bounds: [Kp, Ki, Kd]
        bounds = [(0.01, 1.0), (0.0, 0.5), (0.0, 0.1)]
        
        result = differential_evolution(self.objective, bounds, strategy='best1bin', 
                                       maxiter=20, popsize=10, mutation=(0.5, 1), 
                                       recombination=0.7, tol=0.01)
        
        if result.success:
            print("\n✅ Optimization Successful!")
            print(f"Suggested Gains: Kp={result.x[0]:.4f}, Ki={result.x[1]:.4f}, Kd={result.x[2]:.4f}")
            print(f"Minimal Cost Found: {result.fun:.6f}")
            return result.x
        else:
            print("\n❌ Optimization failed to converge.")
            return None

if __name__ == "__main__":
    tuner = PIDTuner()
    best_gains = tuner.optimize()
    if best_gains is not None:
        print("\n[TIP] Update config.json with these values for elite performance.")
