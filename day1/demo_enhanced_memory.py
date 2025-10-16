#!/usr/bin/env python3
"""
Enhanced Memory Demo - Hello Advisor Agent

This script demonstrates the enhanced memory capabilities of the agent,
showing how it can remember names, preferences, loves, likes, favorites, and more.
"""

from hello_advisor import HelloAdvisor
import time


def print_separator():
    """Print a visual separator."""
    print("\n" + "─" * 70 + "\n")


def simulate_enhanced_memory_conversation():
    """Simulate a conversation showcasing enhanced memory features."""
    print("🧠" * 35)
    print("HELLO ADVISOR - ENHANCED MEMORY DEMO")
    print("🧠" * 35)
    print("\nWatch as the agent remembers various types of information!\n")
    
    agent = HelloAdvisor()
    
    # Conversation flow showcasing different memory types
    conversations = [
        ("Hello!", "👋 Starting the conversation"),
        ("My name is Emma", "📝 Telling the agent my name"),
        ("I love reading books", "❤️  Sharing something I love"),
        ("I really love traveling to new places", "❤️  Sharing another love"),
        ("I like hiking", "👍 Sharing something I like"),
        ("I enjoy cooking Italian food", "👍 Sharing another like"),
        ("My favorite color is purple", "⭐ Sharing favorite color"),
        ("My favorite movie is Inception", "⭐ Sharing favorite movie"),
        ("I prefer coffee over tea", "✨ Sharing a preference"),
        ("I'm interested in machine learning", "🎯 Sharing an interest"),
        ("I don't like cold weather", "👎 Sharing a dislike"),
        ("Hello again", "🔄 Greeting again (should use name)"),
        ("What do you know about me?", "🧠 Testing complete recall"),
    ]
    
    for user_input, description in conversations:
        print_separator()
        print(f"💬 {description}")
        print(f"\n👤 User: {user_input}")
        
        # Small delay for dramatic effect
        time.sleep(0.4)
        
        response = agent.process_input(user_input)
        print(f"\n🤖 Hello Advisor:\n{response}")
        
        time.sleep(0.6)
    
    print_separator()
    print("\n✨ Demo Complete! ✨\n")
    print("Key Observations:")
    print("  1. 🤖 AUTONOMY: Agent automatically categorized different types of information")
    print("  2. 🧠 MEMORY: Agent stored and organized 7 different types of data:")
    print("     - Name (Emma)")
    print("     - 2 Loves (reading books, traveling)")
    print("     - 2 Likes (hiking, cooking Italian food)")
    print("     - 2 Favorites (color: purple, movie: Inception)")
    print("     - 1 Preference (coffee over tea)")
    print("     - 1 Interest (machine learning)")
    print("     - 1 Dislike (cold weather)")
    print("  3. 💭 REASONING: Agent used stored name in personalized greeting")
    print("  4. 📊 ORGANIZATION: Information is categorized and well-structured")
    print("\nTry the interactive version: python3 cli.py")
    print("Share your own preferences and see what it remembers!\n")


def demonstrate_memory_types():
    """Demonstrate each memory type individually."""
    print_separator()
    print("📚 MEMORY TYPES SUPPORTED:\n")
    
    examples = [
        ("👤 Name", "My name is John", "Stores your identity"),
        ("❤️  Loves", "I love pizza", "Things you're passionate about"),
        ("👍 Likes", "I like photography", "Things you enjoy"),
        ("⭐ Favorites", "My favorite book is 1984", "Your top picks by category"),
        ("✨ Preferences", "I prefer working remotely", "Your personal preferences"),
        ("🎯 Interests", "I'm interested in AI", "Topics you're curious about"),
        ("👎 Dislikes", "I don't like spicy food", "Things you avoid"),
    ]
    
    for emoji_type, example, description in examples:
        print(f"{emoji_type}")
        print(f"  Example: \"{example}\"")
        print(f"  Purpose: {description}\n")
    
    print("💡 The agent can extract and remember all these from natural conversation!")


def main():
    """Main entry point for the demo."""
    print("\n" + "🎨"*35)
    print("ENHANCED MEMORY DEMONSTRATION")
    print("🎨"*35 + "\n")
    
    simulate_enhanced_memory_conversation()
    demonstrate_memory_types()
    
    print("\n" + "="*70)
    print("✨ Try it yourself!")
    print("="*70)
    print("\nRun: python3 cli.py")
    print("\nThen share things about yourself:")
    print("  - Tell it your name")
    print("  - Share what you love")
    print("  - Mention your favorites")
    print("  - Express your preferences")
    print("  - Discuss your interests")
    print("\nThen ask: 'What do you know about me?'")
    print("Watch as the agent recalls everything perfectly! 🎯\n")


if __name__ == "__main__":
    main()

