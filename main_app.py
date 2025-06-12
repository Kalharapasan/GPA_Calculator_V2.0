#!/usr/bin/env python3
"""
Advanced GPA Calculator Application
===================================

A modern, feature-rich GPA calculator with user authentication,
data persistence, and a beautiful user interface.

Author: Assistant
Version: 2.0
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from gpa_calculator import ModernGPACalculator
    from database_manager import DatabaseManager
    from login_window import LoginWindow
except ImportError as e:
    print(f"Import Error: {e}")
    print("Make sure all required files are in the same directory:")
    print("- main_app.py")
    print("- gpa_calculator.py")
    print("- database_manager.py")
    print("- login_window.py")
    sys.exit(1)


class GPACalculatorApp:
    """Main application class that handles the application lifecycle"""
    
    def __init__(self):
        self.root = None
        self.calculator = None
        self.setup_application()
    
    def setup_application(self):
        """Initialize the main application"""
        try:
            self.root = tk.Tk()
            self.root.title("Advanced GPA Calculator")
            self.root.withdraw()
            self.root.minsize(800, 600)

            try:
                self.root.tk.call('tk', 'scaling', 1.0)
            except:
                pass

            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

            self.calculator = ModernGPACalculator(self.root)
            self.root.deiconify()

        except Exception as e:
            self.handle_startup_error(e)

    def handle_startup_error(self, error):
        error_msg = f"Failed to start application: {str(error)}"
        print(error_msg)

        if self.root:
            try:
                messagebox.showerror("Startup Error", error_msg)
            except:
                pass
        sys.exit(1)

    def on_closing(self):
        try:
            if self.calculator and self.calculator.current_user_id:
                if messagebox.askyesno("Quit Application", "Do you want to save your data before quitting?", parent=self.root):
                    self.calculator.save_data()

            if messagebox.askokcancel("Quit", "Are you sure you want to quit?", parent=self.root):
                self.cleanup_and_exit()
        except:
            self.cleanup_and_exit()

    def cleanup_and_exit(self):
        try:
            if self.root:
                self.root.quit()
                self.root.destroy()
        except:
            pass
        finally:
            sys.exit(0)

    def run(self):
        try:
            if self.root:
                self.root.mainloop()
        except KeyboardInterrupt:
            print("\nApplication interrupted by user")
            self.cleanup_and_exit()
        except Exception as e:
            print(f"Runtime error: {e}")
            self.cleanup_and_exit()


def check_dependencies():
    """Check if all required dependencies are available"""
    required_modules = ['tkinter', 'sqlite3', 'hashlib', 'json', 'datetime', 're']
    missing_modules = []

    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)

    if missing_modules:
        print("Missing required modules:")
        for module in missing_modules:
            print(f"  - {module}")
        print("\nPlease install the missing modules and try again.")
        return False

    return True


def main():
    """Main entry point of the application"""
    print("Advanced GPA Calculator v2.0")
    print("=" * 40)

    if not check_dependencies():
        sys.exit(1)

    app = GPACalculatorApp()
    app.run()


if __name__ == "__main__":
    main()
