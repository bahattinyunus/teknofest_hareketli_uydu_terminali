import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

def generate_report(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    print(f"Generating Visual Report for: {file_path}")
    df = pd.read_csv(file_path)
    
    # Create figure
    fig, axs = plt.subplots(2, 1, figsize=(10, 8))
    fig.suptitle(f"GÖKBÖRÜ SOTM Mission Analysis - {os.path.basename(file_path)}", fontsize=16)

    # Plot 1: Tracking Errors
    axs[0].plot(df['timestamp'], df['az_error'], label='Azimuth Error', color='green')
    axs[0].plot(df['timestamp'], df['el_error'], label='Elevation Error', color='orange')
    axs[0].axhline(y=0.5, color='red', linestyle='--', label='Threshold (0.5°)')
    axs[0].set_ylabel('Error (Degrees)')
    axs[0].set_title('Antenna Tracking Accuracy over Time')
    axs[0].legend()
    axs[0].grid(True, alpha=0.3)

    # Plot 2: Platform Motion (Disturbances)
    axs[1].plot(df['timestamp'], df['roll'], label='Roll', color='red', alpha=0.7)
    axs[1].plot(df['timestamp'], df['pitch'], label='Pitch', color='blue', alpha=0.7)
    axs[1].set_ylabel('Platform angle (Degrees)')
    axs[1].set_xlabel('Time (s)')
    axs[1].set_title('Platform Disturbances (SoTM Environment)')
    axs[1].legend()
    axs[1].grid(True, alpha=0.3)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    output_name = file_path.replace(".csv", "_report.png")
    plt.savefig(output_name)
    print(f"✅ Report saved as: {output_name}")
    
    # Show plot if not headless
    if "--no-show" not in sys.argv:
        plt.show()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_report(sys.argv[1])
    else:
        print("Usage: python report_generator.py <mission_log.csv>")
