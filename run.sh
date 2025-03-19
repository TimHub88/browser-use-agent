#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if the virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate || source venv/Scripts/activate

# Install required packages if not already installed
echo "Installing requirements..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    echo "DEEPSEEK_API_KEY=" > .env
    echo "Please edit the .env file and add your DeepSeek API key."
    echo "You can do this by opening the .env file in a text editor."
    exit 1
fi

# Check if DEEPSEEK_API_KEY is set in .env
if grep -q "DEEPSEEK_API_KEY=$" .env; then
    echo "DeepSeek API key is not set in .env file."
    echo "Please edit the .env file and add your DeepSeek API key."
    exit 1
fi

# Run the application based on the provided arguments
if [ "$1" = "web" ]; then
    echo "Starting web interface..."
    python run.py web
elif [ "$1" = "cli" ]; then
    shift
    echo "Running command-line task: $*"
    python run.py cli "$*"
else
    echo "Usage: ./run.sh [web|cli <task>]"
    echo "  web            Start the web interface"
    echo "  cli <task>     Run a task directly from command line"
fi 