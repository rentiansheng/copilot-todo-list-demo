#!/bin/bash
# Start the Tree Management API server

echo "Starting Tree Management API..."
echo "Make sure Elasticsearch is running and configured in .env file"
echo ""

# Check if .env exists, if not copy from example
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "Please edit .env with your Elasticsearch credentials"
    echo ""
fi

# Install dependencies if not already installed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# Start the server
echo "Starting server on http://localhost:8000 (binding to all interfaces 0.0.0.0:8000)"
echo "API docs available at http://localhost:8000/docs"
echo ""

uvicorn main:app --reload --host 0.0.0.0 --port 8000
