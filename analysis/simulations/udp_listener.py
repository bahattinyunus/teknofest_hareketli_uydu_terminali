import socket
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.telemetry import TelemetryParser, TerminalState

def run_listener(ip="0.0.0.0", port=1923):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    parser = TelemetryParser()
    
    print(f"📡 GÖKBÖRÜ Ground Station UDP Listener started on UDP {port}...")
    print("Waiting for telemetry stream (Press Ctrl+C to stop)...\n")
    print(f"{'PKT#':<6} | {'TIME':<10} | {'ROLL':<6} | {'PITCH':<6} | {'AZ_ERR':<8} | {'EL_ERR':<8} | {'RSSI':<6} | {'STATE':<10}")
    print("-" * 85)

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            try:
                packet = parser.parse(data)
                az_err = packet.target_az - packet.actual_az
                el_err = packet.target_el - packet.actual_el
                state_str = TerminalState(packet.state).name
                
                print(f"#{packet.packet_count:<4} | {packet.timestamp:<10.2f} | "
                      f"{packet.roll:<6.2f} | {packet.pitch:<6.2f} | "
                      f"{az_err:<8.3f} | {el_err:<8.3f} | "
                      f"{packet.rssi:<6.1f} | {state_str:<10}")
            except Exception as e:
                print(f"Error parsing packet from {addr}: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Listener stopped by user.")
    finally:
        sock.close()

if __name__ == "__main__":
    run_listener()
