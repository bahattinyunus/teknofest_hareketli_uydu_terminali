import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import os

class SOTMVibrationAnalyzer:
    """
    AI-Driven Predictive Maintenance Module.
    Uses Isolation Forest to detect anomalous vibration patterns (simulated FFT/IMU data)
    indicating potential actuator fatigue or gear wear.
    """
    def __init__(self, contamination=0.05):
        self.model = IsolationForest(n_estimators=100, contamination=contamination, random_state=42)
        self.is_trained = False

    def generate_synthetic_data(self, samples=1000):
        """Simulates healthy and anomalous vibration signals (Z-Axis Acceleration Variance)"""
        print("⚙️ Generating synthetic vibration telemetry...")
        
        # Healthy operation: Baseline vibration with uniform thermal noise
        healthy_z_var = np.random.normal(0.01, 0.002, int(samples * 0.9))
        healthy_temp = np.random.normal(45.0, 5.0, int(samples * 0.9))
        
        # Anomalous operation: Micro-stuttering in gears causing high variance
        anomaly_z_var = np.random.normal(0.05, 0.015, int(samples * 0.1))
        anomaly_temp = np.random.normal(70.0, 10.0, int(samples * 0.1)) # Associated with heating
        
        z_var = np.concatenate([healthy_z_var, anomaly_z_var])
        temp = np.concatenate([healthy_temp, anomaly_temp])
        
        df = pd.DataFrame({'Z_Accel_Variance': z_var, 'Motor_Temp_C': temp})
        # Shuffle
        return df.sample(frac=1).reset_index(drop=True)

    def train(self, df: pd.DataFrame):
        print("🧠 Training AI Model (Isolation Forest)...")
        features = df[['Z_Accel_Variance', 'Motor_Temp_C']].values
        self.model.fit(features)
        self.is_trained = True
        print("✅ Training Complete.")

    def analyze_and_plot(self, df: pd.DataFrame):
        if not self.is_trained:
            self.train(df)
            
        print("🔍 Scanning for mechanical anomalies...")
        features = df[['Z_Accel_Variance', 'Motor_Temp_C']].values
        
        # 1 = Normal, -1 = Anomaly
        predictions = self.model.predict(features)
        df['Anomaly'] = predictions
        
        anomalies = df[df['Anomaly'] == -1]
        print(f"⚠️ Detected {len(anomalies)} critical anomaly frames out of {len(df)}.")
        
        # Visualization
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.scatter(df[df['Anomaly'] == 1]['Z_Accel_Variance'], 
                   df[df['Anomaly'] == 1]['Motor_Temp_C'], 
                   color='#3fb950', alpha=0.6, label='Healthy Operation')
                   
        ax.scatter(df[df['Anomaly'] == -1]['Z_Accel_Variance'], 
                   df[df['Anomaly'] == -1]['Motor_Temp_C'], 
                   color='#f85149', alpha=0.9, marker='x', label='Critical Vibration/Temp Anomaly')
                   
        ax.set_title("GÖKBÖRÜ Edge AI: Actuator Fatigue Detection", color='white', pad=20)
        ax.set_xlabel("Z-Axis Acceleration Variance (g²)")
        ax.set_ylabel("Motor Junction Temperature (°C)")
        ax.legend()
        ax.grid(True, alpha=0.1)
        
        os.makedirs('analysis/reports', exist_ok=True)
        out_path = 'analysis/reports/ai_vibration_report.png'
        plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='#0d1117')
        print(f"📊 AI Analysis Report saved to {out_path}")
        plt.show()

if __name__ == "__main__":
    analyzer = SOTMVibrationAnalyzer()
    dataset = analyzer.generate_synthetic_data(samples=1000)
    analyzer.analyze_and_plot(dataset)
