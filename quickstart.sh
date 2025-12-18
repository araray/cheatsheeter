#!/bin/bash
# CheatSheeter Quick Start Script

set -e

echo "🚀 CheatSheeter Quick Start"
echo "============================"
echo ""

# Check if Docker is installed
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "✓ Docker found"
    echo ""
    echo "Starting CheatSheeter with Docker..."
    docker-compose up -d
    echo ""
    echo "✓ CheatSheeter is running!"
    echo "📝 Access at: http://localhost:5000"
    echo ""
    echo "Commands:"
    echo "  docker-compose logs -f    # View logs"
    echo "  docker-compose down       # Stop application"
    echo ""
else
    echo "Docker not found. Starting locally..."
    echo ""

    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 is required but not installed."
        exit 1
    fi

    echo "✓ Python found"

    # Setup backend
    echo ""
    echo "Setting up backend..."
    cd backend

    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi

    # Activate virtual environment
    source venv/bin/activate

    # Install dependencies
    echo "Installing dependencies..."
    pip install -q --upgrade pip
    pip install -q -r requirements.txt

    # Create cheatsheets directory
    mkdir -p cheatsheets

    # Start server
    echo ""
    echo "✓ Starting CheatSheeter..."
    echo "📝 Access at: http://localhost:5000"
    echo ""
    echo "Press Ctrl+C to stop"
    python app.py
fi
