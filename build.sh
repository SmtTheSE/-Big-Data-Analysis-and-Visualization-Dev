#!/usr/bin/env bash

# Exit on error
set -e

# Explicitly use Python 3.10
export PYTHON_VERSION=3.10.8

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install dependencies
pip install -r requirements.txt

echo "Build completed successfully!"