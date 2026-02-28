import os
import sys
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    while True:
        clear_screen()
        print("="*50)
        print("🐺 GÖKBÖRÜ SOTM SYSTEM - COMMAND CENTER")
        print("="*50)
        print("1. Launch GUI Dashboard (Real-time Stabilization)")
        print("2. Run Headless Tracking Simulation")
        print("3. Run PID Auto-Optimizer (Differential Evolution)")
        print("4. Run System Unit Tests")
        print("5. Exit")
        print("="*50)
        
        choice = input("Select an option (1-5): ")
        
        if choice == '1':
            from src.gui_app import main as launch_gui
            launch_gui()
        elif choice == '2':
            os.system("python analysis/simulations/tracking_sim.py")
        elif choice == '3':
            os.system("python analysis/calculators/pid_optimizer.py")
        elif choice == '4':
            os.system("pytest tests/")
            input("\nPress Enter to return to menu...")
        elif choice == '5':
            print("Exiting GÖKBÖRÜ Command Center. İstikbal Göklerdedir!")
            break
        else:
            print("Invalid selection. Try again.")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
