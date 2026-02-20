import math

def calculate_azimuth_elevation(obs_lat, obs_lon, obs_alt, sat_lat, sat_lon, sat_alt):
    """
    Calculates the Azimuth and Elevation from an observer to a satellite.
    
    Args:
        obs_lat, obs_lon: Observer's latitude and longitude in degrees.
        obs_alt: Observer's altitude in meters.
        sat_lat, sat_lon: Satellite's latitude and longitude in degrees.
        sat_alt: Satellite's altitude in meters.
        
    Returns:
        tuple: (Azimuth in degrees, Elevation in degrees, Slant Range in km)
    """
    # Earth radius in km
    R_earth = 6371.0

    # Convert to radians
    lat1 = math.radians(obs_lat)
    lon1 = math.radians(obs_lon)
    lat2 = math.radians(sat_lat)
    lon2 = math.radians(sat_lon)
    
    # Difference in coordinates
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Haversine formula for surface distance
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    surface_dist_km = R_earth * c
    
    # Approximate flat earth calculation for short ranges (typical for model satellites)
    # For high altitude balloons/model satellites, we can use simple trigonometry relative to local horizon
    
    # Relative position vector in local ENU (East-North-Up) coordinates
    # This is a simplified approximation suitable for visual line of sight within ~50km
    
    north_dist = (sat_lat - obs_lat) * 111139 # meters
    east_dist = (sat_lon - obs_lon) * 111139 * math.cos(lat1) # meters
    up_dist = sat_alt - obs_alt # meters
    
    # Azimuth calculation (0 is North, 90 is East)
    azimuth = math.degrees(math.atan2(east_dist, north_dist))
    if azimuth < 0:
        azimuth += 360
        
    # Elevation calculation
    ground_dist = math.sqrt(north_dist**2 + east_dist**2)
    elevation = math.degrees(math.atan2(up_dist, ground_dist))
    
    slant_range_km = math.sqrt(ground_dist**2 + up_dist**2) / 1000.0
    
    return azimuth, elevation, slant_range_km

if __name__ == "__main__":
    print("--- Antenna Pointing Calculator ---")
    
    # Example: Ground Station in Ankara, Satellite slightly offset
    gs_lat, gs_lon, gs_alt = 39.9255, 32.8662, 938 # Ankara
    sat_lat, sat_lon, sat_alt = 39.9300, 32.8700, 1500 # Slightly North-East, 1500m altitude
    
    print(f"Ground Station: {gs_lat}, {gs_lon}, {gs_alt}m")
    print(f"Satellite:      {sat_lat}, {sat_lon}, {sat_alt}m")
    
    az, el, dist = calculate_azimuth_elevation(gs_lat, gs_lon, gs_alt, sat_lat, sat_lon, sat_alt)
    
    print(f"\nPointing Solution:")
    print(f"  Azimuth:   {az:.2f} degrees")
    print(f"  Elevation: {el:.2f} degrees")
    print(f"  Range:     {dist:.3f} km")
