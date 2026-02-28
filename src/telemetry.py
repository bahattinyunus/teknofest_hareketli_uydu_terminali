import struct
from dataclasses import dataclass
from enum import IntEnum

class TerminalState(IntEnum):
    SEARCHING = 0
    TRACKING = 1
    LOST = 2
    STOWED = 3

@dataclass
class TelemetryPacket:
    team_id: int            # 2 bytes (H)
    packet_count: int       # 2 bytes (H)
    timestamp: float        # 4 bytes (f)
    
    # Platform Orientation
    roll: float             # 4 bytes (f)
    pitch: float            # 4 bytes (f)
    yaw: float              # 4 bytes (f)
    
    # Antenna State
    actual_az: float        # 4 bytes (f)
    actual_el: float        # 4 bytes (f)
    target_az: float        # 4 bytes (f)
    target_el: float        # 4 bytes (f)
    
    # Performance
    rssi: float             # 4 bytes (f)
    state: int              # 1 byte  (B)
    checksum: int           # 1 byte  (B)

class TelemetryParser:
    def __init__(self):
        # Format: < (Little Endian)
        # H H f - Header (Team, Count, Time)
        # f f f - Orientation
        # f f f f - Antenna
        # f B B - System (RSSI, State, Checksum)
        self.format_string = '<HHf fff ffff fBB' 
        self.packet_size = struct.calcsize(self.format_string)

    def calculate_checksum(self, data_bytes: bytes) -> int:
        """Simple XOR checksum for the packet."""
        checksum = 0
        for b in data_bytes:
            checksum ^= b
        return checksum & 0xFF

    def parse(self, data: bytes) -> TelemetryPacket:
        """
        Parses raw byte data into a TelemetryPacket.
        """
        if len(data) != self.packet_size:
            raise ValueError(f"Invalid data size. Expected {self.packet_size}, got {len(data)}")
        
        # Verify checksum (last byte)
        received_checksum = data[-1]
        calculated = self.calculate_checksum(data[:-1])
        if received_checksum != calculated:
            print(f"Warning: Checksum mismatch! Recv: {received_checksum}, Calc: {calculated}")
        
        unpacked = struct.unpack(self.format_string, data)
        # The fields match the dataclass order
        return TelemetryPacket(*unpacked)

    def serialize(self, packet: TelemetryPacket) -> bytes:
        """
        Serializes a TelemetryPacket into bytes and adds checksum.
        """
        # Exclude checksum field from packing, we calculate it after
        raw_data = struct.pack('<HHf fff ffff fB', 
                            packet.team_id,
                            packet.packet_count,
                            packet.timestamp, 
                            packet.roll, 
                            packet.pitch, 
                            packet.yaw,
                            packet.actual_az,
                            packet.actual_el,
                            packet.target_az,
                            packet.target_el,
                            packet.rssi,
                            packet.state)
        
        checksum = self.calculate_checksum(raw_data)
        return raw_data + struct.pack('B', checksum)

class UDPTemetrySender:
    """
    Sends serialized TelemetryPacket data over UDP to a Ground Station.
    """
    def __init__(self, ip="127.0.0.1", port=1923):
        import socket
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.parser = TelemetryParser()

    def send(self, packet: TelemetryPacket):
        try:
            data = self.parser.serialize(packet)
            self.sock.sendto(data, (self.ip, self.port))
        except Exception as e:
            print(f"UDP Send Error: {e}")

    def close(self):
        self.sock.close()

if __name__ == "__main__":
    import time
    # Test stub for UDP Telemetry
    sender = UDPTemetrySender()
    
    print(f"Sending test packets to {sender.ip}:{sender.port}...")
    for i in range(5):
        test_packet = TelemetryPacket(
            team_id=1923, 
            packet_count=i, 
            timestamp=time.time(),
            roll=2.5, pitch=-1.2, yaw=180.0,
            actual_az=180.5, actual_el=35.2,
            target_az=180.0, target_el=35.0,
            rssi=-65.4,
            state=TerminalState.TRACKING,
            checksum=0 
        )
        sender.send(test_packet)
        print(f"Sent Packet #{i}")
        time.sleep(1)
    sender.close()
