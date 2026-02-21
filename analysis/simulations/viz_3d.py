import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

class SOTMVisualizer3D:
    """
    Renders a 3D visualization of the SOTM terminal and its platform.
    Useful for debugging kinematics and spatial orientation.
    """
    def __init__(self):
        self.fig = plt.figure(figsize=(12, 9), facecolor='#0b0d17')
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_facecolor('#0b0d17')
        
        # Colors & Styling
        self.ax.set_xlim([-1.5, 1.5]); self.ax.set_ylim([-1.5, 1.5]); self.ax.set_zlim([0, 3])
        self.ax.set_title("GÖKBÖRÜ SOTM - Advanced 3D Dynamics", color='white', fontsize=16, fontweight='bold')
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
        
        # 3. Satellite Beam (Laser) - Extend to a distant point
        beam_end = origin + (v_earth * 2.5)
        self.beam_line.set_data([tip[0], beam_end[0]], [tip[1], beam_end[1]])
        self.beam_line.set_3d_properties([tip[2], beam_end[2]])
        
        return self.platform_line, self.antenna_line, self.beam_line, *self.legs

def run_demo():
    viz = SOTMVisualizer3D()
    def animate(i):
        t = i / 10.0
        # Scenario: Platform hitting a bumpy road (High-frequency Roll/Pitch)
        roll = 8 * np.sin(t) + 2 * np.sin(t * 3)
        pitch = 8 * np.cos(t * 0.8) + 2 * np.cos(t * 2.5)
        
        # The stabilizer tries to keep it pointing North (Az=0) and Up (El=45)
        # We simulate the PERFECT stabilization result (compensation)
        return viz.update(roll, pitch, 0, 45)

    ani = FuncAnimation(viz.fig, animate, frames=300, interval=30, blit=True)
    plt.show()

if __name__ == "__main__":
    run_demo()
