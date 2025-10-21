#!/usr/bin/env bash

# Exit on error
set -e

# Explicitly use Python 3.10
export PYTHON_VERSION=3.10.8

# Upgrade pip and build tools
pip install --upgrade pip setuptools wheel

# Install Pillow first to avoid conflicts
pip install Pillow==10.0.1

# Install other dependencies
pip install -r requirements.txt

echo "Build completed successfully!"