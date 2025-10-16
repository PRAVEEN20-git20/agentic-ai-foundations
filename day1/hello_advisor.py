"""
Hello Advisor - Enhanced Rule-Based Chat Agent

This module implements an AI agent with autonomy, memory, and reasoning
capabilities. The agent can handle greetings, tell jokes, answer questions,
remember user preferences, and maintain conversation context.
"""

from typing import Tuple, Dict, Any, Optional
import random
import re
from memory_manager import MemoryManager


class HelloAdvisor:
    """
    An intelligent chat agent with memory and reasoning capabilities.
    
    The agent demonstrates:
    - Autonomy: Makes decisions on how to respond based on input analysis
    - Memory: Remembers user preferences and conversation history
    - Reasoning: Uses context and patterns to provide appropriate responses
    """

    def __init__(self):
        """Initialize the Hello Advisor agent with memory and knowledge base."""
        self.memory = MemoryManager(max_history_size=50)
        self.name = "Hello Advisor"
        
        # Knowledge base for jokes (categorized)
        self.jokes = {
            "science": [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the physicist break up with the biologist? There was no chemistry!",
                "Parallel lines have so much in common. It's a shame they'll never meet.",
            ],
            "programming": [
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "There are 10 types of people: those who understand binary and those who don't.",
                "Why do Java developers wear glasses? Because they don't C#!",
            ],
            "general": [
                "Why don't eggs tell jokes? They'd crack each other up!",
                "What do you call a bear with no teeth? A gummy bear!",
                "Why did the scarecrow win an award? He was outstanding in his field!",
            ]
        }
        
        # Knowledge base for facts
        self.facts = {
            "agent": "I'm Hello Advisor, an AI agent with autonomy, memory, and reasoning capabilities.",
            "purpose": "I'm here to chat with you, answer questions, tell jokes, and remember our conversations!",
            "capabilities": "I can greet you, tell jokes, remember your preferences (name, likes, loves, favorites, interests, dislikes), track our conversation, and provide helpful responses. I'll remember everything you tell me about yourself!",
        }

    def process_input(self, user_input: str) -> str:
        """
        Main entry point for processing user input.
        
        This method demonstrates agent autonomy by analyzing input and
        deciding on the appropriate response strategy.

        Args:
            user_input: The user's input text

        Returns:
            The agent's response text

        Side effects:
            Updates memory with the interaction
        """
        # Normalize input
        user_input_lower = user_input.lower().strip()
        
        # Reasoning: Analyze input to determine intent and response strategy
        intent = self._analyze_intent(user_input_lower)
        
        # Autonomy: Decide on response based on analyzed intent
        response = self._generate_response(intent, user_input, user_input_lower)
        
        # Memory: Store the interaction
        self.memory.add_interaction(
            user_input=user_input,
            agent_response=response,
            metadata={"intent": intent}
        )
        
        return response

    def _analyze_intent(self, user_input_lower: str) -> str:
        """
        Analyze user input to determine intent (reasoning component).

        Args:
            user_input_lower: Normalized lowercase user input

        Returns:
            Intent category string
        """
        # Check for memory/preference commands FIRST (before greetings)
        # This prevents "I love" from being confused with positive emotions
        preference_patterns = [
            "my name is", "i love", "i like", "i enjoy", 
            "my favorite", "i prefer", "i'm interested in", "i hate", 
            "i dislike", "i don't like", "call me", "i am interested",
            "i really love", "i really like", "i absolutely love"
        ]
        if any(pattern in user_input_lower for pattern in preference_patterns):
            return "remember"
        
        # Generic "remember" command (after specific patterns)
        if user_input_lower.startswith("remember") or user_input_lower == "remember":
            return "remember"
        
        # Check for recall questions
        if "do you remember" in user_input_lower or "what do you know about me" in user_input_lower:
            return "recall"
        
        # Check for greetings
        greetings = ["hello", "hi", "hey", "greetings", "good morning", 
                    "good afternoon", "good evening"]
        if any(greeting in user_input_lower for greeting in greetings):
            return "greeting"
        
        # Check for farewells
        farewells = ["bye", "goodbye", "see you", "farewell", "exit", "quit"]
        if any(farewell in user_input_lower for farewell in farewells):
            return "farewell"
        
        # Check for joke requests
        joke_keywords = ["joke", "funny", "laugh", "humor", "something funny"]
        if any(keyword in user_input_lower for keyword in joke_keywords):
            return "joke_request"
        
        # Check for identity questions
        identity_keywords = ["who are you", "what are you", "your name", 
                           "who is", "what is your"]
        if any(keyword in user_input_lower for keyword in identity_keywords):
            return "identity"
        
        # Check for capability questions
        capability_keywords = ["what can you", "how can you help", "what do you do",
                              "your capabilities", "can you"]
        if any(keyword in user_input_lower for keyword in capability_keywords):
            return "capabilities"
        
        # Check for help requests
        if "help" in user_input_lower or "what can i ask" in user_input_lower:
            return "help"
        
        # Check for memory status
        if "summary" in user_input_lower or "session info" in user_input_lower:
            return "memory_summary"
        
        # Default to general conversation
        return "general"

    def _generate_response(self, intent: str, original_input: str, 
                          normalized_input: str) -> str:
        """
        Generate appropriate response based on intent (autonomy component).

        Args:
            intent: Determined intent category
            original_input: Original user input
            normalized_input: Normalized lowercase input

        Returns:
            Generated response string
        """
        # Personalization: Use user's name if known
        user_name = self.memory.get_preference("user_name", "")
        greeting_suffix = f", {user_name}" if user_name else ""
        
        if intent == "greeting":
            self.memory.add_topic("greeting")
            greetings = [
                f"Hello{greeting_suffix}! How can I assist you today?",
                f"Hi there{greeting_suffix}! Great to see you!",
                f"Hey{greeting_suffix}! What can I do for you?",
            ]
            return random.choice(greetings)
        
        elif intent == "farewell":
            interaction_count = self.memory.context["interaction_count"]
            return f"Goodbye{greeting_suffix}! It was great chatting with you. We had {interaction_count} interactions. See you next time!"
        
        elif intent == "joke_request":
            self.memory.add_topic("jokes")
            return self._tell_joke(normalized_input)
        
        elif intent == "identity":
            self.memory.add_topic("identity")
            return self.facts["agent"]
        
        elif intent == "capabilities":
            self.memory.add_topic("capabilities")
            return self.facts["capabilities"]
        
        elif intent == "remember":
            return self._handle_remember(original_input)
        
        elif intent == "recall":
            return self._handle_recall()
        
        elif intent == "help":
            return self._provide_help()
        
        elif intent == "memory_summary":
            return self._provide_summary()
        
        else:  # general
            return self._handle_general_conversation(normalized_input)

    def _tell_joke(self, user_input: str) -> str:
        """
        Tell a joke, optionally from a specific category.

        Args:
            user_input: Normalized user input

        Returns:
            A joke string
        """
        # Check if user requested a specific category
        category = "general"
        if "science" in user_input or "scientist" in user_input:
            category = "science"
        elif "programming" in user_input or "coding" in user_input or "developer" in user_input:
            category = "programming"
        
        joke = random.choice(self.jokes[category])
        return f"{joke}\n\n😄 Hope that made you smile!"

    def _handle_remember(self, user_input: str) -> str:
        """
        Handle requests to remember information.

        Args:
            user_input: Original user input

        Returns:
            Confirmation response

        Side effects:
            Updates memory preferences
        """
        user_input_lower = user_input.lower()
        stored_items = []
        
        # Extract name if present (but not when followed by "interested")
        name_pattern = r"(?:my name is|call me)\s+(\w+)"
        match = re.search(name_pattern, user_input_lower)
        
        if match:
            name = match.group(1).capitalize()
            self.memory.update_preference("user_name", name)
            self.memory.add_topic("personal_info")
            stored_items.append(f"your name ({name})")
        
        # Extract things they love
        love_patterns = [
            r"i love ([^,.!?]+)",
            r"i really love ([^,.!?]+)",
            r"i absolutely love ([^,.!?]+)"
        ]
        for pattern in love_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                loved_thing = match.group(1).strip()
                # Get existing loves or create new list
                loves = self.memory.get_preference("loves", [])
                if not isinstance(loves, list):
                    loves = []
                if loved_thing not in loves:
                    loves.append(loved_thing)
                    self.memory.update_preference("loves", loves)
                    stored_items.append(f"you love {loved_thing}")
                break
        
        # Extract things they like
        like_patterns = [
            r"i like ([^,.!?]+)",
            r"i really like ([^,.!?]+)",
            r"i enjoy ([^,.!?]+)"
        ]
        for pattern in like_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                liked_thing = match.group(1).strip()
                likes = self.memory.get_preference("likes", [])
                if not isinstance(likes, list):
                    likes = []
                if liked_thing not in likes:
                    likes.append(liked_thing)
                    self.memory.update_preference("likes", likes)
                    stored_items.append(f"you like {liked_thing}")
                break
        
        # Extract favorite things
        favorite_pattern = r"my favorite (\w+) is ([^,.!?]+)"
        match = re.search(favorite_pattern, user_input_lower)
        if match:
            category = match.group(1).strip()
            favorite = match.group(2).strip()
            favorites = self.memory.get_preference("favorites", {})
            if not isinstance(favorites, dict):
                favorites = {}
            favorites[category] = favorite
            self.memory.update_preference("favorites", favorites)
            stored_items.append(f"your favorite {category} is {favorite}")
        
        # Extract preferences (prefer X over Y)
        prefer_pattern = r"i prefer ([^,.!?]+)"
        match = re.search(prefer_pattern, user_input_lower)
        if match:
            preference = match.group(1).strip()
            preferences = self.memory.get_preference("preferences", [])
            if not isinstance(preferences, list):
                preferences = []
            if preference not in preferences:
                preferences.append(preference)
                self.memory.update_preference("preferences", preferences)
                stored_items.append(f"you prefer {preference}")
        
        # Extract dislikes
        dislike_patterns = [
            r"i (?:hate|dislike|don't like) ([^,.!?]+)",
            r"i really (?:hate|dislike|don't like) ([^,.!?]+)"
        ]
        for pattern in dislike_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                disliked_thing = match.group(1).strip()
                dislikes = self.memory.get_preference("dislikes", [])
                if not isinstance(dislikes, list):
                    dislikes = []
                if disliked_thing not in dislikes:
                    dislikes.append(disliked_thing)
                    self.memory.update_preference("dislikes", dislikes)
                    stored_items.append(f"you dislike {disliked_thing}")
                break
        
        # Extract interests
        interest_patterns = [
            r"i'm interested in ([^,.!?]+)",
            r"i am interested in ([^,.!?]+)"
        ]
        for pattern in interest_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                interest = match.group(1).strip()
                interests = self.memory.get_preference("interests", [])
                if not isinstance(interests, list):
                    interests = []
                if interest not in interests:
                    interests.append(interest)
                    self.memory.update_preference("interests", interests)
                    stored_items.append(f"you're interested in {interest}")
                break
        
        # Build response based on what was stored
        if stored_items:
            if len(stored_items) == 1:
                return f"Got it! I'll remember that {stored_items[0]}. 📝"
            else:
                items_text = ", ".join(stored_items[:-1]) + f" and {stored_items[-1]}"
                return f"Got it! I'll remember that {items_text}. 📝"
        
        # Generic remember request with examples
        return ("I can remember many things about you! Try telling me:\n"
                "- Your name: 'My name is...'\n"
                "- Things you love: 'I love...'\n"
                "- Things you like: 'I like...'\n"
                "- Your favorites: 'My favorite [thing] is...'\n"
                "- Your preferences: 'I prefer...'\n"
                "- Your interests: 'I'm interested in...'\n"
                "- Things you dislike: 'I don't like...'")


    def _handle_recall(self) -> str:
        """
        Handle requests to recall stored information.

        Returns:
            Summary of remembered information
        """
        user_name = self.memory.get_preference("user_name")
        loves = self.memory.get_preference("loves", [])
        likes = self.memory.get_preference("likes", [])
        favorites = self.memory.get_preference("favorites", {})
        preferences = self.memory.get_preference("preferences", [])
        dislikes = self.memory.get_preference("dislikes", [])
        interests = self.memory.get_preference("interests", [])
        topics = list(self.memory.context["topics_discussed"])
        interaction_count = self.memory.context["interaction_count"]
        
        response_parts = ["Let me share what I remember about you:"]
        
        # Personal info
        if user_name:
            response_parts.append(f"\n👤 **Personal:**")
            response_parts.append(f"  - Your name is {user_name}")
        
        # Loves
        if loves:
            if not user_name:  # Add section header if we didn't add it above
                response_parts.append(f"\n❤️  **You Love:**")
            else:
                response_parts.append(f"\n❤️  **Things You Love:**")
            for love in loves:
                response_parts.append(f"  - {love}")
        
        # Likes
        if likes:
            response_parts.append(f"\n👍 **Things You Like:**")
            for like in likes:
                response_parts.append(f"  - {like}")
        
        # Favorites
        if favorites:
            response_parts.append(f"\n⭐ **Your Favorites:**")
            for category, favorite in favorites.items():
                response_parts.append(f"  - Favorite {category}: {favorite}")
        
        # Preferences
        if preferences:
            response_parts.append(f"\n✨ **Your Preferences:**")
            for pref in preferences:
                response_parts.append(f"  - {pref}")
        
        # Interests
        if interests:
            response_parts.append(f"\n🎯 **Your Interests:**")
            for interest in interests:
                response_parts.append(f"  - {interest}")
        
        # Dislikes
        if dislikes:
            response_parts.append(f"\n👎 **Things You Dislike:**")
            for dislike in dislikes:
                response_parts.append(f"  - {dislike}")
        
        # Session info
        response_parts.append(f"\n📊 **Session Info:**")
        if topics:
            response_parts.append(f"  - Topics discussed: {', '.join(topics)}")
        response_parts.append(f"  - Interactions: {interaction_count}")
        
        # Check if we have any personal information stored
        has_personal_info = any([user_name, loves, likes, favorites, preferences, dislikes, interests])
        if not has_personal_info:
            return ("I don't have any personal information about you yet! "
                   "Tell me about yourself - what you love, like, or your favorite things. "
                   "I'll remember it all! 😊")
        
        return "\n".join(response_parts)

    def _provide_help(self) -> str:
        """
        Provide help information about what the agent can do.

        Returns:
            Help text
        """
        help_text = """
Here's what I can help you with:

🗣️  **Greetings**: Say hello and I'll greet you back!
😄 **Jokes**: Ask me for a joke (try science, programming, or general jokes)
❓ **Questions**: Ask about me, my capabilities, or purpose
💭 **Memory**: I can remember lots about you!
   - Your name: "My name is..."
   - Things you love: "I love..."
   - Things you like: "I like..."
   - Your favorites: "My favorite [thing] is..."
   - Your preferences: "I prefer..."
   - Your interests: "I'm interested in..."
   - Things you dislike: "I don't like..."
🧠 **Recall**: Ask "What do you know about me?" to see everything I remember
📊 **Summary**: Ask for a session summary to see our conversation stats
👋 **Farewell**: Say goodbye when you're ready to end our chat

Try sharing things about yourself - I'll remember it all!
        """.strip()
        return help_text

    def _provide_summary(self) -> str:
        """
        Provide a summary of the current session.

        Returns:
            Session summary text
        """
        summary = self.memory.get_summary()
        
        summary_text = f"""
📊 **Session Summary**

- Interactions: {summary['interaction_count']}
- Topics discussed: {', '.join(summary['topics_discussed']) if summary['topics_discussed'] else 'None yet'}
- Preferences stored: {summary['preferences_set']}
- Session duration: {summary['session_duration']}

Keep chatting to build more memories!
        """.strip()
        return summary_text

    def _handle_general_conversation(self, user_input: str) -> str:
        """
        Handle general conversation that doesn't fit specific intents.

        Args:
            user_input: Normalized user input

        Returns:
            Response text
        """
        # Check for questions
        if "?" in user_input:
            return "That's an interesting question! I'm still learning. For now, try asking about me, request a joke, or tell me your name!"
        
        # Check for expressions of emotion
        positive_emotions = ["thanks", "thank you", "awesome", "great", "love", "good"]
        if any(emotion in user_input for emotion in positive_emotions):
            return "You're very welcome! I'm happy to help. What else can I do for you?"
        
        # Default response with helpful guidance
        responses = [
            "I'm here to help! You can ask me for a joke, questions about me, or tell me your name.",
            "I'm not sure how to respond to that yet, but I'm learning! Try asking for help to see what I can do.",
            "Interesting! I'm still expanding my knowledge. Ask me for a joke or tell me about yourself!",
        ]
        return random.choice(responses)

    def get_memory_export(self) -> str:
        """
        Export current memory state.

        Returns:
            JSON string of memory state
        """
        return self.memory.export_memory()

    def load_memory_import(self, json_data: str) -> None:
        """
        Import memory state from JSON.

        Args:
            json_data: JSON string containing memory state

        Side effects:
            Replaces current memory with imported data
        """
        self.memory.import_memory(json_data)

