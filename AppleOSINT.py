#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DetectMe - OSINT Tool
Main Application Entry Point
"""

import sys
import os
import platform

# Check if running on macOS/iOS
if platform.system() != "Darwin":
    print("Error: This tool is designed exclusively for Apple devices (macOS/iOS)")
    print("   Detected system:", platform.system())
    sys.exit(1)

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Core.Main import MainApplication

def main():
    """Main entry point for AppleOSINT"""
    try:
        app = MainApplication()
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()



