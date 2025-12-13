#!/bin/bash

# Script to test the TARDIS Lights API with Mock LEDs

echo "Starting TARDIS Lights API with Mock LEDs..."

# Activate virtual environment
source .venv/bin/activate

# Start the backend server in the background
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!

# Wait for server to start
sleep 2

echo "Testing API endpoints..."
echo "======================="

# Test /led/on
echo "Testing /led/on:"
curl -s -X POST http://localhost:8000/led/on
echo -e "\n"

# Test /led/color
echo "Testing /led/color (red):"
curl -s -X POST "http://localhost:8000/led/color?r=255&g=0&b=0"
echo -e "\n"

# Test /led/pulse
echo "Testing /led/pulse (green):"
curl -s -X POST "http://localhost:8000/led/pulse?r=0&g=255&b=0"
echo -e "\n"

# Test /led/off
echo "Testing /led/off:"
curl -s -X POST http://localhost:8000/led/off
echo -e "\n"

# Stop the server
echo "Stopping server..."
kill $SERVER_PID

echo "Test complete! Check the Mock LED outputs above."