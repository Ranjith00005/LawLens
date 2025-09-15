#!/bin/bash

# LawLens Startup Script

echo "🚀 Starting LawLens Legal Research Assistant..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Please create .env file with your API keys (see .env.example)"
    exit 1
fi

echo "Starting backend server..."
cd backend
uvicorn hybrid_main:app --host 0.0.0.0 --port 9001 --reload &
BACKEND_PID=$!

echo "Waiting for backend to start..."
sleep 3

echo "Starting frontend..."
cd ../frontend
streamlit run app.py &
FRONTEND_PID=$!

echo "✅ LawLens is running!"
echo "Backend: http://localhost:9001"
echo "Frontend: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait