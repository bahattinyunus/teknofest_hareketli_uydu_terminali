import numpy as np

def calculate_link_budget(frequency_ghz, distance_km, tx_power_dbm, tx_gain_dbi, rx_gain_dbi, loss_db=2.0):
    """
    Calculates the Link Budget using the Friis Transmission Equation.
    
    Args:
        frequency_ghz: Carrier frequency (e.g., 12.5 for Ku-band)
        distance_km: Distance to satellite (e.g., 35786 for GEO)
        tx_power_dbm: Terminal transmit power
        tx_gain_dbi: Terminal antenna gain
        rx_gain_dbi: Satellite antenna gain
        loss_db: Atmospheric and cable losses
        
    Returns:
        dict: RSSI (Received Signal Strength) and Margin
    """
    # 1. Free Space Path Loss (FSPL)
    # FSPL = 20*log10(d) + 20*log10(f) + 92.45
    fspl = 20 * np.log10(distance_km) + 20 * np.log10(frequency_ghz) + 92.45
    
    # 2. Received Power (Pr)
    pr = tx_power_dbm + tx_gain_dbi + rx_gain_dbi - fspl - loss_db
    
    return {
        "Frequency (GHz)": frequency_ghz,
        "FSPL (dB)": fspl,
        "Received Power (dBm)": pr,
        "Status": "Link OK" if pr > -120 else "Link Failure"
    }

if __name__ == "__main__":
    print("--- GÖKBÖRÜ SOTM Link Budget Pro ---")
    # Example for Ku-Band Satellite Link (GEO)
    result = calculate_link_budget(
        frequency_ghz=12.5, 
        distance_km=36000, 
        tx_power_dbm=40,   # 10W
        tx_gain_dbi=35,    # 45cm Dish
        rx_gain_dbi=30     # Satellite RX
    )
    for k, v in result.items():
        if isinstance(v, float):
            print(f"{k}: {v:.2f}")
        else:
            print(f"{k}: {v}")
