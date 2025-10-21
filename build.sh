#!/usr/bin/env bash

# Exit on error
set -e

# Explicitly set Python version
export PYTHON_VERSION=3.10.8

# Upgrade pip and build tools
pip install --upgrade pip setuptools wheel

# Install packages with preference for wheels and fallback strategy
pip install --prefer-binary --no-cache-dir -r requirements.txt

echo "Build completed successfully!"