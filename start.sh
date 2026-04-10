#!/bin/bash
# Start script for HidenCloud deployment

# Install dependencies
pip install -r requirements.txt

# Set default env vars if not set
export AUTH_TOKEN=${AUTH_TOKEN:-"your-secret-token"}
export PORT=${PORT:-8000}

# Start the server
uvicorn app:app --host 0.0.0.0 --port $PORT