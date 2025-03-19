# Browser-Use Web Interface

A simple web interface for the [Browser-Use](https://github.com/browser-use/browser-use) project that allows you to control a browser with DeepSeek V3 LLM.

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your DeepSeek API key:
   ```
   DEEPSEEK_API_KEY=your_api_key_here
   ```

## Usage

There are two ways to use this application:

### Web Interface

Run the web interface to input tasks and view logs through a browser:

**Windows:**
```
run.bat web
```

**Linux/Mac:**
```
./run.sh web
```

Then open your browser and navigate to `http://localhost:5000`:
1. Enter your task in the text area
2. Click "Execute Task"
3. The execution logs will appear in real-time in the logs section

### Command Line

Run a task directly from the command line:

**Windows:**
```
run.bat cli "your task description here"
```

**Linux/Mac:**
```
./run.sh cli "your task description here"
```

Example:
```
run.bat cli "Go to google.com and search for 'DeepSeek V3'"
```

## Features

- Simple web interface to input tasks
- Real-time logs of the agent's execution
- Command-line interface for direct task execution
- Uses DeepSeek V3 LLM for browser automation
- Cross-platform support (Windows, Linux, Mac)

## Requirements

- Python 3.9+
- Valid DeepSeek API key
- A browser supported by Browser-Use

## Note

This is a basic implementation. For more advanced features and configurations, please refer to the [Browser-Use documentation](https://docs.browser-use.com/). 