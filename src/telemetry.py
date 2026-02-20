import struct
from dataclasses import dataclass

@dataclass
class TelemetryPacket:
    team_id: int            # 2 bytes
    packet_count: int       # 2 bytes
    timestamp: float        # 4 bytes (Unix timestamp or ms)
    latitude: float         # 4 bytes
    longitude: float        # 4 bytes
    altitude: float         # 4 bytes
    pressure: float         # 4 bytes
    temperature: float      # 4 bytes
    battery_voltage: float  # 4 bytes
    state: int              # 1 byte (0: Wait, 1: Ascent, 2: Descent, 3: Landed)

class TelemetryParser:
    def __init__(self):
        # Format: < (Little Endian)
        # H (ushort) - Team ID
        # H (ushort) - Packet Count
        # f (float) - Timestamp
        # f (float) - Lat
        # f (float) - Lon
        # f (float) - Alt
        # f (float) - Pressure
        # f (float) - Temp
        # f (float) - Battery
        # B (uchar) - State
        self.format_string = '<HHfffffffB' 
        self.packet_size = struct.calcsize(self.format_string)

    def parse(self, data: bytes) -> TelemetryPacket:
        """
        Parses raw byte data into a TelemetryPacket.
        """
        if len(data) != self.packet_size:
            raise ValueError(f"Invalid data size. Expected {self.packet_size}, got {len(data)}")
        
        unpacked = struct.unpack(self.format_string, data)
        return TelemetryPacket(*unpacked)

    def serialize(self, packet: TelemetryPacket) -> bytes:
        """
        Serializes a TelemetryPacket into bytes.
        """
        return struct.pack(self.format_string, 
                           packet.team_id,
                           packet.packet_count,
                           packet.timestamp, 
                           packet.latitude, 
                           packet.longitude, 
                           packet.altitude,
                           packet.pressure,
                           packet.temperature,
                           packet.battery_voltage,
                           packet.state)

if __name__ == "__main__":
    # Test stub
    parser = TelemetryParser()
    # Team ID 123, Packet 1, Time 1000.0, Lat 39.9, Lon 32.8, Alt 100, Pres 1013, Temp 25, Batt 12.0, State 1
    test_packet = TelemetryPacket(123, 1, 1000.0, 39.9, 32.8, 100.0, 1013.25, 25.0, 12.0, 1)
    
    serialized = parser.serialize(test_packet)
    print(f"Serialized ({len(serialized)} bytes): {serialized.hex()}")
    
    parsed = parser.parse(serialized)
    print(f"Parsed: {parsed}")
