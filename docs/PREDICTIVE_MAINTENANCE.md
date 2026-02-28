# 🛠️ GÖKBÖRÜ SOTM: Predictive Maintenance

This document outlines the theoretical framework for the AI-driven predictive maintenance module designed for the SOTM terminal.

## 1. Vibration Analysis (FFT)
The system monitors IMU data to detect mechanical fatigue in the Stewart platform's actuators. By applying a Fast Fourier Transform (FFT) to the accelerometer Z-axis, we identify "Harmonic Resonance" patterns that correspond to gear wear.

### **Fatigue Detection Logic**
If the power spectral density (PSD) at the actuator's fundamental frequency exceeds a dynamically calculated threshold $\tau$:
$$PSD(f_{actuator}) > \tau \cdot \mu(PSD_{baseline})$$
An alert is triggered for "Actuator Degradation".

## 2. Thermal Drift Compensation
The SOTM terminal operates in extreme environments. We utilize a causal model to correlate motor temperature with torque efficiency.

$$\eta(T) = \eta_0 \cdot \exp(-\alpha (T - T_{ref}))$$

Where:
- $\eta$: Torque efficiency.
- $\alpha$: Thermal degradation coefficient.

## 3. Sensor Anomaly Detection
We use an **Isolation Forest** (Machine Learning) approach to detect sensor failures or "stuck-at" faults in real-time.

### **Features used for Anomaly Score:**
1. Kalman Filter Innovation Squared ($y_k^T S_k^{-1} y_k$)
2. PID Output Saturation Duration
3. Power Consumption Spikes

---
*GÖKBÖRÜ OTONOM SİSTEMLERİ - AI Engineering Division*
