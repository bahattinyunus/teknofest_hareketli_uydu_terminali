import math

def calculate_parachute_diameter(mass, descent_rate, drag_coefficient=1.5, air_density=1.225):
    """
    Calculates the required parachute diameter for a given mass and descent rate.

    Args:
        mass (float): Mass of the payload in kg.
        descent_rate (float): Desired descent rate in m/s.
        drag_coefficient (float): Drag coefficient of the parachute (default 1.5 for flat circular).
        air_density (float): Air density in kg/m^3 (default 1.225 at sea level).

    Returns:
        float: Required diameter in meters.
    """
    area = (2 * mass * 9.81) / (air_density * drag_coefficient * descent_rate**2)
    diameter = math.sqrt(4 * area / math.pi)
    return diameter

if __name__ == "__main__":
    print("--- Parachute Sizing Calculator ---")
    try:
        mass = float(input("Enter payload mass (kg): "))
        descent_rate = float(input("Enter desired descent rate (m/s): "))
        
        diameter = calculate_parachute_diameter(mass, descent_rate)
        
        print(f"\nResults:")
        print(f"  Payload Mass: {mass} kg")
        print(f"  Descent Rate: {descent_rate} m/s")
        print(f"  Required Parachute Diameter: {diameter:.2f} meters")
        
    except ValueError:
        print("Invalid input. Please enter numeric values.")
