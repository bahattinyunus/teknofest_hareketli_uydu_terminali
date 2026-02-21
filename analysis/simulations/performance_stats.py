import pandas as pd
import numpy as np
import sys
import os

def analyze_log(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    print(f"\n--- GÖKBÖRÜ SOTM PERFORMANCE ANALYSIS ---")
    print(f"Analyzing: {os.path.basename(file_path)}")
    
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # Check for required columns
    required = ['az_error', 'el_error', 'roll', 'pitch']
    if not all(col in df.columns for col in required):
        print(f"Error: Log file missing required SoTM columns: {required}")
        return

    # Calculate Metrics
    df['total_error'] = np.sqrt(df['az_error']**2 + df['el_error']**2)
    
    metrics = {
        "Avg Tracking Error": df['total_error'].mean(),
        "Max Tracking Error": df['total_error'].max(),
        "Std Dev Error": df['total_error'].std(),
        "Max Platform Tilt (Roll)": df['roll'].abs().max(),
        "Max Platform Tilt (Pitch)": df['pitch'].abs().max(),
        "Sample Count": len(df)
    }

    print("-" * 40)
    for key, val in metrics.items():
        unit = "°" if "Error" in key or "Tilt" in key else ""
        print(f"{key:25}: {val:8.4f}{unit}")
    
    # Threshold Check (Teknofest Limit: 0.5°)
    if metrics["Max Tracking Error"] < 0.5:
        print("\n✅ STATUS: COMPLIANT with Specification (< 0.5°)")
    else:
        print("\n⚠️ STATUS: NON-COMPLIANT (Exceeds 0.5° threshold)")
    print("-" * 40)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze_log(sys.argv[1])
    else:
        print("Usage: python performance_stats.py <mission_log.csv>")
