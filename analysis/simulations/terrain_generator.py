import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

class ISO8608Terrain:
    """
    ISO 8608 Road Surface Profile Generator.
    Generates hyper-realistic 6-DOF disturbances (mainly Roll/Pitch) based on spectral density.
    
    Road Classes (Degree of roughness):
    A: Very Good (Smooth Tarmac)
    C: Average (Rough Macadam/Dirt Road)
    E: Poor (Severe Off-Road / Tactical Terrain)
    """
    CLASSES = {
        'A': 16e-6,
        'C': 256e-6,
        'E': 4096e-6
    }
    
    def __init__(self, road_class='C', velocity_kph=40.0, wheelbase=2.5, track_width=1.8):
        self.road_class = road_class
        self.Gd_n0 = self.CLASSES.get(road_class.upper(), self.CLASSES['C'])
        self.v = velocity_kph / 3.6  # Convert to m/s
        self.L = wheelbase           # meters
        self.W = track_width         # meters
        
    def generate_profile(self, duration=10.0, dt=0.02):
        """Generates the Roll and Pitch arrays over time."""
        print(f"🌍 Generating ISO 8608 Class {self.road_class} Terrain at {self.v*3.6:.1f} km/h...")
        n_samples = int(duration / dt)
        time = np.linspace(0, duration, n_samples)
        
        # Spatial frequencies (cycles/meter) from 0.01 to 10 
        delta_n = 0.01
        n_space = np.arange(0.01, 10.0, delta_n)
        
        # Power Spectral Density (PSD) calculation
        Gd_n = self.Gd_n0 * (n_space / 0.1) ** (-2)
        
        # Amplitudes from PSD
        A = np.sqrt(2 * Gd_n * delta_n)
        
        # Generate left and right track elevations
        left_track = np.zeros(n_samples)
        right_track = np.zeros(n_samples)
        
        for i, ns in enumerate(n_space):
            phase_l = np.random.uniform(0, 2 * np.pi)
            phase_r = np.random.uniform(0, 2 * np.pi)
            
            omega = 2 * np.pi * ns * self.v
            left_track += A[i] * np.sin(omega * time + phase_l)
            right_track += A[i] * np.sin(omega * time + phase_r)
            
        # Delay rear tires based on wheelbase and velocity
        delay_idx = int((self.L / self.v) / dt)
        rear_left = np.pad(left_track, (delay_idx, 0))[:-delay_idx] if delay_idx > 0 else left_track
        rear_right = np.pad(right_track, (delay_idx, 0))[:-delay_idx] if delay_idx > 0 else right_track
        
        # Calculate Roll and Pitch (rad -> deg)
        roll_rad = np.arctan((left_track - right_track) / self.W)
        
        front_avg = (left_track + right_track) / 2
        rear_avg = (rear_left + rear_right) / 2
        pitch_rad = np.arctan((front_avg - rear_avg) / self.L)
        
        roll_deg = np.degrees(roll_rad)
        pitch_deg = np.degrees(pitch_rad)
        
        return pd.DataFrame({
            'Time': time,
            'Roll': roll_deg,
            'Pitch': pitch_deg,
            'Elevation_FL': left_track
        })

    def plot_profile(self, df: pd.DataFrame):
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df['Time'], df['Roll'], label='Vehicle Roll (deg)', color='#00d4ff', alpha=0.9)
        ax.plot(df['Time'], df['Pitch'], label='Vehicle Pitch (deg)', color='#ff3366', alpha=0.9)
        
        ax.set_title(f"ISO 8608 Class {self.road_class} Terrain Profile - {self.v*3.6:.0f} km/h", color='white', pad=15)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Angle Disturbance (degrees)")
        ax.legend()
        ax.grid(alpha=0.15)
        
        os.makedirs('analysis/reports', exist_ok=True)
        out_path = f'analysis/reports/terrain_class_{self.road_class.lower()}.png'
        plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='#0d1117')
        print(f"📊 Terrain Profile saved to {out_path}")
        plt.show()

if __name__ == "__main__":
    # Test Severe Tactical Off-Road Profile
    terrain = ISO8608Terrain(road_class='E', velocity_kph=35.0)
    df = terrain.generate_profile(duration=15.0)
    terrain.plot_profile(df)
