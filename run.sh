#!/bin/bash

echo "🔁 Activating virtual environment..."

if [ ! -f "venv/bin/activate" ]; then
    echo "❌ Virtual environment not found. Run 'python3 -m venv venv' first."
    exit 1
fi

source venv/bin/activate

if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
else
    echo "⚠️ requirements.txt not found. Skipping pip install."
fi

echo "🚀 Starting FastAPI server with Uvicorn..."
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > logs.txt 2>&1 &

echo "✅ Server started in background with PID $!"
echo "📄 Logs are being written to: logs.txt"
