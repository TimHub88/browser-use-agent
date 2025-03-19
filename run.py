#!/usr/bin/env python3
import argparse
import asyncio
import os
from dotenv import load_dotenv
from pydantic import SecretStr
from browser_use import Agent
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

async def run_agent(task):
    """Run the browser agent with the given task"""
    # Get API key from environment
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY environment variable is not set")
    
    print(f"Initializing DeepSeek V3 LLM...")
    
    # Initialize the LLM
    llm = ChatOpenAI(
        base_url='https://api.deepseek.com/v1',
        model='deepseek-v3',
        api_key=SecretStr(api_key),
        temperature=0.2,  # Lower temperature for more deterministic responses
        max_tokens=4096,  # Limit token usage
        timeout=60,  # Set timeout to prevent hanging requests
    )
    
    print(f"Creating agent with task: {task}")
    
    # Create the agent with the task
    # Note: Agent class only accepts basic parameters
    agent = Agent(
        task=task,
        llm=llm,
        use_vision=False
    )
    
    print("Starting agent execution...")
    
    # Run the agent
    await agent.run()
    
    print("Task completed!")

def run_web_interface():
    """Run the web interface"""
    from server import app
    print("Starting web interface on http://localhost:5000")
    app.run(debug=True, port=5000)

def main():
    parser = argparse.ArgumentParser(description='Browser-Use with DeepSeek V3')
    
    # Create subparsers for the different modes
    subparsers = parser.add_subparsers(dest='mode', help='Mode of operation')
    
    # Web interface mode
    web_parser = subparsers.add_parser('web', help='Run the web interface')
    
    # CLI mode for direct task execution
    cli_parser = subparsers.add_parser('cli', help='Run a task directly from command line')
    cli_parser.add_argument('task', type=str, help='The task to execute')
    
    args = parser.parse_args()
    
    if args.mode == 'web':
        run_web_interface()
    elif args.mode == 'cli':
        asyncio.run(run_agent(args.task))
    else:
        parser.print_help()

if __name__ == '__main__':
    main() 