import pytest
import numpy as np
from src.sensor_fusion import KalmanFilter

def test_kalman_initialization():
    kf = KalmanFilter(process_variance=0.1, measurement_variance=0.1)
    assert kf.x == 0.0
    assert kf.p == 1.0

def test_kalman_update():
    kf = KalmanFilter(process_variance=0.01, measurement_variance=0.1)
    
    # Simulate measurements with noise around 10.0
    measurements = [10.1, 9.9, 10.0, 10.2, 9.8]
    
    for m in measurements:
        kf.update(m)
        
    # Should converge towards 10.0
    assert abs(kf.x - 10.0) < 0.5
    # Uncertainty should decrease
    assert kf.p < 1.0

def test_kalman_noise_reduction():
    kf = KalmanFilter(process_variance=0.001, measurement_variance=1.0)
    
    raw_data = [5.0 + np.random.normal(0, 2) for _ in range(100)]
    filtered_data = []
    
    for d in raw_data:
        kf.update(d)
        filtered_data.append(kf.x)
        
    assert np.std(filtered_data) < np.std(raw_data)
