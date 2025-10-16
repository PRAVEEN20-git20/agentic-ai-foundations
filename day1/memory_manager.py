"""
Memory Manager for Hello Advisor Agent

This module handles memory and state management for the agent,
including conversation history, user preferences, and context tracking.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json


class MemoryManager:
    """
    Manages agent memory including conversation history, user preferences,
    and contextual information across interactions.
    """

    def __init__(self, max_history_size: int = 50):
        """
        Initialize the memory manager.

        Args:
            max_history_size: Maximum number of conversation turns to retain
        """
        self.max_history_size = max_history_size
        self.conversation_history: List[Dict[str, Any]] = []
        self.user_preferences: Dict[str, Any] = {}
        self.context: Dict[str, Any] = {
            "session_start": datetime.now().isoformat(),
            "interaction_count": 0,
            "topics_discussed": set(),
        }

    def add_interaction(self, user_input: str, agent_response: str, 
                       metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Add a conversation turn to memory.

        Args:
            user_input: User's input text
            agent_response: Agent's response text
            metadata: Optional metadata about the interaction

        Side effects:
            Updates conversation_history and context
        """
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "agent_response": agent_response,
            "metadata": metadata or {}
        }
        
        self.conversation_history.append(interaction)
        self.context["interaction_count"] += 1

        # Prune history if it exceeds max size
        if len(self.conversation_history) > self.max_history_size:
            self.conversation_history.pop(0)

    def update_preference(self, key: str, value: Any) -> None:
        """
        Update a user preference.

        Args:
            key: Preference identifier
            value: Preference value

        Side effects:
            Updates user_preferences dictionary
        """
        self.user_preferences[key] = value

    def get_preference(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a user preference.

        Args:
            key: Preference identifier
            default: Default value if preference not found

        Returns:
            The preference value or default
        """
        return self.user_preferences.get(key, default)

    def add_topic(self, topic: str) -> None:
        """
        Track a discussion topic.

        Args:
            topic: Topic identifier

        Side effects:
            Updates context topics_discussed set
        """
        self.context["topics_discussed"].add(topic)

    def has_discussed_topic(self, topic: str) -> bool:
        """
        Check if a topic has been discussed.

        Args:
            topic: Topic identifier

        Returns:
            True if topic was discussed, False otherwise
        """
        return topic in self.context["topics_discussed"]

    def get_recent_history(self, count: int = 5) -> List[Dict[str, Any]]:
        """
        Get recent conversation history.

        Args:
            count: Number of recent interactions to retrieve

        Returns:
            List of recent interactions
        """
        return self.conversation_history[-count:]

    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current memory state.

        Returns:
            Dictionary containing memory statistics and state
        """
        return {
            "interaction_count": self.context["interaction_count"],
            "topics_discussed": list(self.context["topics_discussed"]),
            "preferences_set": len(self.user_preferences),
            "session_duration": self._calculate_session_duration(),
        }

    def _calculate_session_duration(self) -> str:
        """
        Calculate session duration.

        Returns:
            Human-readable session duration string
        """
        start = datetime.fromisoformat(self.context["session_start"])
        duration = datetime.now() - start
        minutes = int(duration.total_seconds() / 60)
        return f"{minutes} minute(s)"

    def clear(self) -> None:
        """
        Clear all memory (useful for testing or fresh starts).

        Side effects:
            Resets all memory structures to initial state
        """
        self.conversation_history.clear()
        self.user_preferences.clear()
        self.context = {
            "session_start": datetime.now().isoformat(),
            "interaction_count": 0,
            "topics_discussed": set(),
        }

    def export_memory(self) -> str:
        """
        Export memory to JSON format.

        Returns:
            JSON string representation of memory state
        """
        export_data = {
            "conversation_history": self.conversation_history,
            "user_preferences": self.user_preferences,
            "context": {
                **self.context,
                "topics_discussed": list(self.context["topics_discussed"])
            }
        }
        return json.dumps(export_data, indent=2)

    def import_memory(self, json_data: str) -> None:
        """
        Import memory from JSON format.

        Args:
            json_data: JSON string containing memory state

        Side effects:
            Replaces current memory with imported data
        """
        data = json.loads(json_data)
        self.conversation_history = data.get("conversation_history", [])
        self.user_preferences = data.get("user_preferences", {})
        context = data.get("context", {})
        self.context = {
            **context,
            "topics_discussed": set(context.get("topics_discussed", []))
        }

