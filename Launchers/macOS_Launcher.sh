#!/bin/bash

# macOS Launcher for AppleOSINT

cd "$(dirname "$0")/.."

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Error: This launcher is designed for macOS only!"
    exit 1
fi

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run AppleOSINT
python3 AppleOSINT.py



