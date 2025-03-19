from flask import Flask, request, jsonify, send_from_directory
import os
import time
import threading
import json
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import SecretStr
import logging
import queue
import sys

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Queue to store logs
logs_queue = queue.Queue()
# Flag to indicate if a task is running
task_running = False
# Flag to indicate if a task has completed
task_completed = False

# Custom log handler that adds messages to our queue
class QueueHandler(logging.Handler):
    def emit(self, record):
        log_entry = {
            'timestamp': int(time.time() * 1000),
            'message': self.format(record)
        }
        logs_queue.put(log_entry)

# Add our custom handler to the root logger
queue_handler = QueueHandler()
queue_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(queue_handler)

# Redirect stdout and stderr to our logging system
class LoggerWriter:
    def __init__(self, level):
        self.level = level
        self.buffer = []

    def write(self, message):
        if not message:
            return
            
        # Make sure message is a string
        if isinstance(message, bytes):
            message = message.decode('utf-8', errors='replace')
            
        if message.strip():
            self.buffer.append(message)
            if message.endswith('\n'):
                self.flush()

    def flush(self):
        if self.buffer:
            # Make sure all items in buffer are strings
            str_buffer = [item if isinstance(item, str) else item.decode('utf-8', errors='replace') 
                          for item in self.buffer]
            message = ''.join(str_buffer)
            logger.log(self.level, message.strip())
            self.buffer = []

# Redirect stdout to INFO level logs
sys.stdout = LoggerWriter(logging.INFO)
# Redirect stderr to ERROR level logs
sys.stderr = LoggerWriter(logging.ERROR)

async def run_agent(task):
    global task_running, task_completed
    
    try:
        # Reset flags
        task_running = True
        task_completed = False
        
        # Get API key for DeepSeek
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            logger.error("DEEPSEEK_API_KEY not found in environment variables")
            raise ValueError("DEEPSEEK_API_KEY environment variable is not set")
        
        logger.info(f"Initializing DeepSeek LLM")
        
        # Initialize the LLM with DeepSeek V3
        llm = ChatOpenAI(
            base_url='https://api.deepseek.com/v1',
            model='deepseek-v3',  # Using DeepSeek V3 model
            api_key=SecretStr(api_key),
            temperature=0.2,  # Lower temperature for more deterministic responses
            max_tokens=4096,  # Limit token usage
            timeout=60,  # Set timeout to prevent hanging requests
        )
        
        logger.info(f"Creating agent with task: {task}")
        
        # Create the agent with the task
        # Note: Agent class only accepts basic parameters, not all the ones we tried before
        agent = Agent(
            task=task,
            llm=llm,
            use_vision=False  # Set to True if you need visual capabilities
        )
        
        logger.info("Starting agent execution")
        
        # Run the agent
        await agent.run()
        
        logger.info("Agent execution completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error running agent: {str(e)}")
        return False
    finally:
        task_running = False
        task_completed = True

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/execute', methods=['POST'])
def execute_task():
    global task_running
    
    if task_running:
        return jsonify({'success': False, 'message': 'A task is already running'}), 409
    
    data = request.json
    task = data.get('task')
    
    if not task:
        return jsonify({'success': False, 'message': 'No task provided'}), 400
    
    # Clear the logs queue
    while not logs_queue.empty():
        logs_queue.get()
    
    # Start the agent in a separate thread
    def run_async_task():
        asyncio.run(run_agent(task))
    
    threading.Thread(target=run_async_task).start()
    
    return jsonify({'success': True, 'message': 'Task started'})

@app.route('/logs')
def get_logs():
    since = int(request.args.get('since', 0))
    logs = []
    
    # Get all logs from the queue that are newer than 'since'
    while not logs_queue.empty():
        log = logs_queue.get()
        if log['timestamp'] > since:
            logs.append(log)
    
    return jsonify({
        'logs': logs,
        'completed': task_completed
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000) 