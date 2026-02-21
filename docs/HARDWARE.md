# 🛠️ GÖKBÖRÜ SOTM Hardware Specification

This document details the hardware components required to build the Satcom on The Move (SoTM) terminal, aligned with the Teknofest 2026 technical requirements.

## 1. Stabilization kaide (Gimbal)
| Component | Specification | Recommendation |
| :--- | :--- | :--- |
| **Azimuth Motor** | High-Torque BLDC with Encoder | AK80-6 or Maxon EC-4pole |
| **Elevation Motor** | Hollow-Shaft BLDC / Servo | Maxon EC-max or Dynamixel XM540 |
| **Bearings** | Thin-section Kayar Rulman | Silverthin SA020 |
| **Slip Ring** | 360° Continuous (RF + Power) | Senring SNM012 |

## 2. Sensors & Intelligence
| Component | Specification | Recommendation |
| :--- | :--- | :--- |
| **Main Controller** | ARM Cortex-M7 (Real-time) | STM32H743VIT6 |
| **IMU / Gyro** | High-Stability 9-Axis | Bosch BNO055 or Xsens MTI-1 |
| **GPS** | Multi-GNSS + RTK | u-blox ZED-F9P |

## 3. Communication & RF
| Component | Specification | Recommendation |
| :--- | :--- | :--- |
| **Antenna** | 45cm Parabolic Offset | Industrial Grade Ku-Band |
| **LNB / BUC** | Ku-band Universal | Norsat / Wavestream |
| **Laser Module** | 5mW Red (Simulation Target) | Standard 650nm Module |

## 4. Power System
| Component | Specification | Recommendation |
| :--- | :--- | :--- |
| **DC-DC Converter** | 5V-36V Universal | Vicor or MeanWell |
| **Battery (Optional)** | 6S LiPo / LiFePO4 | 5000mAh for Field Ops |

---
> [!NOTE]
> All components must be selected to keep the total system weight below **20kg** as per Section 2.8 of the specification.
