# 🛡️ GÖKBÖRÜ SOTM: Electronic Warfare & Anti-Jamming

In the modern tactical battlefield, autonomous systems must survive highly contested electromagnetic environments (CEMA - Cyber Electromagnetic Activities). GÖKBÖRÜ integrates "God-Tier" resilience against **RF Jamming** and **GNSS/IMU Spoofing**.

## 1. GNSS & IMU Spoofing Rejection (Anti-Spoofing)

Adversaries often broadcast fake GPS signals to induce false coordinate locks, or use directed energy to temporarily blind IMUs, causing catastrophic orientation errors.

### **The Fix: Kinematic Plausibility Gates**
GÖKBÖRÜ's `SOTMSensorFusion` module implements a **Mahalanobis Distance** check within its Extended Kalman Filter. 
If a sudden change in Roll/Pitch ($\Delta \theta$) exceeds the physical capabilities of the vehicle's suspension system (e.g., > 15° per 20ms), the data packet is mathematically rejected as a **"Spoofed Injection"**. 

$$ \text{If } | \theta_{k} - \hat{\theta}_{k-1} | > \Theta_{max\_delta} \implies \text{Reject & Use Inertial Prediction} $$

## 2. RF Ku/Ka-Band Jamming Resilience

When an adversary floods the satellite downlink frequency with noise, the RSSI drops exponentially, leading to a loss of target lock.

### **The Fix: Autonomous Dead-Reckoning**
When $RSSI < RSSI_{threshold}$, the system switches from "Active Track" to **"Inertial Dead-Reckoning"**. 
1. The motors freeze tracking based on signal strength.
2. The internal Kalman Filter relies entirely on raw gyro integration to maintain the antenna pointing at the last known satellite coordinate relative to the vehicle's movement.
3. Once the vehicle drives out of the Jamming Zone, the system re-acquires the lock instantly, requiring zero searching parameters.

## 3. Simulating the Attack
You can test this cyber-resilience using the built-in Electronic Warfare simulator:
```bash
python analysis/simulations/ew_jammer.py
```
Monitor the output on the UDP Ground Station listener to observe the attack phases.

---
*GÖKBÖRÜ OTONOM SİSTEMLERİ - Electronic Warfare Division*
