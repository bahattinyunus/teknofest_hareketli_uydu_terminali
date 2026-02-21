import pandas as pd
import time
import threading
from .telemetry import TelemetryPacket, TerminalState

class MissionReplayer:
    """
    Replays mission log data into the system, simulating real-time telemetry inflow.
    """
    def __init__(self, callback):
        self.callback = callback # Function to call with each replayed point
        self.is_playing = False
        self.thread = None

    def load_csv(self, file_path):
        try:
            self.data = pd.read_csv(file_path)
            print(f"✅ Loaded {len(self.data)} points from {file_path}")
            return True
        except Exception as e:
            print(f"❌ Error loading log: {e}")
            return False

    def start(self, speed=1.0):
        if self.is_playing: return
        self.is_playing = True
        self.thread = threading.Thread(target=self._run_replay, args=(speed,))
        self.thread.start()

    def stop(self):
        self.is_playing = False
        if self.thread:
            self.thread.join()

    def _run_replay(self, speed):
        last_time = None
        for index, row in self.data.iterrows():
            if not self.is_playing: break
            
            # Simulate timing
            current_log_time = row['timestamp']
            if last_time is not None:
                delay = (current_log_time - last_time) / speed
                if delay > 0: time.sleep(delay)
            
            last_time = current_log_time
            
            # Construct a state-like dictionary compatible with GUI/Visualizer
            state = {
                "roll": row.get('roll', 0),
                "pitch": row.get('pitch', 0),
                "yaw": row.get('yaw', 0),
                "actual_az": row.get('actual_az', 180),
                "actual_el": row.get('actual_el', 30),
                "target_az": row.get('target_az', 180),
                "target_el": row.get('target_el', 30),
                "az_error": row.get('az_error', 0),
                "el_error": row.get('el_error', 0),
                "az_cmd": 0, "el_cmd": 0 # Not relevant for replay
            }
            
            self.callback(state)

if __name__ == "__main__":
    # Test stub: Simple print callback
    def mock_ui_update(state):
        print(f"Replay Time: {time.time()} | Az Err: {state['az_error']:.4f}")

    replayer = MissionReplayer(mock_ui_update)
    # This would require an existing CSV log to test properly in a real run
    print("Replayer initialized. Usage: load a CSV and call start().")
