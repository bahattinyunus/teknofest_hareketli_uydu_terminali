import pytest
import numpy as np
from src.kinematics import SOTMKinematics

def test_static_pointing():
    kin = SOTMKinematics()
    kin.set_target_satellite(180, 45)
    az, el = kin.get_antenna_angles(0, 0, 0)
    assert pytest.approx(az, 0.1) == 180.0
    assert pytest.approx(el, 0.1) == 45.0

def test_roll_compensation():
    kin = SOTMKinematics()
    kin.set_target_satellite(0, 90) # Zenith
    # If platform rolls 10 degrees, antenna must roll -10 relative to platform
    # to stay pointed at Zenith
    az, el = kin.get_antenna_angles(10, 0, 0)
    # At zenith, az is ambiguous, but el should be 80 relative to body frame
    assert pytest.approx(el, 0.5) == 80.0

def test_azimuth_wrapping():
    kin = SOTMKinematics()
    kin.set_target_satellite(350, 0)
    # Yaw 20 degrees right -> Target should move to 330 in body frame
    az, el = kin.get_antenna_angles(0, 0, 20)
    assert pytest.approx(az, 0.1) == 330.0
