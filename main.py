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
        print("5. Analyze Mission Log (Generate Visual Report)")
        print("6. Exit")
        print("="*50)
        
        choice = input("Select an option (1-6): ")
        
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
            log_files = [f for f in os.listdir('.') if f.startswith('mission_log') and f.endswith('.csv')]
            if not log_files:
                print("No mission logs found. Run a simulation or GUI first.")
                time.sleep(1)
                continue
            print("\nAvailable Logs:")
            for i, f in enumerate(log_files):
                print(f"{i+1}. {f}")
            log_choice = input("\nSelect a log to analyze (or 'q' to cancel): ")
            if log_choice.isdigit() and 1 <= int(log_choice) <= len(log_files):
                selected_log = log_files[int(log_choice)-1]
                os.system(f"python analysis/simulations/report_generator.py {selected_log}")
            else:
                continue
        elif choice == '6':
            print("Exiting GÖKBÖRÜ Command Center. İstikbal Göklerdedir!")
            break
        else:
            print("Invalid selection. Try again.")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
