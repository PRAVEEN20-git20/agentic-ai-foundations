#!/usr/bin/env python3
"""
Interactive CLI for Document Q&A Agent

Provides a user-friendly command-line interface for interacting with
the Document Q&A agent with colored output and special commands.
"""

import os
import sys
from pathlib import Path
from typing import Optional
from doc_qa_agent import DocumentQAAgent


# ANSI color codes for terminal output
class Colors:
    """Terminal color codes for pretty output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_colored(text: str, color: str = Colors.END, end: str = '\n') -> None:
    """Print colored text to terminal."""
    print(f"{color}{text}{Colors.END}", end=end)


def print_banner() -> None:
    """Print welcome banner."""
    banner = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║           📚 Document Q&A Agent CLI 📚                    ║
║                                                          ║
║      An Agentic AI for Intelligent Document Search       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """
    print_colored(banner, Colors.CYAN + Colors.BOLD)
    print_colored("Type 'help' for commands or 'exit' to quit\n", Colors.YELLOW)


def print_separator() -> None:
    """Print a visual separator."""
    print_colored("─" * 60, Colors.BLUE)


def load_environment() -> bool:
    """
    Load environment variables from .env file.
    
    Returns:
        True if OpenAI API key is set, False otherwise
    """
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass  # python-dotenv not installed, rely on system env vars
    
    return bool(os.getenv("OPENAI_API_KEY"))


def initialize_agent() -> Optional[DocumentQAAgent]:
    """
    Initialize the Document Q&A agent.
    
    Returns:
        DocumentQAAgent instance or None if initialization fails
    """
    try:
        agent = DocumentQAAgent()
        print_colored("✓ Agent initialized successfully!\n", Colors.GREEN)
        return agent
    except ValueError as e:
        print_colored(f"\n✗ Error: {str(e)}", Colors.RED)
        print_colored("\nPlease set your OPENAI_API_KEY in a .env file or environment variable.", Colors.YELLOW)
        print_colored("Example: OPENAI_API_KEY=sk-...", Colors.YELLOW)
        return None
    except Exception as e:
        print_colored(f"\n✗ Unexpected error: {str(e)}", Colors.RED)
        return None


def handle_load_command(agent: DocumentQAAgent, args: str) -> None:
    """
    Handle the 'load' command to load PDF documents.
    
    Args:
        agent: The DocumentQAAgent instance
        args: Arguments (file paths) for the load command
    """
    if not args.strip():
        print_colored("Usage: load <file_path> [file_path2 ...]", Colors.YELLOW)
        print_colored("Example: load document.pdf", Colors.YELLOW)
        return
    
    # Parse file paths (support multiple files)
    file_paths = [path.strip() for path in args.split()]
    
    # Validate files exist
    valid_paths = []
    for path in file_paths:
        if Path(path).exists():
            valid_paths.append(path)
        else:
            print_colored(f"✗ File not found: {path}", Colors.RED)
    
    if not valid_paths:
        print_colored("✗ No valid files to load", Colors.RED)
        return
    
    # Load documents
    try:
        if len(valid_paths) == 1:
            agent.load_document(valid_paths[0])
        else:
            agent.load_multiple_documents(valid_paths)
    except Exception as e:
        print_colored(f"✗ Error loading documents: {str(e)}", Colors.RED)


def handle_save_command(agent: DocumentQAAgent, args: str) -> None:
    """
    Handle the 'save' command to save vector store.
    
    Args:
        agent: The DocumentQAAgent instance
        args: Arguments (store name) for the save command
    """
    name = args.strip() if args.strip() else "default"
    response = agent.save_vector_store(name=name)
    
    if "✓" in response:
        print_colored(response, Colors.GREEN)
    else:
        print_colored(response, Colors.RED)


def handle_loadstore_command(agent: DocumentQAAgent, args: str) -> None:
    """
    Handle the 'loadstore' command to load a saved vector store.
    
    Args:
        agent: The DocumentQAAgent instance
        args: Arguments (store name) for the loadstore command
    """
    name = args.strip() if args.strip() else "default"
    response = agent.load_vector_store(name=name)
    
    if "✓" in response:
        print_colored(response, Colors.GREEN)
    else:
        print_colored(response, Colors.RED)


