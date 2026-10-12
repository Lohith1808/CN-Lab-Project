"""
main.py
Execution entry point for Subnet Mask Calculator
"""

import sys
from cli_interface import run_app

def main():
    try:
        run_app()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()