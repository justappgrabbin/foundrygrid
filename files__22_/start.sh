#!/bin/bash

# SynthAI Startup Script

echo "╔════════════════════════════════════════════════════════════╗"
echo "║               🧬 SynthAI - Starting Up                     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in the right directory
if [ ! -f "api/app.py" ]; then
    echo "❌ Error: Please run this script from the synthai directory"
    exit 1
fi

echo "📦 Installing dependencies..."
pip install -r requirements.txt --break-system-packages -q

echo "✅ Dependencies installed"
echo ""

echo "🚀 Starting API server on port 5000..."
echo "   API endpoints available at: http://localhost:5000"
echo ""

cd api
python app.py
