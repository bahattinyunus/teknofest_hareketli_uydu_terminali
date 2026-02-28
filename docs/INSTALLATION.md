# 💻 GÖKBÖRÜ SOTM: Installation & Setup

Follow these steps to set up the development environment for the GÖKBÖRÜ Satcom on The Move system.

## 1. Prerequisites
- **Python 3.9+**
- **Git**

## 2. Environment Setup

### Windows
```powershell
# Clone the repository
git clone https://github.com/bahattinyunus/teknofest_hareketli_uydu_terminali
cd teknofest_hareketli_uydu_terminali

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Linux / MacOS
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 3. Running the System

### Quick Start (Windows)
Double-click `run.bat` or run:
```bash
python main.py
```

### Testing
To run the full test suite:
```bash
pytest tests/
```

## 4. Dependencies
The system relies on the following core libraries:
- `PyQt6` & `pyqtgraph`: Real-time GUI dashboard.
- `numpy`: Kinematic and matrix calculations.
- `pandas` & `matplotlib`: Mission logging and visual report analysis.
- `scipy`: PID gain optimization.

---
*GÖKBÖRÜ OTONOM SİSTEMLERİ*
