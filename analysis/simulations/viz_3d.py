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
        self.fig = plt.figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim([-1, 1]); self.ax.set_ylim([-1, 1]); self.ax.set_zlim([0, 2])
        self.ax.set_title("GÖKBÖRÜ SOTM 3D Simulator")
        
        # Base platform (Stewart Base)
        self.platform_line, = self.ax.plot([], [], [], 'k-', lw=2, label="Stewart Base")
        
        # Antenna vector (Boresight)
        self.antenna_line, = self.ax.plot([], [], [], 'r-o', lw=3, label="Antenna Boresight")
        
        self.ax.legend()

    def update(self, roll, pitch, az, el):
        """
        Updates the 3D scene.
        az, el: Antenna angles relative to the platform.
        """
        r = np.radians(roll)
        p = np.radians(pitch)
        a = np.radians(az)
        e = np.radians(el)
        
        # 1. Base corner points (simplified triangle)
        base_points = np.array([
            [0.5, 0, 0],
            [-0.25, 0.43, 0],
            [-0.25, -0.43, 0],
            [0.5, 0, 0] # Loop back
        ])
        
        # Rotation matrices for platform tilt
        Rx = np.array([[1,0,0], [0, np.cos(r), -np.sin(r)], [0, np.sin(r), np.cos(r)]])
        Ry = np.array([[np.cos(p), 0, np.sin(p)], [0,1,0], [-np.sin(p), 0, np.cos(p)]])
        R = Ry @ Rx
        
        tilted_base = (R @ base_points.T).T
        self.platform_line.set_data(tilted_base[:, 0], tilted_base[:, 1])
        self.platform_line.set_3d_properties(tilted_base[:, 2])
        
        # 2. Antenna Boresight Vector
        # Origin is center of tilted platform
        origin = np.mean(tilted_base[:-1], axis=0) + np.array([0, 0, 0.2]) # Slightly above base
        
        # Vector points in az/el relative to platform Body frame
        # We need to rotate this body-frame vector by platform R to get in Earth frame
        v_body = np.array([
            np.cos(e) * np.cos(a),
            np.cos(e) * np.sin(a),
            np.sin(e)
        ])
        v_earth = R @ v_body
        
        tip = origin + (v_earth * 0.8) # 0.8 scale
        
        self.antenna_line.set_data([origin[0], tip[0]], [origin[1], tip[1]])
        self.antenna_line.set_3d_properties([origin[2], tip[2]])
        
        return self.platform_line, self.antenna_line

def run_demo():
    viz = SOTMVisualizer3D()
    def animate(i):
        roll = 8 * np.sin(i / 10.0)
        pitch = 8 * np.cos(i / 10.0)
        # Assuming stabilization keeps it pointing "Up" in Earth frame
        # So in Body frame it compensates for roll/pitch
        return viz.update(roll, pitch, 0, 90)

    ani = FuncAnimation(viz.fig, animate, frames=200, interval=50, blit=True)
    plt.show()

if __name__ == "__main__":
    run_demo()
