#!/bin/bash

# TARDIS Lights Project - Start Script
# This script automates the startup of the TARDIS Lights project, which consists of a FastAPI backend and a React frontend. It ensures both servers run simultaneously for development.
#
# Prerequisites:
# - Python virtual environment set up in .venv/ with dependencies installed (pip install -r backend/requirements.txt)
# - Node.js and npm installed with dependencies (npm install in frontend/)
#
# What the Script Does:
# 1. Activate Virtual Environment: Activates the Python venv to use correct interpreter and packages.
# 2. Start Backend Server: Launches FastAPI on port 8000 in background.
# 3. Start Frontend Server: Launches React dev server on port 3001 in background.
#
# Usage: ./start.sh from project root
# Access: Frontend http://localhost:3001, Backend http://127.0.0.1:8000/docs

echo "Starting TARDIS Lights project..."

# Step 1: Activate the Python virtual environment
echo "Activating Python virtual environment..."
source .venv/bin/activate

# Step 2: Start the backend server in the background
echo "Starting backend server on http://127.0.0.1:8000..."
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 &

# Step 3: Start the frontend server in the background
echo "Starting frontend server..."
cd frontend
npm start &

echo "Both servers are starting in the background."
echo "Backend API: http://127.0.0.1:8000"
echo "Frontend UI: http://localhost:3001"
echo "Press Ctrl+C to stop all servers."