#!/bin/bash
# Start Python FastAPI backend on port 5001
cd "$(dirname "$0")"
python3 -m uvicorn main:app --host 0.0.0.0 --port 5001 --reload
