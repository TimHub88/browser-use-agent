@echo off
SETLOCAL EnableDelayedExpansion

REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH. Please install Python and try again.
    exit /b 1
)

REM Check if the virtual environment exists
IF NOT EXIST venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Install required packages if not already installed
echo Installing requirements...
pip install -r requirements.txt

REM Check if .env file exists
IF NOT EXIST .env (
    echo Creating .env file...
    echo DEEPSEEK_API_KEY= > .env
    echo Please edit the .env file and add your DeepSeek API key.
    echo You can do this by opening the .env file in a text editor.
    exit /b 1
)

REM Check if first argument is "web"
IF "%1"=="web" (
    echo Starting web interface...
    python run.py web
    exit /b 0
)

REM Check if first argument is "cli"
IF "%1"=="cli" (
    SET "task=%*"
    SET "task=!task:cli =!"
    echo Running command-line task: !task!
    python run.py cli "!task!"
    exit /b 0
)

REM If no valid arguments provided, show usage instructions
echo Usage: run.bat [web^|cli ^<task^>]
echo   web            Start the web interface
echo   cli ^<task^>     Run a task directly from command line

ENDLOCAL 