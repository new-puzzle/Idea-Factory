#!/bin/bash

# Idea Factory - Quick Start Script

echo "🏭 Idea Factory - Quick Start"
echo "=============================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "📝 Please edit .env and add your ANTHROPIC_API_KEY"
    echo "   Then run this script again."
    exit 1
fi

# Check if API key is set
if grep -q "your_api_key_here" .env; then
    echo "⚠️  Please update your ANTHROPIC_API_KEY in .env file"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check which mode to run
echo "Select mode:"
echo "1) Run Streamlit frontend only (recommended)"
echo "2) Run FastAPI backend only"
echo "3) Run both frontend and backend"
echo ""
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        echo ""
        echo "🚀 Starting Streamlit frontend..."
        echo "   Open http://localhost:8501 in your browser"
        echo ""
        cd frontend
        streamlit run app.py
        ;;
    2)
        echo ""
        echo "🚀 Starting FastAPI backend..."
        echo "   API docs: http://localhost:8000/docs"
        echo ""
        cd backend
        python main.py
        ;;
    3)
        echo ""
        echo "🚀 Starting both services..."
        echo "   Backend: http://localhost:8000"
        echo "   Frontend: http://localhost:8501"
        echo ""
        # Start backend in background
        cd backend
        python main.py &
        BACKEND_PID=$!

        # Start frontend
        cd ../frontend
        streamlit run app.py

        # Cleanup on exit
        kill $BACKEND_PID
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
