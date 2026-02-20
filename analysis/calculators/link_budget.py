import math

def calculate_fspl(distance_km, frequency_mhz):
    """
    Calculates Free Space Path Loss (FSPL) in dB.
    """
    return 20 * math.log10(distance_km) + 20 * math.log10(frequency_mhz) + 32.44

def calculate_link_margin(tx_power_dbm, tx_gain_dbi, rx_gain_dbi, rx_sensitivity_dbm, distance_km, frequency_mhz, cable_loss_db=2.0):
    """
    Calculates the link margin.
    """
    fspl = calculate_fspl(distance_km, frequency_mhz)
    
    # EIRP = Tx Power + Tx Gain - Cable Loss
    eirp = tx_power_dbm + tx_gain_dbi - cable_loss_db
    
    # Received Power = EIRP + Rx Gain - FSPL
    rx_power = eirp + rx_gain_dbi - fspl
    
    # Link Margin = Received Power - Rx Sensitivity
    margin = rx_power - rx_sensitivity_dbm
    
    return margin, fspl, rx_power

if __name__ == "__main__":
    print("--- Link Budget Calculator ---")
    try:
        freq = float(input("Frequency (MHz): "))
        dist = float(input("Distance (km): "))
        tx_pwr = float(input("Tx Power (dBm): "))
        tx_gain = float(input("Tx Antenna Gain (dBi): "))
        rx_gain = float(input("Rx Antenna Gain (dBi): "))
        rx_sens = float(input("Rx Sensitivity (dBm): "))
        
        margin, fspl, rx_pwr = calculate_link_margin(tx_pwr, tx_gain, rx_gain, rx_sens, dist, freq)
        
        print(f"\nResults:")
        print(f"  FSPL: {fspl:.2f} dB")
        print(f"  Received Power: {rx_pwr:.2f} dBm")
        print(f"  Link Margin: {margin:.2f} dB")
        
        if margin > 0:
            print("  Status: LINK CLOSES (Good)")
        else:
            print("  Status: LINK FAILS (Insufficient Margin)")
            
    except ValueError:
        print("Invalid input. Please enter numeric values.")
