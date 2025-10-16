#!/usr/bin/env python3
"""
Interactive CLI for Hello Advisor Agent

This script provides a user-friendly command-line interface for interacting
with the Hello Advisor agent. It demonstrates real-time agent interaction
with colored output and session management.
"""

import sys
from typing import Optional
from hello_advisor import HelloAdvisor


# ANSI color codes for better CLI experience
class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_banner():
    """Display welcome banner."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║           🤖  HELLO ADVISOR AGENT  🤖                ║
║                                                       ║
║     An AI Agent with Autonomy, Memory & Reasoning    ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
{Colors.ENDC}

{Colors.YELLOW}Welcome! I'm your Hello Advisor, an intelligent chat agent.
Type 'help' to see what I can do, or 'exit' to quit.{Colors.ENDC}
"""
    print(banner)


def print_user_input(text: str):
    """
    Print user input with formatting.

    Args:
        text: User input text
    """
    print(f"\n{Colors.GREEN}You:{Colors.ENDC} {text}")


def print_agent_response(text: str):
    """
    Print agent response with formatting.

    Args:
        text: Agent response text
    """
    print(f"\n{Colors.BLUE}Hello Advisor:{Colors.ENDC} {text}")


def print_system_message(text: str):
    """
    Print system message with formatting.

    Args:
        text: System message text
    """
    print(f"\n{Colors.YELLOW}[System]{Colors.ENDC} {text}")


def handle_special_commands(user_input: str, agent: HelloAdvisor) -> Optional[str]:
    """
    Handle special CLI commands.

    Args:
        user_input: User input text
        agent: HelloAdvisor instance

    Returns:
        Command result or None if not a special command
    """
    user_input_lower = user_input.lower().strip()
    
    if user_input_lower in ["exit", "quit", "q"]:
        # Get farewell from agent
        farewell = agent.process_input("goodbye")
        print_agent_response(farewell)
        print_system_message("Thank you for using Hello Advisor! 👋")
        return "EXIT"
    
    elif user_input_lower == "clear":
        # Clear screen (works on Unix-like systems)
        print("\033[2J\033[H")
        print_system_message("Screen cleared!")
        return "CONTINUE"
    
    elif user_input_lower == "export":
        # Export memory
        memory_json = agent.get_memory_export()
        print_system_message("Memory exported:")
        print(f"{Colors.CYAN}{memory_json}{Colors.ENDC}")
        return "CONTINUE"
    
    return None


def run_interactive_session():
    """
    Run the main interactive session loop.
    
    This function handles the continuous interaction between
    user and agent, managing input/output and session state.
    """
    print_banner()
    
    # Initialize agent
    agent = HelloAdvisor()
    
    print_system_message(f"Session started! Chat with {agent.name} below.\n")
    
    try:
        while True:
            # Get user input
            try:
                user_input = input(f"{Colors.GREEN}You:{Colors.ENDC} ").strip()
            except EOFError:
                # Handle Ctrl+D
                print()
                print_system_message("Session ended.")
                break
            
            # Skip empty input
            if not user_input:
                continue
            
            # Handle special commands
            command_result = handle_special_commands(user_input, agent)
            if command_result == "EXIT":
                break
            elif command_result == "CONTINUE":
                continue
            
            # Process input through agent
            try:
                response = agent.process_input(user_input)
                print_agent_response(response)
            except Exception as e:
                print_system_message(f"{Colors.RED}Error processing input: {e}{Colors.ENDC}")
                print_system_message("Please try again or type 'help' for assistance.")
    
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print()
        response = agent.process_input("goodbye")
        print_agent_response(response)
        print_system_message("Session interrupted. Goodbye! 👋")
    
    except Exception as e:
        # Handle unexpected errors
        print_system_message(f"{Colors.RED}Unexpected error: {e}{Colors.ENDC}")
        print_system_message("Session ended due to error.")
        sys.exit(1)


def main():
    """Main entry point for the CLI application."""
    run_interactive_session()


if __name__ == "__main__":
    main()

