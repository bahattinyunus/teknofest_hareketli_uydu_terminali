import struct
from dataclasses import dataclass

@dataclass
class TelemetryPacket:
    timestamp: float
    latitude: float
    longitude: float
    altitude: float
    status: int

class TelemetryParser:
    def __init__(self):
        # Example format: float, float, float, float, int (d, d, d, d, i)
        # Adjust struct format based on actual protocol
        self.format_string = '<ddddi' 
        self.packet_size = struct.calcsize(self.format_string)

    def parse(self, data: bytes) -> TelemetryPacket:
        """
        Parses raw byte data into a TelemetryPacket.
        
        Args:
            data (bytes): The raw data received from the satellite.
            
        Returns:
            TelemetryPacket: The parsed telemetry object.
        """
        if len(data) != self.packet_size:
            raise ValueError(f"Invalid data size. Expected {self.packet_size}, got {len(data)}")
        
        unpacked_data = struct.unpack(self.format_string, data)
        return TelemetryPacket(*unpacked_data)

    def serialize(self, packet: TelemetryPacket) -> bytes:
        """
        Serializes a TelemetryPacket into bytes.
        """
        return struct.pack(self.format_string, 
                           packet.timestamp, 
                           packet.latitude, 
                           packet.longitude, 
                           packet.altitude, 
                           packet.status)

if __name__ == "__main__":
    # Test stub
    parser = TelemetryParser()
    test_packet = TelemetryPacket(123456.78, 39.93, 32.85, 100.0, 1)
    serialized = parser.serialize(test_packet)
    print(f"Serialized: {serialized}")
    parsed = parser.parse(serialized)
    print(f"Parsed: {parsed}")
