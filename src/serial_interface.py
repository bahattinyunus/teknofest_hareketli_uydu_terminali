import serial
import time
import struct
from .telemetry import TelemetryPacket, TelemetryParser

class SOTMSerialInterface:
    """
    Hardware-in-the-Loop (HIL) Serial Interface.
    Communicates with the physical STM32 Microcontroller via UART (RS422/RS485).
    """
    def __init__(self, port="COM3", baudrate=115200, timeout=1.0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.parser = TelemetryParser()
        self.serial_conn = None

    def connect(self):
        try:
            self.serial_conn = serial.Serial(
                port=self.port, 
                baudrate=self.baudrate, 
                timeout=self.timeout
            )
            print(f"✅ Connected to STM32 HIL Controller on {self.port} at {self.baudrate} bps.")
            return True
        except serial.SerialException as e:
            print(f"❌ Failed to connect to {self.port}: {e}")
            return False

    def send_command(self, cmd_id: int, payload_bytes: bytes):
        """
        Sends a command to the STM32 (e.g., Target Az/El Update).
        Format: [SYNC][CMD_ID][PAYLOAD_LEN][PAYLOAD][CHECKSUM]
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            return False
            
        sync_word = b'\xAA\x55'
        length = len(payload_bytes)
        
        # Calculate XOR checksum
        checksum = cmd_id ^ length
        for b in payload_bytes:
            checksum ^= b
            
        packet = sync_word + struct.pack('<BB', cmd_id, length) + payload_bytes + struct.pack('<B', checksum)
        self.serial_conn.write(packet)
        return True

    def read_telemetry(self) -> TelemetryPacket:
        """
        Reads a full binary telemetry packet from the STM32.
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            return None
            
        # A real implementation would parse a sync-word stream. 
        # Here we assume the buffer aligns with our packet_size.
        if self.serial_conn.in_waiting >= self.parser.packet_size:
            raw_data = self.serial_conn.read(self.parser.packet_size)
            try:
                return self.parser.parse(raw_data)
            except Exception as e:
                print(f"⚠️ Serial Parse Error: {e}")
        return None

    def close(self):
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("Serial connection closed.")

if __name__ == "__main__":
    # Test stub
    interface = SOTMSerialInterface(port="COM3")
    if interface.connect():
        # Example: Requesting MCU to recalibrate IMU (Cmd ID 0x05)
        interface.send_command(0x05, b'\x01')
        time.sleep(1)
        interface.close()
