#!/bin/bash
## Installing dependancies
echo "Installing dependancies"
pip install -r requitements.txt
# Start FastAPI backend
echo "Starting FastAPI backend..."
uvicorn backend.src.api.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Start React frontend
echo "Starting React frontend..."
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install --legacy-peer-deps
npm run dev &
FRONTEND_PID=$!

# Wait for both processes to exit
wait $BACKEND_PID
wait $FRONTEND_PID
