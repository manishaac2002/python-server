#!/bin/bash

echo "🔁 Activating virtual environment..."
source venv/bin/activate

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🚀 Starting server with nohup..."
nohup python main.py > logs.txt 2>&1 &

echo "✅ Server started in background. Logs: logs.txt"
