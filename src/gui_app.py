import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QComboBox
from PyQt6.QtCore import QTimer
import pyqtgraph as pg

from .stabilization import SOTMStabilizer
from .simulated_hardware import SimulatedMotor, SimulatedSensors
from .hardware_interface import HardwareAbstrationLayer

class SOTMDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GÖKBÖRÜ SOTM Control Station")
        self.resize(1000, 700)
        
        # Core Components
        self.sensors = SimulatedSensors()
        self.az_motor = SimulatedMotor(initial_angle=180.0)
        self.el_motor = SimulatedMotor(initial_angle=30.0)
        self.hal = HardwareAbstrationLayer(self.az_motor, self.el_motor, self.sensors)
        self.stabilizer = SOTMStabilizer(target_az=180.0, target_el=30.0)
        
        self.init_ui()
        
        # Timer for control loop (50Hz)
        self.timer = QTimer()
        self.timer.timeout.connect(self.control_loop)
        self.timer.start(20) # 20ms = 50Hz

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header = QLabel("🛰️ SOTM Stabilization Dashboard")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        main_layout.addWidget(header)
        
        # Top Panel: Info & Controls
        control_panel = QHBoxLayout()
        
        self.status_label = QLabel("Mode: AUTO | Target: Türksat 4B")
        control_panel.addWidget(self.status_label)
        
        toggle_btn = QPushButton("Toggle Manual/Auto")
        control_panel.addWidget(toggle_btn)
        
        main_layout.addLayout(control_panel)
        
        # Mid Panel: Plots
        plot_layout = QHBoxLayout()
        
        # Platform Plot
        self.platform_plot = pg.PlotWidget(title="Platform Orientation (Roll/Pitch)")
        self.platform_plot.addLegend()
        self.roll_curve = self.platform_plot.plot(pen='r', name="Roll")
        self.pitch_curve = self.platform_plot.plot(pen='b', name="Pitch")
        plot_layout.addWidget(self.platform_plot)
        
        # Tracking Error Plot
        self.error_plot = pg.PlotWidget(title="Tracking Error (Az/El)")
        self.error_plot.addLegend()
        self.az_error_curve = self.error_plot.plot(pen='g', name="Az Error")
        self.el_error_curve = self.error_plot.plot(pen='y', name="El Error")
        plot_layout.addWidget(self.error_plot)
        
        main_layout.addLayout(plot_layout)
        
        # Data buffering
        self.ptr = 0
        self.buf_size = 500
        self.data_roll = np.zeros(self.buf_size)
        self.data_pitch = np.zeros(self.buf_size)
        self.data_az_err = np.zeros(self.buf_size)
        self.data_el_err = np.zeros(self.buf_size)

    def control_loop(self):
        # 1. Read Sensors
        roll, pitch, yaw = self.sensors.get_orientation()
        current_az = self.az_motor.get_angle()
        current_el = self.el_motor.get_angle()
        
        # 2. Run Stabilizer
        az_cmd, el_cmd = self.stabilizer.update(roll, pitch, yaw, current_az, current_el)
        
        # 3. Update Hardware
        self.hal.update_antenna(az_cmd, el_cmd)
        
        # 4. Update UI
        self.update_plots(roll, pitch, az_cmd, el_cmd)

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
