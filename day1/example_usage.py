"""
Example Usage of Hello Advisor Agent

This script demonstrates programmatic usage of the Hello Advisor agent
with various interaction patterns.
"""

from hello_advisor import HelloAdvisor


def example_basic_conversation():
    """Example of basic conversation."""
    print("="*60)
    print("EXAMPLE 1: Basic Conversation")
    print("="*60)
    
    agent = HelloAdvisor()
    
    # Greeting
    response = agent.process_input("Hello!")
    print(f"User: Hello!")
    print(f"Agent: {response}\n")
    
    # Ask about capabilities
    response = agent.process_input("What can you do?")
    print(f"User: What can you do?")
    print(f"Agent: {response}\n")
    
    # Request a joke
    response = agent.process_input("Tell me a programming joke")
    print(f"User: Tell me a programming joke")
    print(f"Agent: {response}\n")


def example_personalized_conversation():
    """Example of personalized conversation with memory."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Personalized Conversation with Memory")
    print("="*60)
    
    agent = HelloAdvisor()
    
    # Introduce yourself
    response = agent.process_input("My name is Sarah")
    print(f"User: My name is Sarah")
    print(f"Agent: {response}\n")
    
    # Greet again - should be personalized
    response = agent.process_input("Hello")
    print(f"User: Hello")
    print(f"Agent: {response}\n")
    
    # Ask for recall
    response = agent.process_input("What do you remember about me?")
    print(f"User: What do you remember about me?")
    print(f"Agent: {response}\n")
    
    # Check session summary
    response = agent.process_input("summary")
    print(f"User: summary")
    print(f"Agent: {response}\n")


def example_multi_category_jokes():
    """Example of requesting different joke categories."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Different Joke Categories")
    print("="*60)
    
    agent = HelloAdvisor()
    
    # Science joke
    response = agent.process_input("Tell me a science joke")
    print(f"User: Tell me a science joke")
    print(f"Agent: {response}\n")
    
    # Programming joke
    response = agent.process_input("Tell me a programming joke")
    print(f"User: Tell me a programming joke")
    print(f"Agent: {response}\n")
    
    # General joke
    response = agent.process_input("Tell me something funny")
    print(f"User: Tell me something funny")
    print(f"Agent: {response}\n")


def example_memory_persistence():
    """Example of memory export and import."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Memory Persistence (Export/Import)")
    print("="*60)
    
    # Create agent with some history
    agent1 = HelloAdvisor()
    agent1.process_input("Hello")
    agent1.process_input("My name is Alex")
    agent1.process_input("Tell me a joke")
    agent1.process_input("Tell me another joke")
    
    print("Agent 1 created some conversation history...")
    
    # Export memory
    memory_json = agent1.get_memory_export()
    print(f"Exported memory: {len(memory_json)} characters\n")
    
    # Create new agent and import memory
    agent2 = HelloAdvisor()
    agent2.load_memory_import(memory_json)
    print("Created Agent 2 and imported memory from Agent 1\n")
    
    # Test that memory was preserved
    response = agent2.process_input("Hello")
    print(f"User: Hello")
    print(f"Agent 2: {response}")
    print("(Notice the personalized greeting with remembered name!)\n")
    
    # Check what's remembered
    response = agent2.process_input("What do you know about me?")
    print(f"User: What do you know about me?")
    print(f"Agent 2: {response}\n")


def example_context_awareness():
    """Example showing context awareness and reasoning."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Context Awareness and Reasoning")
    print("="*60)
    
    agent = HelloAdvisor()
    
    # Build context
    interactions = [
        "Hello",
        "My name is Jordan",
        "Tell me a joke",
        "Tell me a science joke",
        "What do you remember about me?",
        "summary",
    ]
    
    for user_input in interactions:
        response = agent.process_input(user_input)
        print(f"User: {user_input}")
        print(f"Agent: {response}\n")
        print("-" * 60 + "\n")


def example_help_and_guidance():
    """Example of getting help and guidance."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Getting Help")
    print("="*60)
    
    agent = HelloAdvisor()
    
    response = agent.process_input("help")
    print(f"User: help")
    print(f"Agent: {response}\n")


def main():
    """Run all examples."""
    print("\n" + "🤖"*30)
    print("HELLO ADVISOR - EXAMPLE USAGE DEMONSTRATIONS")
    print("🤖"*30 + "\n")
    
    example_basic_conversation()
    example_personalized_conversation()
    example_multi_category_jokes()
    example_memory_persistence()
    example_context_awareness()
    example_help_and_guidance()
    
    print("\n" + "="*60)
    print("✨ Examples completed!")
    print("="*60)
    print("\nTo try the interactive CLI, run: python3 cli.py")
    print("To run tests, run: python3 test_agent.py")


if __name__ == "__main__":
    main()

