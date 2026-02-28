import time
import numpy as np
import random
from src.telemetry import TelemetryPacket, TerminalState, UDPTemetrySender

class EWJammingSimulator:
    """
    Simulates an Electronic Warfare (EW) environment.
    Injects high-power RF noise (RSSI dropping) and GNSS Spoofing (sudden orientation jumps).
    """
    def __init__(self, target_ip="127.0.0.1", port=1923):
        self.sender = UDPTemetrySender(ip=target_ip, port=port)
        self.running = True
        self.packet_count = 0

    def generate_spoofed_telemetry(self, is_jammed=False, is_spoofed=False) -> TelemetryPacket:
        # Base healthy state
        roll = 2.0 * np.sin(self.packet_count / 10.0)
        pitch = 1.0 * np.cos(self.packet_count / 10.0)
        yaw = 180.0
        rssi = -45.0 + random.uniform(-2, 2)
        state = TerminalState.TRACKING
        
        # Apply EW Effects
        if is_jammed:
            # Ku-Band RF Jamming: Drastic drop in signal quality
            rssi = -110.0 + random.uniform(-5, 5)
            state = TerminalState.LOST
        
        if is_spoofed:
            # GNSS/IMU Spoofing: Sudden physically impossible angular jump
            roll += random.uniform(45.0, 90.0)
            pitch -= random.uniform(30.0, 60.0)
            
        target_az = 180.0
        target_el = 45.0
        
        # If tracking, target matches actual. If jammed, actual drifts.
        actual_az = target_az if not is_jammed else target_az + random.uniform(-10, 10)
        actual_el = target_el if not is_jammed else target_el + random.uniform(-10, 10)

        packet = TelemetryPacket(
            team_id=1923,
            packet_count=self.packet_count,
            timestamp=time.time(),
            roll=roll, pitch=pitch, yaw=yaw,
            actual_az=actual_az, actual_el=actual_el,
            target_az=target_az, target_el=target_el,
            rssi=rssi,
            state=state,
            checksum=0
        )
        self.packet_count += 1
        return packet

    def run_scenario(self):
        print("🛡️ GÖKBÖRÜ ELECTRONIC WARFARE (EW) SIMULATOR STARTED")
        print("Transmitting to UDP Ground Station. Ensure Listener is active.")
        print("-" * 60)
        
        try:
            print("[T+00s] Phase 1: Normal Operations (Clear Sky)")
            for _ in range(5):
                self.sender.send(self.generate_spoofed_telemetry())
                time.sleep(1)
                
            print("\n[T+05s] ⚠️ Phase 2: Hostile RF Ku-Band Jamming Detected!")
            print("Signal Loss Imminent. Switch to Inertial Dead-Reckoning.")
            for _ in range(5):
                self.sender.send(self.generate_spoofed_telemetry(is_jammed=True))
                time.sleep(1)
                
            print("\n[T+10s] 💥 Phase 3: Sophisticated GNSS/IMU Spoofing Attack!")
            print("Injecting false coordinate and high-delta orientation data.")
            for _ in range(5):
                self.sender.send(self.generate_spoofed_telemetry(is_jammed=True, is_spoofed=True))
                time.sleep(1)
                
            print("\n[T+15s] ✅ Phase 4: Jammer Evaded. Re-Acquiring Target.")
            for _ in range(5):
                self.sender.send(self.generate_spoofed_telemetry())
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\nSimulation aborted.")
        finally:
            self.sender.close()
            print("EW Simulation Complete.")

if __name__ == "__main__":
    sim = EWJammingSimulator()
    sim.run_scenario()
