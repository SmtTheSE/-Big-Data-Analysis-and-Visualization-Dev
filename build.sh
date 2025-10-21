#!/usr/bin/env bash

# Exit on error
set -e

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

echo "Build completed successfully!"