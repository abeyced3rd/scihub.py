#!/bin/bash

# Quick Start Guide for SciHub Web Application

echo "╔════════════════════════════════════════════════════════════╗"
echo "║          SciHub Web Application - Quick Start              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.6 or higher."
    exit 1
fi

echo "✅ Python is installed"
echo ""

# Install dependencies if needed
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Create downloads folder
mkdir -p downloads

echo "✅ Created downloads folder"
echo ""

# Run the application
echo "🚀 Starting SciHub Web Application..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 Open your browser and go to: http://localhost:5000"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python run.py
