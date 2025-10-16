"""
Test script for enhanced memory features

This script tests the new capability to remember user preferences,
loves, likes, favorites, interests, and dislikes.
"""

from hello_advisor import HelloAdvisor


def print_test(test_name: str):
    """Print test header."""
    print(f"\n{'='*70}")
    print(f"TEST: {test_name}")
    print('='*70)


def print_interaction(user_input: str, response: str):
    """Print test interaction."""
    print(f"\n👤 User: {user_input}")
    print(f"🤖 Agent: {response}")


def test_enhanced_memory():
    """Test all enhanced memory features."""
    print_test("Enhanced Memory Features")
    agent = HelloAdvisor()
    
    # Test name memory
    response = agent.process_input("My name is Sarah")
    print_interaction("My name is Sarah", response)
    assert "Sarah" in response, f"Expected name confirmation, got: {response}"
    
    # Test loves
    response = agent.process_input("I love pizza")
    print_interaction("I love pizza", response)
    assert "love" in response.lower() and "pizza" in response.lower(), \
        f"Expected love confirmation, got: {response}"
    
    response = agent.process_input("I really love traveling")
    print_interaction("I really love traveling", response)
    assert "love" in response.lower() and "traveling" in response.lower(), \
        f"Expected love confirmation, got: {response}"
    
    # Test likes
    response = agent.process_input("I like reading books")
    print_interaction("I like reading books", response)
    assert "like" in response.lower() and "reading books" in response.lower(), \
        f"Expected like confirmation, got: {response}"
    
    response = agent.process_input("I enjoy coding")
    print_interaction("I enjoy coding", response)
    assert "like" in response.lower() and "coding" in response.lower(), \
        f"Expected like confirmation, got: {response}"
    
    # Test favorites
    response = agent.process_input("My favorite color is blue")
    print_interaction("My favorite color is blue", response)
    assert "favorite" in response.lower() and "blue" in response.lower(), \
        f"Expected favorite confirmation, got: {response}"
    
    response = agent.process_input("My favorite food is sushi")
    print_interaction("My favorite food is sushi", response)
    assert "favorite" in response.lower() and "sushi" in response.lower(), \
        f"Expected favorite confirmation, got: {response}"
    
    # Test preferences
    response = agent.process_input("I prefer tea over coffee")
    print_interaction("I prefer tea over coffee", response)
    assert "prefer" in response.lower() and "tea over coffee" in response.lower(), \
        f"Expected preference confirmation, got: {response}"
    
    # Test interests
    response = agent.process_input("I'm interested in artificial intelligence")
    print_interaction("I'm interested in artificial intelligence", response)
    assert "interested" in response.lower() and "artificial intelligence" in response.lower(), \
        f"Expected interest confirmation, got: {response}"
    
    # Test dislikes
    response = agent.process_input("I don't like cold weather")
    print_interaction("I don't like cold weather", response)
    assert "dislike" in response.lower() and "cold weather" in response.lower(), \
        f"Expected dislike confirmation, got: {response}"
    
    # Test recall - should show everything
    response = agent.process_input("What do you know about me?")
    print_interaction("What do you know about me?", response)
    
    # Verify all information is in the recall
    expected_items = [
        "Sarah", "pizza", "traveling", "reading books", "coding",
        "blue", "sushi", "tea over coffee", "artificial intelligence",
        "cold weather"
    ]
    
    for item in expected_items:
        assert item in response, f"Expected '{item}' in recall, got: {response}"
    
    print("\n✅ All enhanced memory tests passed!")
    print("\n📊 Stored Information:")
    print(response)


def test_multiple_items_same_category():
    """Test storing multiple items in the same category."""
    print_test("Multiple Items in Same Category")
    agent = HelloAdvisor()
    
    # Add multiple loves
    agent.process_input("I love basketball")
    agent.process_input("I love swimming")
    agent.process_input("I love music")
    
    response = agent.process_input("What do you know about me?")
    print_interaction("What do you know about me?", response)
    
    # Verify all loves are stored
    assert "basketball" in response, "Expected basketball in recall"
    assert "swimming" in response, "Expected swimming in recall"
    assert "music" in response, "Expected music in recall"
    
    print("\n✅ Multiple items test passed!")


def test_duplicate_prevention():
    """Test that duplicate items aren't stored multiple times."""
    print_test("Duplicate Prevention")
    agent = HelloAdvisor()
    
    # Try to add the same love twice
    agent.process_input("I love chocolate")
    agent.process_input("I love chocolate")  # Same thing again
    
    # Check memory directly
    loves = agent.memory.get_preference("loves", [])
    chocolate_count = loves.count("chocolate")
    
    print(f"\n📝 'chocolate' appears {chocolate_count} time(s) in loves list")
    assert chocolate_count == 1, f"Expected chocolate to appear once, but found {chocolate_count} times"
    
    print("\n✅ Duplicate prevention test passed!")


def test_complex_sentence():
    """Test storing multiple things from one sentence."""
    print_test("Complex Sentence with Multiple Items")
    agent = HelloAdvisor()
    
    # This should store both name and a love
    response = agent.process_input("My name is Alex and I love hiking")
    print_interaction("My name is Alex and I love hiking", response)
    
    # Both should be stored
    recall = agent.process_input("What do you know about me?")
    print_interaction("What do you know about me?", recall)
    
    assert "Alex" in recall, "Expected name in recall"
    assert "hiking" in recall, "Expected hiking in recall"
    
    print("\n✅ Complex sentence test passed!")


def test_recall_empty_memory():
    """Test recall when no personal information is stored."""
    print_test("Recall with Empty Memory")
    agent = HelloAdvisor()
    
    response = agent.process_input("What do you know about me?")
    print_interaction("What do you know about me?", response)
    
    assert "don't have any personal information" in response.lower() or \
           "tell me about yourself" in response.lower(), \
        f"Expected empty memory message, got: {response}"
    
    print("\n✅ Empty memory test passed!")


def test_remember_help():
    """Test the help message for remembering."""
    print_test("Remember Help Message")
    agent = HelloAdvisor()
    
    response = agent.process_input("remember")
    print_interaction("remember", response)
    
    # Should provide examples of what can be remembered
    assert "name" in response.lower() and "love" in response.lower(), \
        f"Expected help with examples, got: {response}"
    
    print("\n✅ Remember help test passed!")


def run_all_tests():
    """Run all enhanced memory tests."""
    print("\n" + "🧠" * 35)
    print("ENHANCED MEMORY FEATURES - TEST SUITE")
    print("🧠" * 35)
    
    try:
        test_enhanced_memory()
        test_multiple_items_same_category()
        test_duplicate_prevention()
        test_complex_sentence()
        test_recall_empty_memory()
        test_remember_help()
        
        print("\n" + "="*70)
        print("🎉 ALL ENHANCED MEMORY TESTS PASSED! 🎉")
        print("="*70)
        print("\nThe agent can now remember:")
        print("  ✅ Names")
        print("  ✅ Things users love")
        print("  ✅ Things users like")
        print("  ✅ Favorite items (by category)")
        print("  ✅ Preferences")
        print("  ✅ Interests")
        print("  ✅ Dislikes")
        print("\nTry it out with: python3 cli.py")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

