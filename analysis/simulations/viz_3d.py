import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import socket
import threading
import sys
import os

# Append src to path so telemetry can be imported independently
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.telemetry import TelemetryParser, TelemetryPacket

class SOTMVisualizer3D:
    """
    Renders a 3D Digital Twin of the SOTM terminal.
    Can be run in Math-Simulation mode or Live-UDP (Digital Twin) mode.
    """
    def __init__(self, mode="simulation"):
        self.mode = mode
        self.fig = plt.figure(figsize=(12, 9), facecolor='#0b0d17')
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_facecolor('#0b0d17')
        
        # Latest telemetry state for Digital Twin Mode
        self.latest_roll = 0.0
        self.latest_pitch = 0.0
        self.latest_az = 0.0
        self.latest_el = 45.0
        
        # Colors & Styling
        self.ax.set_xlim([-1.5, 1.5]); self.ax.set_ylim([-1.5, 1.5]); self.ax.set_zlim([0, 3])
        title = "GÖKBÖRÜ SOTM - Live Digital Twin" if mode == "live" else "GÖKBÖRÜ SOTM - Simulation"
        self.ax.set_title(title, color='#00d4ff' if mode == "live" else 'white', fontsize=16, fontweight='bold')
        self.ax.grid(False)
        self.ax.xaxis.pane.fill = self.ax.yaxis.pane.fill = self.ax.zaxis.pane.fill = False
        self.ax.view_init(elev=20, azim=45)

        # Ground Plane (Grid)
        xx, yy = np.meshgrid(np.linspace(-1.5, 1.5, 10), np.linspace(-1.5, 1.5, 10))
        zz = np.zeros_like(xx)
        self.ax.plot_wireframe(xx, yy, zz, color='#1f2d3d', alpha=0.3, lw=0.5)

        # Platform base components
        self.platform_line, = self.ax.plot([], [], [], color='#00d4ff', lw=3, label="Active Platform")
        self.legs = [self.ax.plot([], [], [], color='#4a5568', lw=1, alpha=0.6)[0] for _ in range(3)]
        
        # Antenna components
        self.antenna_line, = self.ax.plot([], [], [], color='#ffcc00', lw=4, label="Antenna Body")
        self.beam_line, = self.ax.plot([], [], [], color='#ff3366', lw=1.5, alpha=0.8, label="Satellite Beam")
        
        # Tracking satellite point
        self.sat_point, = self.ax.plot([0], [0], [2.5], 'w*', markersize=10, label="Target Satellite")
        
        self.ax.legend(facecolor='#1a202c', edgecolor='none', labelcolor='white')

        if self.mode == "live":
            self.start_udp_listener()

    def start_udp_listener(self):
        """Runs a background thread to listen to port 1923 for real telemetry."""
        self.parser = TelemetryParser()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind to all interfaces, port 1923
        self.sock.bind(('0.0.0.0', 1923))
        self.listener_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listener_thread.start()
        print("📡 Listener Thread Bound to UDP Port 1923. Waiting for Telemetry...")

    def _listen_loop(self):
        while True:
            try:
                data, _ = self.sock.recvfrom(1024)
                if len(data) >= self.parser.packet_size:
                    packet = self.parser.parse(data)
                    # Update thread-safe variables
                    self.latest_roll = packet.roll
                    self.latest_pitch = packet.pitch
                    self.latest_az = packet.actual_az
                    self.latest_el = packet.actual_el
            except Exception as e:
                pass

    def update(self, roll, pitch, az, el):
        r, p = np.radians(roll), np.radians(pitch)
        a, e = np.radians(az), np.radians(el)
        
        # 1. Base corner points (Stewart Layout)
        base_fixed = np.array([[0.6, 0, 0], [-0.3, 0.52, 0], [-0.3, -0.52, 0], [0.6, 0, 0]])
        
        # Rotation matrices
        Rx = np.array([[1,0,0], [0, np.cos(r), -np.sin(r)], [0, np.sin(r), np.cos(r)]])
        Ry = np.array([[np.cos(p), 0, np.sin(p)], [0,1,0], [-np.sin(p), 0, np.cos(p)]])
        R = Ry @ Rx
        
        tilted_base = (R @ base_fixed.T).T + np.array([0, 0, 0.4]) # Lift from ground
        self.platform_line.set_data(tilted_base[:, 0], tilted_base[:, 1])
        self.platform_line.set_3d_properties(tilted_base[:, 2])
        
        # Draw 'legs' connecting to ground
        for i in range(3):
            self.legs[i].set_data([base_fixed[i,0], tilted_base[i,0]], [base_fixed[i,1], tilted_base[i,1]])
            self.legs[i].set_3d_properties([0, tilted_base[i,2]])

        # 2. Antenna Boresight
        origin = np.mean(tilted_base[:-1], axis=0) + (R @ np.array([0, 0, 0.1]))
        
        v_body = np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])
        v_earth = R @ v_body
        
        tip = origin + (v_earth * 0.6)
        
        self.antenna_line.set_data([origin[0], tip[0]], [origin[1], tip[1]])
        self.antenna_line.set_3d_properties([origin[2], tip[2]])
        
        # 3. Satellite Beam (Laser)
        beam_end = origin + (v_earth * 2.5)
        self.beam_line.set_data([tip[0], beam_end[0]], [tip[1], beam_end[1]])
        self.beam_line.set_3d_properties([tip[2], beam_end[2]])
        
        return self.platform_line, self.antenna_line, self.beam_line, *self.legs

    def animate(self, i):
        if self.mode == "live":
            # Real telemetry overrides math
            return self.update(self.latest_roll, self.latest_pitch, self.latest_az, self.latest_el)
        else:
            # Standalone Simulation Scenario
            t = i / 10.0
            roll = 8 * np.sin(t) + 2 * np.sin(t * 3)
            pitch = 8 * np.cos(t * 0.8) + 2 * np.cos(t * 2.5)
            # Simulating PERFECT stabilization (antenna fixed at Az=0, El=45)
            return self.update(roll, pitch, 0, 45)

def run_demo(mode="simulation"):
    print(f"Launching 3D Visualizer in {mode.upper()} mode...")
    viz = SOTMVisualizer3D(mode=mode)
    ani = FuncAnimation(viz.fig, viz.animate, frames=300, interval=30, blit=True)
    plt.show()

if __name__ == "__main__":
    import sys
    mode = "live" if "--live" in sys.argv else "simulation"
    run_demo(mode)
