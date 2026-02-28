import pytest
import numpy as np
from src.stabilization import SOTMStabilizer

def test_stabilizer_error_calculation():
    stabilizer = SOTMStabilizer(target_az=180.0, target_el=45.0)
    
    # No motion, at target
    state = stabilizer.update(roll_raw=0, pitch_raw=0, yaw=0, feedback_az=180.0, feedback_el=45.0, dt=0.02)
    assert abs(state["az_error"]) < 0.1
    assert abs(state["el_error"]) < 0.1

def test_stabilizer_re_pointing():
    stabilizer = SOTMStabilizer(target_az=180.0, target_el=45.0)
    
    # Change target
    stabilizer.kinematics.set_target_satellite(az=90.0, el=30.0)
    assert stabilizer.kinematics.target_az == pytest.approx(np.radians(90.0))
    assert stabilizer.kinematics.target_el == pytest.approx(np.radians(30.0))

def test_stabilizer_pid_clamping():
    stabilizer = SOTMStabilizer()
    # Mock large error to trigger clamping if implemented (check source)
    # This is a placeholder for checking logic consistency
    state = stabilizer.update(roll_raw=20, pitch_raw=20, yaw=0, feedback_az=0, feedback_el=0, dt=0.02)
    assert "az_cmd" in state
    assert "el_cmd" in state
