"""
Test script for Hello Advisor Agent

This script tests various scenarios to ensure the agent works correctly.
"""

from hello_advisor import HelloAdvisor


def print_test(test_name: str):
    """Print test header."""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print('='*60)


def print_interaction(user_input: str, response: str):
    """Print test interaction."""
    print(f"\n👤 User: {user_input}")
    print(f"🤖 Agent: {response}")


def test_greetings():
    """Test greeting functionality."""
    print_test("Greetings")
    agent = HelloAdvisor()
    
    test_inputs = ["hello", "Hi there!", "Good morning"]
    for user_input in test_inputs:
        response = agent.process_input(user_input)
        print_interaction(user_input, response)
        assert any(word in response.lower() for word in ["hello", "hi", "hey"]), \
            f"Expected greeting response, got: {response}"
    
    print("\n✅ Greeting tests passed!")


def test_jokes():
    """Test joke functionality."""
    print_test("Jokes")
    agent = HelloAdvisor()
    
    test_inputs = [
        "Tell me a joke",
        "Tell me a science joke",
        "Tell me a programming joke"
    ]
    
    for user_input in test_inputs:
        response = agent.process_input(user_input)
        print_interaction(user_input, response)
        assert len(response) > 10, f"Expected joke response, got: {response}"
    
    print("\n✅ Joke tests passed!")


def test_identity():
    """Test identity questions."""
    print_test("Identity Questions")
    agent = HelloAdvisor()
    
    test_inputs = [
        "Who are you?",
        "What are you?",
        "What's your name?"
    ]
    
    for user_input in test_inputs:
        response = agent.process_input(user_input)
        print_interaction(user_input, response)
        assert "advisor" in response.lower() or "agent" in response.lower(), \
            f"Expected identity response, got: {response}"
    
    print("\n✅ Identity tests passed!")


def test_memory():
    """Test memory functionality."""
    print_test("Memory and Personalization")
    agent = HelloAdvisor()
    
    # Set name
    response = agent.process_input("My name is Alice")
    print_interaction("My name is Alice", response)
    assert "Alice" in response, f"Expected name confirmation, got: {response}"
    
    # Greet with personalization
    response = agent.process_input("Hello")
    print_interaction("Hello", response)
    assert "Alice" in response, f"Expected personalized greeting, got: {response}"
    
    # Recall test
    response = agent.process_input("What do you know about me?")
    print_interaction("What do you know about me?", response)
    assert "Alice" in response, f"Expected name recall, got: {response}"
    
    print("\n✅ Memory tests passed!")


def test_capabilities():
    """Test capability questions."""
    print_test("Capabilities")
    agent = HelloAdvisor()
    
    response = agent.process_input("What can you do?")
    print_interaction("What can you do?", response)
    assert len(response) > 20, f"Expected capability description, got: {response}"
    
    print("\n✅ Capability tests passed!")


def test_help():
    """Test help functionality."""
    print_test("Help Command")
    agent = HelloAdvisor()
    
    response = agent.process_input("help")
    print_interaction("help", response)
    assert "joke" in response.lower() and "greeting" in response.lower(), \
        f"Expected help text, got: {response}"
    
    print("\n✅ Help tests passed!")


def test_summary():
    """Test session summary."""
    print_test("Session Summary")
    agent = HelloAdvisor()
    
    # Have some interactions
    agent.process_input("Hello")
    agent.process_input("Tell me a joke")
    agent.process_input("My name is Bob")
    
    response = agent.process_input("summary")
    print_interaction("summary", response)
    assert "interaction" in response.lower() or "session" in response.lower(), \
        f"Expected summary, got: {response}"
    
    print("\n✅ Summary tests passed!")


def test_farewell():
    """Test farewell functionality."""
    print_test("Farewell")
    agent = HelloAdvisor()
    
    # Have some interactions first
    agent.process_input("Hello")
    agent.process_input("My name is Charlie")
    
    response = agent.process_input("Goodbye")
    print_interaction("Goodbye", response)
    assert "bye" in response.lower() or "goodbye" in response.lower(), \
        f"Expected farewell, got: {response}"
    
    print("\n✅ Farewell tests passed!")


def test_memory_export():
    """Test memory export functionality."""
    print_test("Memory Export/Import")
    agent = HelloAdvisor()
    
    # Create some memory
    agent.process_input("Hello")
    agent.process_input("My name is David")
    agent.process_input("Tell me a joke")
    
    # Export memory
    memory_json = agent.get_memory_export()
    print(f"\n📤 Exported memory ({len(memory_json)} characters)")
    assert len(memory_json) > 50, "Expected substantial memory export"
    
    # Import into new agent
    new_agent = HelloAdvisor()
    new_agent.load_memory_import(memory_json)
    
    # Verify memory was imported by checking preference directly
    imported_name = new_agent.memory.get_preference("user_name")
    print(f"\n✅ Imported user name: {imported_name}")
    assert imported_name == "David", f"Expected imported name 'David', got: {imported_name}"
    
    # Verify personalized greeting works
    response = new_agent.process_input("Hello")
    print_interaction("Hello (after import)", response)
    assert "David" in response, f"Expected personalized greeting with imported name, got: {response}"
    
    print("\n✅ Memory export/import tests passed!")


def test_general_conversation():
    """Test general conversation handling."""
    print_test("General Conversation")
    agent = HelloAdvisor()
    
    # Test question handling
    response = agent.process_input("What's the weather like?")
    print_interaction("What's the weather like?", response)
    assert len(response) > 10, "Expected some response"
    
    # Test gratitude
    response = agent.process_input("Thank you!")
    print_interaction("Thank you!", response)
    assert "welcome" in response.lower(), f"Expected gratitude response, got: {response}"
    
    print("\n✅ General conversation tests passed!")


def run_all_tests():
    """Run all tests."""
    print("\n" + "🚀" * 30)
    print("HELLO ADVISOR AGENT - TEST SUITE")
    print("🚀" * 30)
    
    try:
        test_greetings()
        test_jokes()
        test_identity()
        test_memory()
        test_capabilities()
        test_help()
        test_summary()
        test_farewell()
        test_memory_export()
        test_general_conversation()
        
        print("\n" + "="*60)
        print("🎉 ALL TESTS PASSED! 🎉")
        print("="*60)
        print("\nThe Hello Advisor agent is working correctly!")
        print("Try it out with: python3 cli.py")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

