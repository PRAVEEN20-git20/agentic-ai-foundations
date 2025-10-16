#!/usr/bin/env python3
"""
Quick Demo of Hello Advisor Agent

This script provides a quick demonstration of the agent's capabilities.
Run this to see the agent in action without entering the interactive CLI.
"""

from hello_advisor import HelloAdvisor
import time


def print_separator():
    """Print a visual separator."""
    print("\n" + "─" * 70 + "\n")


def simulate_conversation():
    """Simulate a natural conversation with the agent."""
    print("🤖" * 35)
    print("HELLO ADVISOR - QUICK DEMO")
    print("🤖" * 35)
    print("\nWatch as the agent demonstrates autonomy, memory, and reasoning!\n")
    
    agent = HelloAdvisor()
    
    # Conversation flow
    conversations = [
        ("Hello!", "👋 Starting with a friendly greeting"),
        ("My name is Alex", "📝 Teaching the agent my name"),
        ("What's your name?", "❓ Asking about the agent"),
        ("Tell me a programming joke", "😄 Requesting humor"),
        ("Hello again", "🔄 Notice: Should use my name now!"),
        ("What do you remember about me?", "🧠 Testing memory recall"),
        ("Tell me a science joke", "🔬 Requesting specific joke category"),
        ("summary", "📊 Checking session statistics"),
    ]
    
    for user_input, description in conversations:
        print_separator()
        print(f"💬 {description}")
        print(f"\n👤 User: {user_input}")
        
        # Small delay for dramatic effect
        time.sleep(0.3)
        
        response = agent.process_input(user_input)
        print(f"\n🤖 Hello Advisor:\n{response}")
        
        time.sleep(0.5)
    
    print_separator()
    print("\n✨ Demo Complete! ✨\n")
    print("Key Observations:")
    print("  1. 🤖 AUTONOMY: Agent chose appropriate responses without hardcoding")
    print("  2. 🧠 MEMORY: Agent remembered user's name across interactions")
    print("  3. 💭 REASONING: Agent understood context and intent from natural language")
    print("\nTo try the interactive version, run: python3 cli.py")
    print("To see more examples, run: python3 example_usage.py")
    print("To run tests, run: python3 test_agent.py\n")


if __name__ == "__main__":
    simulate_conversation()

