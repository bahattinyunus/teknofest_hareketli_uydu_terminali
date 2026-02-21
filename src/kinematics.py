import numpy as np

class SOTMKinematics:
    """
    Handles coordinate transformations for a Satellite Terminal on a moving Stewart Platform.
    Compensates for Roll, Pitch, and Yaw of the platform to maintain antenna boresight alignment.
    """
    
    def __init__(self):
        # Initial satellite orientation in a stable frame (NED or similar)
        self.target_az = 0.0
        self.target_el = 0.0
        
    def set_target_satellite(self, az, el):
        """Sets the fixed target satellite azimuth and elevation."""
        self.target_az = np.radians(az)
        self.target_el = np.radians(el)

    def get_antenna_angles(self, roll, pitch, yaw):
        """
        Calculates the required Azimuth and Elevation motor angles based on platform orientation.
        
        Args:
            roll (float): Platform roll in degrees.
            pitch (float): Platform pitch in degrees.
            yaw (float): Platform yaw in degrees.
            
        Returns:
            tuple: (required_az, required_el) in degrees for the motors.
        """
        r = np.radians(roll)
        p = np.radians(pitch)
        y = np.radians(yaw)
        
        # 1. Target vector in the Earth-Fixed Frame (NED)
        # Assuming R=1 (unit vector)
        # x_e = cos(el) * cos(az)
        # y_e = cos(el) * sin(az)
        # z_e = -sin(el)
        target_v_earth = np.array([
            np.cos(self.target_el) * np.cos(self.target_az),
            np.cos(self.target_el) * np.sin(self.target_az),
            -np.sin(self.target_el)
        ])
        
        # 2. Rotation matrices for Platform orientation (Earth to Body)
        # Z-Y-X rotation sequence (Yaw, Pitch, Roll)
        R_z = np.array([
            [np.cos(y), -np.sin(y), 0],
            [np.sin(y), np.cos(y), 0],
            [0, 0, 1]
        ])
        R_y = np.array([
            [np.cos(p), 0, np.sin(p)],
            [0, 1, 0],
            [-np.sin(p), 0, np.cos(p)]
        ])
        R_x = np.array([
            [1, 0, 0],
            [0, np.cos(r), -np.sin(r)],
            [0, np.sin(r), np.cos(r)]
        ])
        
        # Combined Body-to-Earth Matrix R = Rz * Ry * Rx
        # We need Earth-to-Body Matrix to find target in Antenna Body frame: R_inv = (R_z * R_y * R_x)^T
        R_eb = (R_z @ R_y @ R_x).T
        
        # 3. Target vector in the Platform (Body) Frame
        target_v_body = R_eb @ target_v_earth
        
        # 4. Extract required Azimuth and Elevation from Body Frame vector
        # x_b = cos(el_req) * cos(az_req)
        # y_b = cos(el_req) * sin(az_req)
        # z_b = -sin(el_req)
        
        x_b, y_b, z_b = target_v_body
        
        req_az = np.arctan2(y_b, x_b)
        req_el = -np.arcsin(z_b)
        
        # Normalize Azimuth to 0-360 range
        req_az_deg = np.degrees(req_az) % 360
        req_el_deg = np.degrees(req_el)
        
        return req_az_deg, req_el_deg

if __name__ == "__main__":
    # Simple test
    kin = SOTMKinematics()
    kin.set_target_satellite(180, 45) # South, 45 degrees elevation
    
    print("Stable Frame (0,0,0):", kin.get_antenna_angles(0, 0, 0))
    print("Roll +8 degrees:", kin.get_antenna_angles(8, 0, 0))
    print("Pitch +8 degrees:", kin.get_antenna_angles(0, 8, 0))
