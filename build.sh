#!/bin/bash
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Setting up environment..."
# Create necessary directories
mkdir -p logs
mkdir -p temp

echo "Build completed successfully!"