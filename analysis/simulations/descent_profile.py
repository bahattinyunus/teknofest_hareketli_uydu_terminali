import numpy as np
import matplotlib.pyplot as plt

def simulate_descent(initial_alt, mass, param_Cd, area, dt=0.1):
    """
    Simulates the descent of the payload.
    """
    g = 9.81
    rho = 1.225 # Air density (simplified constant)
    
    heights = [initial_alt]
    velocities = [0]
    times = [0]
    
    curr_h = initial_alt
    curr_v = 0 # Downward is positive
    t = 0
    
    while curr_h > 0:
        # Drag force: Fd = 0.5 * rho * v^2 * Cd * A
        F_drag = 0.5 * rho * (curr_v**2) * param_Cd * area
        
        # Net force: F_net = Weight - Drag
        F_net = (mass * g) - F_drag
        
        # Acceleration
        a = F_net / mass
        
        # Update state
        curr_v += a * dt
        curr_h -= curr_v * dt
        t += dt
        
        heights.append(max(0, curr_h))
        velocities.append(curr_v)
        times.append(t)
        
    return times, heights, velocities

if __name__ == "__main__":
    print("--- Descent Profile Simulation ---")
    
    times, heights, velocities = simulate_descent(initial_alt=500, mass=1.0, param_Cd=1.5, area=0.5)
    
    try:
        plt.figure(figsize=(10, 6))
        
        plt.subplot(2, 1, 1)
        plt.plot(times, heights, 'b-')
        plt.title('Altitude vs Time')
        plt.ylabel('Altitude (m)')
        plt.grid(True)
        
        plt.subplot(2, 1, 2)
        plt.plot(times, velocities, 'r-')
        plt.title('Descent Velocity vs Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity (m/s)')
        plt.grid(True)
        
        output_file = "descent_profile.png"
        plt.tight_layout()
        plt.savefig(output_file)
        print(f"Simulation complete. Graph saved to {output_file}")
        
    except Exception as e:
        print(f"Could not generate plot (matplotlib might be missing or headless): {e}")
