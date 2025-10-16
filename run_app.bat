@echo off
REM ---------------------------------------------------------------
REM Script: run_app.bat
REM Description: Create virtual environment, install dependencies,
REM              and launch Streamlit app for HURDAT2 project.
REM ---------------------------------------------------------------

echo 🔧 Creating virtual environment (.venv)...
python -m venv .venv

echo ✅ Activating virtual environment...
call .venv\Scripts\activate

echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

echo 📦 Installing required packages...
pip install -r requirements.txt

echo 🚀 Launching Streamlit app...
streamlit run visualizer.py

pause
