# 📐 GÖKBÖRÜ SOTM: Mathematical Theory

This document details the mathematical models and algorithms used in the GÖKBÖRÜ Satcom on The Move (SoTM) stabilization system.

## 1. 6-DOF Stewart Platform Kinematics

The terminal utilizes a 6-DOF Stewart platform for antenna stabilization. The inverse kinematics determine the length of each of the six actuators $L_i$ to achieve a desired platform orientation.

### **Inverse Kinematics Equation**
For each actuator $i \in \{1, ..., 6\}$:
$$L_i = \|\vec{P} + R \cdot \vec{p}_i - \vec{b}_i\|$$

Where:
- $\vec{P}$: Translation vector of the platform center.
- $R$: Rotation matrix (Roll $\phi$, Pitch $\theta$, Yaw $\psi$).
- $\vec{p}_i$: Coordinates of the $i$-th attachment point on the moving platform.
- $\vec{b}_i$: Coordinates of the $i$-th attachment point on the fixed base.

### **Rotation Matrix ($R$)**
We use the ZYX Euler sequence:
$$R = R_z(\psi) R_y(\theta) R_x(\phi)$$

## 2. Sensor Fusion: Extended Kalman Filter (EKF)

To eliminate IMU drift and sensor noise, an EKF is implemented to estimate the platform's state.

### **State Prediction**
$$\hat{x}_k = f(x_{k-1}, u_k) + w_k$$
$$P_k = F_k P_{k-1} F_k^T + Q_k$$

### **Measurement Update**
$$K_k = P_k H_k^T (H_k P_k H_k^T + R_k)^{-1}$$
$$x_k = \hat{x}_k + K_k (z_k - h(\hat{x}_k))$$
$$P_k = (I - K_k H_k) P_k$$

## 3. PID Control Discretization

The stabilization loop runs at 50Hz. The continuous PID controller is discretized using the backward Euler method.

### **Discrete PID Equation**
$$u(k) = K_p e(k) + K_i \sum_{j=0}^k e(j)\Delta t + K_d \frac{e(k) - e(k-1)}{\Delta t}$$

---
*GÖKBÖRÜ Engineering Division*