def format_answer(result: dict) -> str:
    """
    Format the agent's answer with sources.
    
    Args:
        result: Result dictionary from agent.ask()
        
    Returns:
        Formatted answer string
    """
    answer = result['answer']
    sources = result.get('sources', [])
    confidence = result.get('confidence', 'unknown')
    
    output = f"\n{answer}\n"
    
    # Add confidence indicator
    if confidence == 'high':
        output += f"\n{Colors.GREEN}🎯 Confidence: High{Colors.END}"
    elif confidence == 'medium':
        output += f"\n{Colors.YELLOW}🎯 Confidence: Medium{Colors.END}"
    elif confidence == 'low':
        output += f"\n{Colors.YELLOW}🎯 Confidence: Low{Colors.END}"
    
    # Add sources
    if sources and not result.get('error'):
        output += f"\n\n{Colors.CYAN}📚 Sources:{Colors.END}\n"
        seen_sources = set()
        for source in sources:
            source_key = f"{source['source']} (Page {source['page']})"
            if source_key not in seen_sources:
                similarity_pct = int(source['similarity'] * 100)
                output += f"  - {source_key} (relevance: {similarity_pct}%)\n"
                seen_sources.add(source_key)
    
    return output


def run_cli() -> None:
    """Main CLI loop."""
    # Print banner
    print_banner()
    
    # Load environment
    if not load_environment():
        print_colored("⚠️  Warning: OPENAI_API_KEY not found in environment", Colors.YELLOW)
    
    # Initialize agent
    agent = initialize_agent()
    if agent is None:
        return
    
    print_colored("Ready to answer your questions! Load a document to get started.\n", Colors.GREEN)
    
    # Main interaction loop
    while True:
        try:
            # Get user input
            print_colored("\nYou: ", Colors.BOLD, end='')
            user_input = input().strip()
            
            # Handle empty input
            if not user_input:
                continue
            
            # Normalize input
            user_input_lower = user_input.lower()
            
            # Check for exit commands
            if user_input_lower in ['exit', 'quit', 'q', 'bye']:
                print_colored("\n👋 Goodbye! Thanks for using Document Q&A Agent!", Colors.CYAN)
                break
            
            # Check for special commands
            if user_input_lower.startswith('load '):
                handle_load_command(agent, user_input[5:])
                continue
            
            if user_input_lower.startswith('save'):
                args = user_input[4:].strip() if len(user_input) > 4 else ""
                handle_save_command(agent, args)
                continue
            
            if user_input_lower.startswith('loadstore'):
                args = user_input[9:].strip() if len(user_input) > 9 else ""
                handle_loadstore_command(agent, args)
                continue
            
            if user_input_lower == 'help':
                response = agent.get_help()
                print_colored(f"\n{response}", Colors.CYAN)
                continue
            
            if user_input_lower in ['status', 'info']:
                response = agent.get_status()
                print_colored(f"\n{response}", Colors.CYAN)
                continue
            
            if user_input_lower == 'clear':
                response = agent.clear_history()
                print_colored(f"\n{response}", Colors.GREEN)
                continue
            
            if user_input_lower == 'history':
                history = agent.get_conversation_history()
                if history:
                    print_colored("\n📜 Recent Conversation History:", Colors.CYAN)
                    for i, conv in enumerate(history, 1):
                        print_colored(f"\n{i}. Q: {conv['question']}", Colors.YELLOW)
                        print_colored(f"   A: {conv['answer'][:100]}...", Colors.GREEN)
                else:
                    print_colored("\nNo conversation history yet.", Colors.YELLOW)
                continue
            
            # Process as question
            print_colored("\n🤔 Thinking...", Colors.YELLOW)
            
            # Check if it's a question
            if '?' in user_input or any(word in user_input_lower for word in ['what', 'how', 'why', 'when', 'where', 'who']):
                result = agent.ask(user_input)
                response = format_answer(result)
                print_colored(f"\n{Colors.BOLD}Agent:{Colors.END} {response}")
            else:
                # Use chat for general conversation
                response = agent.chat(user_input)
                print_colored(f"\n{Colors.BOLD}Agent:{Colors.END} {response}", Colors.GREEN)
        
        except KeyboardInterrupt:
            print_colored("\n\n👋 Interrupted. Goodbye!", Colors.CYAN)
            break
        
        except Exception as e:
            print_colored(f"\n✗ Error: {str(e)}", Colors.RED)
            print_colored("Type 'help' for usage information.", Colors.YELLOW)


def main() -> None:
    """Entry point for CLI."""
    try:
        run_cli()
    except Exception as e:
        print_colored(f"\n✗ Fatal error: {str(e)}", Colors.RED)
        sys.exit(1)


if __name__ == "__main__":
    main()

