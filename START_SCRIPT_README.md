# TARDIS Lights Project - Start Script Documentation

## Overview
The `start.sh` script automates the startup of the TARDIS Lights project, which consists of a FastAPI backend and a React frontend. It ensures both servers run simultaneously for development.

## Prerequisites
- Python virtual environment set up in `.venv/` with dependencies installed (`pip install -r backend/requirements.txt`)
- Node.js and npm installed with dependencies (`npm install` in `frontend/`)

## What the Script Does

### 1. Activate Virtual Environment
```bash
source .venv/bin/activate
```
- Activates the Python virtual environment to use the correct Python interpreter and installed packages.
- Ensures the backend runs with the required dependencies (FastAPI, Uvicorn, etc.).

### 2. Start Backend Server
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 &
```
- Launches the FastAPI backend server.
- `--host 127.0.0.1`: Binds to localhost for security.
- `--port 8000`: Runs on port 8000.
- `&`: Runs in the background so the script can continue.
- The backend provides API endpoints for LED control (e.g., `/led/on`, `/led/off`).

### 3. Start Frontend Server
```bash
cd frontend
npm start &
```
- Changes to the `frontend/` directory.
- Runs `npm start` to launch the React development server.
- `&`: Runs in the background.
- The frontend serves the UI on port 3001 (default for React).

## Usage
1. Make sure you're in the project root: `cd /Users/nibeck/Documents/Development/tardis-lights`
2. Run: `./start.sh`
3. Access:
   - Frontend: `http://localhost:3001`
   - Backend API docs: `http://127.0.0.1:8000/docs`

## Stopping the Servers
- Press `Ctrl+C` in the terminal running the script to stop both servers.
- Or kill processes manually: `lsof -ti:8000,3001 | xargs kill -9`

## Notes
- The script assumes the virtual environment and npm dependencies are already installed.
- For production, use Docker Compose instead (see `docker-compose.yml`).
- If ports are in use, the script may fail—kill existing processes first.