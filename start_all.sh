#!/bin/bash

# Start Python backend on port 5001
echo "Starting Python FastAPI backend on port 5001..."
cd python_backend && python3 -m uvicorn main:app --host 0.0.0.0 --port 5001 --reload &
PYTHON_PID=$!
cd ..

# Wait for Python backend to be ready
echo "Waiting for Python backend..."
for i in {1..10}; do
  if curl -s http://localhost:5001/ > /dev/null 2>&1; then
    echo "Python backend is ready!"
    break
  fi
  sleep 1
done

# Start Node.js frontend/proxy server on port 5000
echo "Starting Node.js frontend server on port 5000..."
npm run dev &
NODE_PID=$!

echo "Both servers started!"
echo "Python backend PID: $PYTHON_PID"
echo "Node.js frontend PID: $NODE_PID"

# Wait for both processes
wait
