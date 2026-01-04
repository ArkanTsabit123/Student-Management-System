# student-management/utils/helpers.py
"""
Helper functions for Student Management System
"""

import os
from typing import Any


class Helpers:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def display_header(title: str):
        Helpers.clear_screen()
        print("=" * 60)
        print(f"STUDENT MANAGEMENT SYSTEM".center(60))
        print(f"{title}".center(60))
        print("=" * 60)
        print()
    
    @staticmethod
    def wait_for_enter(message: str = "\nPress Enter to continue..."):
        input(message)
    
    @staticmethod
    def validate_input(prompt: str, validation_func=None, error_msg: str = "Invalid input"):
        while True:
            try:
                value = input(prompt).strip()
                if validation_func:
                    if validation_func(value):
                        return value
                    else:
                        print(f"Error: {error_msg}")
                else:
                    return value
            except KeyboardInterrupt:
                print("\nInput cancelled")
                return None
            except Exception as e:
                print(f"Error: {str(e)}")