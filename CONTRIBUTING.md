# 🤝 Contributing to GÖKBÖRÜ SOTM

Thank you for your interest in contributing to the **GÖKBÖRÜ Satcom on The Move (SoTM)** project. We operate at an elite engineering standard, and we value contributions that push the boundaries of autonomous systems and control theory.

## 🚀 How to Contribute

### 1. Find or Create an Issue
Before writing code, please check existing issues to avoid duplicating work. If you have a new idea, open an issue using the provided templates (Bug Report or Feature Request) to discuss it with the team.

### 2. Fork & Branch
1. Fork the repository on GitHub.
2. Clone your fork locally.
3. Create a feature branch matching your goal:
   ```bash
   git checkout -b feature/ekf-optimization
   ```
   *Prefixes: `feature/`, `bugfix/`, `docs/`, `refactor/`*

### 3. Setup Your Environment
We highly recommend using Docker to ensure reproducibility:
```bash
docker-compose up sotm-test
```
Alternatively, follow the `docs/INSTALLATION.md` for local setup.

### 4. Code Standards
- **Python Quality:** Ensure your code is PEP8 compliant.
- **Mathematical Rigor:** Any updates to `kinematics.py`, `sensor_fusion.py`, or `stabilization.py` MUST be accompanied by updates in `docs/MATHEMATICS.md`.
- **Unit Tests:** You must add or update tests in `tests/` to cover new logic.

### 5. Verification (Gökbörü Guardian)
Before submitting a PR, ensure all tests pass:
```bash
pytest tests/ -v
python analysis/simulations/tracking_sim.py --headless
```

### 6. Submit a Pull Request
Push your branch to your fork and open a Pull Request against the `main` branch. Fill out the PR template completely.

## 📜 Code of Conduct
We are a team driven by technical excellence. Please communicate professionally, provide constructive code reviews, and focus on the mission: *National Autonomy and Seamless Connectivity*.
