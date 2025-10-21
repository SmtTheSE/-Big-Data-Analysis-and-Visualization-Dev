#!/usr/bin/env bash

# Exit on error
set -e

# Explicitly use Python 3.10
export PYTHON_VERSION=3.10.8

# Upgrade pip and build tools
pip install --upgrade pip setuptools wheel

# Force use of pre-compiled wheels (avoid building from source)
pip install --only-binary=all -r requirements.txt

echo "Build completed successfully!"