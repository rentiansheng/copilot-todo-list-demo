#!/bin/bash

# CMDB Tree API Startup Script

echo "Starting CMDB Tree API..."
echo "================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found!"
    echo "Copying .env.example to .env..."
    cp .env.example .env
    echo "Please edit .env file to configure your Elasticsearch connection."
fi

# Start the server
echo "================================"
echo "Starting server on http://0.0.0.0:8000"
echo "API Documentation: http://localhost:8000/docs"
echo "Health Check: http://localhost:8000/health"
echo "================================"
echo ""

uvicorn main:app --reload --host 0.0.0.0 --port 8000
