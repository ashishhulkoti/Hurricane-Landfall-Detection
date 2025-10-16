#!/bin/bash

# --------------------------------------------------------------------
# Script: run_app.sh
# Description: Create a Python virtual environment, install dependencies,
#              and run the Streamlit visualization app.
# Usage: ./run_app.sh
# --------------------------------------------------------------------

# Step 1. Create virtual environment
echo "🔧 Creating virtual environment (.venv)..."
python3 -m venv .venv

# Step 2. Activate the virtual environment
echo "✅ Activating virtual environment..."
source .venv/bin/activate

# Step 3. Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Step 4. Install dependencies
echo "📦 Installing required packages..."
pip install -r requirements.txt

# Step 5. Run the Streamlit application
echo "🚀 Launching Streamlit app..."
streamlit run visualizer.py
