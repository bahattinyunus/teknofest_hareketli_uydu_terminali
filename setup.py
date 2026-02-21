from setuptools import setup, find_packages

setup(
    name="gokboru_sotm",
    version="1.0.0",
    author="Gökbörü Otonom Sistemleri",
    description="Teknofest 2026 Mobile Satellite Terminal Stabilization System",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "PyQt6",
        "pyqtgraph",
        "matplotlib",
        "pandas",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "black",
            "flake8",
        ]
    },
    entry_points={
        "console_scripts": [
            "sotm-gui=src.gui_app:main",
            "sotm-sim=analysis.simulations.tracking_sim:run_verification_sim",
        ],
    },
)
