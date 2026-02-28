import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.sensor_fusion import SOTMSensorFusion

class KalmanAutoTuner:
    """
    Evaluates and Tunes the Process (Q) and Measurement (R) covariances 
    of the SOTM Extended Kalman Filter to minimize Root Mean Square Error (RMSE).
    """
    def __init__(self):
        # We sweep Q and R to find the optimal ratio for our specific IMU noise profile.
        self.q_candidates = [0.001, 0.005, 0.01, 0.05]
        self.r_candidates = [0.01, 0.05, 0.1, 0.5, 1.0]
        
    def generate_test_signal(self, duration=100, dt=0.02):
        """Generates a truth signal + noisy IMU measurement."""
        np.random.seed(42)
        n_samples = int(duration / dt)
        time = np.linspace(0, duration, n_samples)
        
        # True kinematic motion (Sine sweep + low frequency drift)
        truth = 10 * np.sin(2 * np.pi * 0.5 * time) + 2 * np.sin(2 * np.pi * 0.1 * time)
        
        # Add high-frequency Gaussian noise (Simulating MPU6050 vibration)
        imu_noise = np.random.normal(0, 1.5, n_samples)
        measurements = truth + imu_noise
        
        return time, truth, measurements
        
    def evaluate_configuration(self, q, r, measurements, truth):
        """Runs the Kalman filter over the dataset and returns RMSE."""
        fusion = SOTMSensorFusion()
        # Override default variances
        fusion.roll_filt.q = q
        fusion.roll_filt.r = r
        
        estimations = []
        for m in measurements:
            est = fusion.process(m, 0)[0] # Just evaluate Roll
            estimations.append(est)
            
        estimations = np.array(estimations)
        rmse = np.sqrt(np.mean((estimations - truth)**2))
        return rmse, estimations

    def auto_tune(self):
        print("🧠 Initiating Kalman Filter Auto-Tuner...")
        time, truth, measurements = self.generate_test_signal(duration=30)
        
        best_rmse = float('inf')
        best_q = None
        best_r = None
        best_est = None
        
        results = []
        
        for q in self.q_candidates:
            for r in self.r_candidates:
                rmse, est = self.evaluate_configuration(q, r, measurements, truth)
                results.append((q, r, rmse))
                print(f"Testing Q={q:.3f}, R={r:.3f} -> RMSE: {rmse:.4f}")
                
                if rmse < best_rmse:
                    best_rmse = rmse
                    best_q = q
                    best_r = r
                    best_est = est
                    
        print("-" * 50)
        print("🎯 OPTIMAL KALMAN PARAMETERS FOUND")
        print(f"Process Variance (Q): {best_q:.4f}")
        print(f"Measurement Variance (R): {best_r:.4f}")
        print(f"Final RMSE: {best_rmse:.4f} degrees")
        print("-" * 50)
        
        # Plotting the victory
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(time, truth, 'w-', lw=2, label="Ground Truth (Actual Motion)")
        ax.plot(time, measurements, 'r.', markersize=2, alpha=0.3, label="Raw IMU Sensor Data")
        ax.plot(time, best_est, '#00d4ff', lw=1.5, label=f"Optimized Kalman Filter (RMSE: {best_rmse:.2f})")
        
        ax.set_title("SOTM Avionics: Kalman Filter Optimization", color='white', pad=10)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Roll Angle (degrees)")
        ax.legend()
        ax.grid(alpha=0.2)
        
        os.makedirs('analysis/reports', exist_ok=True)
        out_path = 'analysis/reports/kalman_tuning_report.png'
        plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='#0d1117')
        print(f"📊 Auto-tuning graph saved to {out_path}")
        # plt.show() # Disabled for headless CLI operation

if __name__ == "__main__":
    tuner = KalmanAutoTuner()
    tuner.auto_tune()
