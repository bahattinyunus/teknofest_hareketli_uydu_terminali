import sys
import numpy as np
import csv
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QComboBox
from PyQt6.QtCore import QTimer
import pyqtgraph as pg

from .stabilization import SOTMStabilizer
from .simulated_hardware import SimulatedMotor, SimulatedSensors
from .hardware_interface import HardwareAbstrationLayer

class SOTMDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🐺 GÖKBÖRÜ SOTM Control Station | Elite Edition")
        self.resize(1100, 800)
        
        # Apply Premium Dark Theme
        self.setStyleSheet("""
            QMainWindow { background-color: #0d1117; }
            QLabel { color: #c9d1d9; font-family: 'Segoe UI', sans-serif; }
            QPushButton { 
                background-color: #21262d; 
                color: #58a6ff; 
                border: 1px solid #30363d; 
                padding: 8px; 
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #30363d; border-color: #8b949e; }
            QComboBox { 
                background-color: #0d1117; 
                color: #c9d1d9; 
                border: 1px solid #30363d; 
                padding: 5px; 
            }
        """)

        # Core Components
        self.sensors = SimulatedSensors()
        self.az_motor = SimulatedMotor(initial_angle=180.0)
        self.el_motor = SimulatedMotor(initial_angle=30.0)
        self.hal = HardwareAbstrationLayer(self.az_motor, self.el_motor, self.sensors)
        self.stabilizer = SOTMStabilizer(target_az=180.0, target_el=30.0)
        
        # Logging
        self.logging_enabled = False
        self.log_file = None
        self.csv_writer = None

        self.init_ui()
        
        # Configure Plots for Dark Theme
        pg.setConfigOption('background', '#0d1117')
        pg.setConfigOption('foreground', '#c9d1d9')

        # Timer for control loop (50Hz)
        self.timer = QTimer()
        self.timer.timeout.connect(self.control_loop)
        self.timer.start(20) # 20ms = 50Hz

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header_layout = QHBoxLayout()
        header = QLabel("🛰️ GÖKBÖRÜ SOTM CONTROL CENTER")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: #58a6ff; margin-bottom: 10px;")
        header_layout.addWidget(header)
        header_layout.addStretch()
        
        version_label = QLabel("v1.2.0-ELITE")
        version_label.setStyleSheet("color: #8b949e; font-style: italic;")
        header_layout.addWidget(version_label)
        main_layout.addLayout(header_layout)
        
        # Top Panel: Info & Controls
        control_panel = QHBoxLayout()
        
        self.status_label = QLabel("🟢 SYSTEM STATE: ACTIVE | TARGET: TÜRKSAT 4B")
        self.status_label.setStyleSheet("color: #3fb950; font-weight: bold;")
        control_panel.addWidget(self.status_label)
        
        self.log_btn = QPushButton("Start Mission Logging")
        self.log_btn.clicked.connect(self.toggle_logging)
        control_panel.addWidget(self.log_btn)
        
        main_layout.addLayout(control_panel)
        
        # Mid Panel: Plots
        plot_layout = QHBoxLayout()
        
        # Platform Plot
        self.platform_plot = pg.PlotWidget(title="Platform Orientation (Roll/Pitch)")
        self.platform_plot.addLegend()
        self.platform_plot.showGrid(x=True, y=True, alpha=0.1)
        self.roll_curve = self.platform_plot.plot(pen=pg.mkPen('#f85149', width=2), name="Roll")
        self.pitch_curve = self.platform_plot.plot(pen=pg.mkPen('#58a6ff', width=2), name="Pitch")
        plot_layout.addWidget(self.platform_plot)
        
        # Tracking Error Plot
        self.error_plot = pg.PlotWidget(title="Tracking Error Analysis (Az/El)")
        self.error_plot.addLegend()
        self.error_plot.showGrid(x=True, y=True, alpha=0.1)
        self.az_error_curve = self.error_plot.plot(pen=pg.mkPen('#3fb950', width=2), name="Az Error")
        self.el_error_curve = self.error_plot.plot(pen=pg.mkPen('#d29922', width=2), name="El Error")
        plot_layout.addWidget(self.error_plot)
        
        main_layout.addLayout(plot_layout)
        
        # Data buffering
        self.ptr = 0
        self.buf_size = 500
        self.data_roll = np.zeros(self.buf_size)
        self.data_pitch = np.zeros(self.buf_size)
        self.data_az_err = np.zeros(self.buf_size)
        self.data_el_err = np.zeros(self.buf_size)

    def toggle_logging(self):
        if not self.logging_enabled:
            filename = f"mission_log_{int(time.time())}.csv"
            self.log_file = open(filename, 'w', newline='')
            self.csv_writer = csv.writer(self.log_file)
            # Expanded SoTM Header
            self.csv_writer.writerow([
                'timestamp', 'roll', 'pitch', 'yaw', 
                'actual_az', 'actual_el', 'target_az', 'target_el',
                'az_error', 'el_error'
            ])
            self.logging_enabled = True
            self.log_btn.setText("Stop Logging")
        else:
            self.logging_enabled = False
            self.log_file.close()
            self.log_btn.setText("Start Logging")

    def control_loop(self):
        # 1. Read Sensors
        roll_raw, pitch_raw, yaw = self.sensors.get_orientation()
        current_az = self.az_motor.get_angle()
        current_el = self.el_motor.get_angle()
        
        # 2. Run Stabilizer (returns state dict)
        state = self.stabilizer.update(roll_raw, pitch_raw, yaw, current_az, current_el, dt=0.02)
        
        # 3. Update Hardware
        self.hal.update_antenna(state["az_cmd"], state["el_cmd"])
        
        # 4. Logging
        if self.logging_enabled:
            self.csv_writer.writerow([
                time.time(), 
                state["roll"], state["pitch"], state["yaw"],
                state["actual_az"], state["actual_el"],
                state["target_az"], state["target_el"],
                state["az_error"], state["el_error"]
            ])
        
        # 5. Update UI
        self.update_plots(state["roll"], state["pitch"], state["az_error"], state["el_error"])

    def update_plots(self, roll, pitch, az_err, el_err):
        self.data_roll[:-1] = self.data_roll[1:]
        self.data_roll[-1] = roll
        self.data_pitch[:-1] = self.data_pitch[1:]
        self.data_pitch[-1] = pitch
        
        self.data_az_err[:-1] = self.data_az_err[1:]
        self.data_az_err[-1] = az_err
        self.data_el_err[:-1] = self.data_el_err[1:]
        self.data_el_err[-1] = el_err
        
        self.roll_curve.setData(self.data_roll)
        self.pitch_curve.setData(self.data_pitch)
        self.az_error_curve.setData(self.data_az_err)
        self.el_error_curve.setData(self.data_el_err)

def main():
    app = QApplication(sys.argv)
    window = SOTMDashboard()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
