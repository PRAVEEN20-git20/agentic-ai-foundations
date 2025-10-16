"""
Example Usage of Document Q&A Agent

This script demonstrates how to use the Document Q&A agent programmatically.
"""

import os
from doc_qa_agent import DocumentQAAgent


def example_basic_usage():
    """Basic usage example: Load a document and ask questions."""
    print("=" * 60)
    print("Example 1: Basic Document Q&A")
    print("=" * 60)
    
    # Initialize agent
    agent = DocumentQAAgent()
    
    # Load a document (you'll need to provide your own PDF)
    # For this example, we'll just show the code structure
    pdf_path = "your_document.pdf"
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"\n⚠️  Note: Please provide a PDF file at '{pdf_path}' to run this example")
        print("You can modify the pdf_path variable to point to your PDF file.\n")
        return
    
    # Load the document
    print(f"\nLoading document: {pdf_path}")
    agent.load_document(pdf_path)
    
    # Ask questions
    questions = [
        "What is this document about?",
        "What are the main topics covered?",
        "Summarize the key points"
    ]
    
    for question in questions:
        print(f"\n{'─' * 60}")
        print(f"Question: {question}")
        print('─' * 60)
        
        result = agent.ask(question)
        print(f"Answer: {result['answer']}")
        print(f"Confidence: {result['confidence']}")
        
        if result.get('sources'):
            print("\nSources:")
            for source in result['sources'][:3]:  # Show top 3 sources
                print(f"  - {source['source']} (Page {source['page']}, Relevance: {source['similarity']:.2f})")


def example_multiple_documents():
    """Example: Load and query multiple documents."""
    print("\n" + "=" * 60)
    print("Example 2: Multiple Documents")
    print("=" * 60)
    
    agent = DocumentQAAgent()
    
    # Load multiple documents
    pdf_paths = [
        "document1.pdf",
        "document2.pdf",
        "document3.pdf"
    ]
    
    # Filter existing files
    existing_files = [path for path in pdf_paths if os.path.exists(path)]
    
    if not existing_files:
        print("\n⚠️  Note: Please provide PDF files to run this example")
        return
    
    print(f"\nLoading {len(existing_files)} documents...")
    agent.load_multiple_documents(existing_files)
    
    # Ask cross-document questions
    result = agent.ask("Compare the main themes across all documents")
    print(f"\nAnswer: {result['answer']}")


def example_conversation_flow():
    """Example: Conversational interaction with the agent."""
    print("\n" + "=" * 60)
    print("Example 3: Conversational Flow")
    print("=" * 60)
    
    agent = DocumentQAAgent()
    
    # Conversational messages
    messages = [
        "Hello!",
        "What can you help me with?",
        "What's your status?",
    ]
    
    for message in messages:
        print(f"\nUser: {message}")
        response = agent.chat(message)
        print(f"Agent: {response}")


def example_save_and_load():
    """Example: Save and load vector stores."""
    print("\n" + "=" * 60)
    print("Example 4: Save and Load Vector Store")
    print("=" * 60)
    
    # Create and populate agent
    agent1 = DocumentQAAgent()
    
    pdf_path = "your_document.pdf"
    if os.path.exists(pdf_path):
        agent1.load_document(pdf_path)
        
        # Save the vector store
        print("\nSaving vector store...")
        response = agent1.save_vector_store(name="example_store")
        print(response)
        
        # Create new agent and load the store
        agent2 = DocumentQAAgent()
        print("\nLoading vector store into new agent...")
        response = agent2.load_vector_store(name="example_store")
        print(response)
        
        # Query the loaded store
        result = agent2.ask("What is this document about?")
        print(f"\nAnswer from loaded store: {result['answer']}")
    else:
        print(f"\n⚠️  Note: Please provide a PDF file at '{pdf_path}' to run this example")


def example_custom_configuration():
    """Example: Custom agent configuration."""
    print("\n" + "=" * 60)
    print("Example 5: Custom Configuration")
    print("=" * 60)
    
    # Create agent with custom settings
    agent = DocumentQAAgent(
        chunk_size=500,  # Smaller chunks for more granular retrieval
        chunk_overlap=100,  # Less overlap
        embedding_model="text-embedding-3-small"
    )
    
    print("\n✓ Agent created with custom configuration:")
    print(f"  - Chunk size: 500 characters")
    print(f"  - Chunk overlap: 100 characters")
    print(f"  - Embedding model: text-embedding-3-small")


def example_session_export():
    """Example: Export session data."""
    print("\n" + "=" * 60)
    print("Example 6: Session Export")
    print("=" * 60)
    
    agent = DocumentQAAgent()
    
    # Simulate some interactions
    agent.chat("Hello!")
    
    # Export session
    session_data = agent.export_session()
    
    print("\nSession data exported:")
    print(f"  - Queries processed: {session_data['session_info']['queries_processed']}")
    print(f"  - Documents loaded: {len(session_data['session_info']['documents_loaded'])}")
    print(f"  - Conversation history: {len(session_data['conversation_history'])} entries")


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print(" " * 15 + "Document Q&A Agent - Usage Examples")
    print("=" * 70)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  Warning: OPENAI_API_KEY not set!")
        print("Please set your OpenAI API key in a .env file or environment variable.")
        print("Example: OPENAI_API_KEY=sk-...")
        return
    
    try:
        # Run examples
        example_conversation_flow()  # No documents needed
        example_custom_configuration()  # No documents needed
        example_session_export()  # No documents needed
        
        # Examples that need documents
        example_basic_usage()
        example_multiple_documents()
        example_save_and_load()
        
        print("\n" + "=" * 70)
        print("✓ Examples completed!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ Error running examples: {str(e)}")


if __name__ == "__main__":
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    main()

