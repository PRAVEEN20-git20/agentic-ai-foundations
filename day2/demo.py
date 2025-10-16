"""
Quick Demo of Document Q&A Agent

A simplified demo script that shows the core functionality without needing PDFs.
Uses mock data to demonstrate the agent's capabilities.
"""

import os
from doc_qa_agent import DocumentQAAgent


def print_section(title: str):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def demo_agent_initialization():
    """Demo: Initialize the agent."""
    print_section("1. Agent Initialization")
    
    try:
        agent = DocumentQAAgent()
        print("✓ Document Q&A Agent initialized successfully!")
        print(f"  - Agent name: {agent.name}")
        print(f"  - Ready to process documents and answer questions")
        return agent
    except ValueError as e:
        print(f"✗ Error: {str(e)}")
        print("\n💡 Tip: Set OPENAI_API_KEY in your .env file")
        return None


def demo_agent_capabilities(agent: DocumentQAAgent):
    """Demo: Show agent capabilities."""
    print_section("2. Agent Capabilities")
    
    print("The agent can:")
    print("  ✓ Load and process PDF documents")
    print("  ✓ Create vector embeddings for efficient search")
    print("  ✓ Answer questions using RAG (Retrieval-Augmented Generation)")
    print("  ✓ Cite sources with page numbers")
    print("  ✓ Handle multiple documents simultaneously")
    print("  ✓ Save and load vector stores for reuse")
    print("  ✓ Maintain conversation history")


def demo_status_check(agent: DocumentQAAgent):
    """Demo: Check agent status."""
    print_section("3. Status Check")
    
    status = agent.get_status()
    print(status)


def demo_help_system(agent: DocumentQAAgent):
    """Demo: Show help information."""
    print_section("4. Help System")
    
    help_text = agent.get_help()
    print(help_text)


def demo_conversational_interaction(agent: DocumentQAAgent):
    """Demo: Conversational interactions."""
    print_section("5. Conversational Interaction")
    
    messages = [
        "Hello!",
        "What can you do?",
        "How do I load documents?",
    ]
    
    for message in messages:
        print(f"User: {message}")
        response = agent.chat(message)
        print(f"Agent: {response}\n")


def demo_document_loading_info(agent: DocumentQAAgent):
    """Demo: Information about document loading."""
    print_section("6. Document Loading (Information)")
    
    print("To use the Q&A functionality, you need to load PDF documents:")
    print()
    print("Programmatic usage:")
    print("  agent.load_document('path/to/document.pdf')")
    print()
    print("CLI usage:")
    print("  load path/to/document.pdf")
    print()
    print("Multiple documents:")
    print("  agent.load_multiple_documents(['doc1.pdf', 'doc2.pdf'])")
    print()
    print("The agent will:")
    print("  1. Extract text from the PDF")
    print("  2. Split text into chunks")
    print("  3. Create embeddings for each chunk")
    print("  4. Store embeddings in a FAISS vector index")


def demo_qa_workflow(agent: DocumentQAAgent):
    """Demo: Q&A workflow explanation."""
    print_section("7. Q&A Workflow")
    
    print("When you ask a question:")
    print()
    print("Step 1: Query Embedding")
    print("  - Your question is converted to a vector embedding")
    print()
    print("Step 2: Similarity Search")
    print("  - The agent searches for relevant document chunks")
    print("  - Uses FAISS for efficient similarity search")
    print()
    print("Step 3: Context Retrieval")
    print("  - Top K most relevant chunks are retrieved")
    print("  - Chunks are combined into context")
    print()
    print("Step 4: LLM Generation")
    print("  - Context + question sent to GPT-4")
    print("  - LLM generates answer based on context")
    print()
    print("Step 5: Source Citation")
    print("  - Sources are included with page numbers")
    print("  - Confidence score is calculated")


def demo_advanced_features(agent: DocumentQAAgent):
    """Demo: Advanced features."""
    print_section("8. Advanced Features")
    
    print("🔹 Vector Store Persistence:")
    print("  - Save: agent.save_vector_store(name='my_store')")
    print("  - Load: agent.load_vector_store(name='my_store')")
    print()
    print("🔹 Conversation History:")
    print("  - Automatically maintained")
    print("  - View: agent.get_conversation_history()")
    print("  - Clear: agent.clear_history()")
    print()
    print("🔹 Session Export:")
    print("  - Export all session data")
    print("  - Useful for analytics and debugging")
    print()
    print("🔹 Custom Configuration:")
    print("  - Adjustable chunk size")
    print("  - Configurable overlap")
    print("  - Choice of embedding models")


def demo_example_questions():
    """Demo: Example questions to ask."""
    print_section("9. Example Questions")
    
    print("Once you load documents, you can ask questions like:")
    print()
    print("📋 Summarization:")
    print("  - What is this document about?")
    print("  - Summarize the main points")
    print("  - What are the key findings?")
    print()
    print("🔍 Specific Information:")
    print("  - What does the document say about [topic]?")
    print("  - Find information about [specific term]")
    print("  - What is the definition of [concept]?")
    print()
    print("🔗 Relationships:")
    print("  - How does [concept A] relate to [concept B]?")
    print("  - Compare [topic 1] and [topic 2]")
    print()
    print("📊 Analysis:")
    print("  - What are the main arguments presented?")
    print("  - What evidence supports [claim]?")
    print("  - What are the conclusions?")


def main():
    """Run the demo."""
    print("\n" + "=" * 70)
    print(" " * 15 + "🚀 Document Q&A Agent - Demo")
    print("=" * 70)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  Warning: OPENAI_API_KEY not set!")
        print("This demo will show you the agent's features, but you'll need")
        print("an API key to actually use the Q&A functionality.")
        print("\nSet your key in a .env file:")
        print("  OPENAI_API_KEY=sk-your-key-here")
    
    # Run demos
    agent = demo_agent_initialization()
    
    if agent:
        demo_agent_capabilities(agent)
        demo_status_check(agent)
        demo_help_system(agent)
        demo_conversational_interaction(agent)
    
    # Info demos (don't need initialized agent)
    if agent:
        demo_document_loading_info(agent)
        demo_qa_workflow(agent)
        demo_advanced_features(agent)
    
    demo_example_questions()
    
    # Final message
    print("\n" + "=" * 70)
    print("✓ Demo completed!")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Set your OPENAI_API_KEY in a .env file")
    print("  2. Run: python cli.py")
    print("  3. Use: load your_document.pdf")
    print("  4. Ask questions about your document!")
    print("\n📚 See README.md for detailed documentation")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    # Try to load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    main()

