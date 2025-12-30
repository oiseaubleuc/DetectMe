#!/bin/bash

# AppleOSINT Installation Script for macOS
# This script installs all necessary dependencies for AppleOSINT

echo "AppleOSINT Installation Script"
echo "=================================="
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Error: This script is designed for macOS only!"
    exit 1
fi

echo "Detected macOS system"
echo ""

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 first."
    echo "   You can install it using: brew install python3"
    exit 1
fi

echo "Python 3 found: $(python3 --version)"
echo ""

# Check for pip
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed. Installing pip3..."
    python3 -m ensurepip --upgrade
fi

echo "pip3 found"
echo ""

# Install Homebrew if not installed (optional, for system dependencies)
if ! command -v brew &> /dev/null; then
    echo "Warning: Homebrew not found. Some system dependencies might need manual installation."
    echo "   You can install Homebrew from: https://brew.sh"
    echo ""
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
echo "Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip3 install --upgrade pip
echo "pip upgraded"
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt
echo "Python dependencies installed"
echo ""

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p Logs
mkdir -p Reports
mkdir -p Screenshots
mkdir -p QRCodes
mkdir -p Proxies
mkdir -p Configuration
mkdir -p GUI/Theme
mkdir -p GUI/Credentials
mkdir -p GUI/Language
mkdir -p GUI/Icon/Entities
echo "Directories created"
echo ""

# Set permissions
echo "Setting permissions..."
chmod +x AppleOSINT.py
chmod +x Launchers/macOS_Launcher.sh
echo "Permissions set"
echo ""

echo "Installation completed successfully!"
echo ""
echo "To run AppleOSINT:"
echo "  source .venv/bin/activate"
echo "  python3 AppleOSINT.py"
echo ""
echo "Or use the launcher:"
echo "  ./Launchers/macOS_Launcher.sh"
echo ""

