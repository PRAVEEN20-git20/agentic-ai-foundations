"""
Document Q&A Agent with LangChain Integration

This module implements an agentic Q&A system that can ingest PDF documents,
create vector embeddings, and answer questions using RAG (Retrieval-Augmented Generation).
"""

from typing import List, Dict, Any, Optional, Tuple
import os
from datetime import datetime
from document_processor import DocumentProcessor
from vector_store_manager import VectorStoreManager


class DocumentQAAgent:
    """
    An intelligent document Q&A agent with autonomy, memory, and reasoning.
    
    The agent demonstrates:
    - Autonomy: Decides which documents to search and how to formulate answers
    - Memory: Maintains conversation history and document context
    - Reasoning: Uses RAG to ground answers in document content
    """
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        embedding_model: str = "text-embedding-3-small"
    ):
        """
        Initialize the Document Q&A agent.
        
        Args:
            chunk_size: Size of text chunks for processing
            chunk_overlap: Overlap between chunks
            embedding_model: OpenAI embedding model to use
        """
        self.name = "Document Q&A Agent"
        self.document_processor = DocumentProcessor(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.vector_store = VectorStoreManager(embedding_model=embedding_model)
        
        # Initialize OpenAI client for chat
        self._init_openai_client()
        
        # Memory: Conversation history and session info
        self.conversation_history: List[Dict[str, str]] = []
        self.session_info = {
            'start_time': datetime.now(),
            'documents_loaded': [],
            'total_chunks': 0,
            'queries_processed': 0
        }
        
        # System prompt for the agent
        self.system_prompt = """You are a helpful AI assistant that answers questions based on provided document context. 

Your responsibilities:
1. Answer questions using ONLY the information from the provided context
2. If the answer is not in the context, clearly state that you don't have that information
3. Cite the source document and page when providing answers
4. Be concise but thorough in your explanations
5. If the context is ambiguous, acknowledge uncertainty

Always ground your answers in the provided context and avoid speculation."""
    
    def _init_openai_client(self) -> None:
        """
        Initialize OpenAI client for chat completions.
        
        Raises:
            ValueError: If OpenAI API key is not set
        """
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "OpenAI library is required. Install it with: pip install openai"
            )
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set. "
                "Please set it in your .env file or environment."
            )
        
        self.client = OpenAI(api_key=api_key)
    
    def load_document(self, file_path: str, show_progress: bool = True) -> Dict[str, Any]:
        """
        Load and ingest a PDF document into the agent's knowledge base.
        
        Args:
            file_path: Path to the PDF file
            show_progress: Whether to show progress messages
            
        Returns:
            Dictionary with ingestion statistics
            
        Side effects:
            Updates vector store and session info
        """
        if show_progress:
            print(f"\n📄 Loading document: {file_path}")
        
        # Process the document
        result = self.document_processor.process_document(file_path)
        chunks = result['chunks']
        metadata = result['metadata']
        
        if show_progress:
            print(f"✓ Extracted {metadata['total_chunks']} chunks")
        
        # Add to vector store
        self.vector_store.add_documents(chunks, show_progress=show_progress)
        
        # Update session info
        self.session_info['documents_loaded'].append(metadata['source'])
        self.session_info['total_chunks'] += metadata['total_chunks']
        
        if show_progress:
            print(f"✓ Document '{metadata['source']}' successfully loaded!\n")
        
        return metadata
    
    def load_multiple_documents(
        self,
        file_paths: List[str],
        show_progress: bool = True
    ) -> Dict[str, Any]:
        """
        Load multiple PDF documents.
        
        Args:
            file_paths: List of paths to PDF files
            show_progress: Whether to show progress messages
            
        Returns:
            Dictionary with aggregated statistics
        """
        if show_progress:
            print(f"\n📚 Loading {len(file_paths)} documents...")
        
        result = self.document_processor.process_multiple_documents(file_paths)
        chunks = result['chunks']
        metadata = result['metadata']
        
        if chunks:
            self.vector_store.add_documents(chunks, show_progress=show_progress)
            
            # Update session info
            for doc_meta in metadata['document_metadata']:
                self.session_info['documents_loaded'].append(doc_meta['source'])
            self.session_info['total_chunks'] = metadata['total_chunks']
        
        if show_progress:
            print(f"✓ Loaded {metadata['total_documents']} documents with {metadata['total_chunks']} chunks!\n")
        
        return metadata
    
    def ask(
        self,
        question: str,
        num_sources: int = 5,
        model: str = "gpt-4o-mini",
        include_sources: bool = True
    ) -> Dict[str, Any]:
        """
        Ask a question about the loaded documents.
        
        Args:
            question: The question to answer
            num_sources: Number of source chunks to retrieve
            model: OpenAI model to use for generation
            include_sources: Whether to include source information in response
            
        Returns:
            Dictionary containing answer, sources, and metadata
        """
        # Check if documents are loaded
        if not self.session_info['documents_loaded']:
            return {
                'answer': "No documents have been loaded yet. Please load some documents first using the 'load' command.",
                'sources': [],
                'confidence': 'low',
                'error': 'no_documents'
            }
        
        # Retrieve relevant context
        context, sources = self.vector_store.get_context_for_query(
            question,
            k=num_sources
        )
        
        if not context:
            return {
                'answer': "I couldn't find relevant information in the loaded documents to answer this question.",
                'sources': [],
                'confidence': 'none',
                'error': 'no_context'
            }
        
        # Build the prompt with context
        user_prompt = self._build_qa_prompt(question, context)
        
        # Generate answer using LLM
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,  # Lower temperature for factual answers
                max_tokens=1000
            )
            
            answer = response.choices[0].message.content
            
            # Estimate confidence based on source similarity
            avg_similarity = sum(s['similarity'] for s in sources) / len(sources) if sources else 0
            confidence = 'high' if avg_similarity > 0.7 else 'medium' if avg_similarity > 0.5 else 'low'
            
            # Update memory
            self.conversation_history.append({
                'question': question,
                'answer': answer,
                'sources': sources,
                'timestamp': datetime.now().isoformat()
            })
            self.session_info['queries_processed'] += 1
            
            result = {
                'answer': answer,
                'sources': sources if include_sources else [],
                'confidence': confidence,
                'context_used': len(context)
            }
            
            return result
            
        except Exception as e:
            return {
                'answer': f"Error generating answer: {str(e)}",
                'sources': [],
                'confidence': 'error',
                'error': str(e)
            }
    
    def _build_qa_prompt(self, question: str, context: str) -> str:
        """
        Build the prompt for Q&A with context.
        
        Args:
            question: User's question
            context: Retrieved document context
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""Based on the following context from the documents, please answer the question.

CONTEXT:
{context}

QUESTION: {question}

Please provide a clear, accurate answer based on the context above. If you reference specific information, mention which part of the context it comes from."""
        
        return prompt
    
    def chat(
        self,
        message: str,
        model: str = "gpt-4o-mini"
    ) -> str:
        """
        Have a conversational interaction with the agent.
        
        This method handles both questions and general conversation,
        using document context when relevant.
        
        Args:
            message: User message
            model: OpenAI model to use
            
        Returns:
            Agent's response
        """
        # Check if it's a question about documents
        question_indicators = ['?', 'what', 'how', 'why', 'when', 'where', 'who', 'explain', 'tell me']
        is_question = any(indicator in message.lower() for indicator in question_indicators)
        
        if is_question and self.session_info['documents_loaded']:
            # Use Q&A mode
            result = self.ask(message, model=model)
            
            answer = result['answer']
            sources = result.get('sources', [])
            
            # Format sources if available
            if sources and not result.get('error'):
                source_text = "\n\n📚 **Sources:**\n"
                seen_sources = set()
                for source in sources:
                    source_key = f"{source['source']} (Page {source['page']})"
                    if source_key not in seen_sources:
                        source_text += f"- {source_key}\n"
                        seen_sources.add(source_key)
                answer += source_text
            
            return answer
        else:
            # General conversation
            return self._handle_general_message(message)
    
    def _handle_general_message(self, message: str) -> str:
        """
        Handle general conversation messages.
        
        Args:
            message: User message
            
        Returns:
            Response string
        """
        message_lower = message.lower()
        
        # Handle greetings
        if any(greeting in message_lower for greeting in ['hello', 'hi', 'hey']):
            return f"Hello! I'm {self.name}. I can answer questions about documents you load. Use 'load' to add documents or 'help' for more information."
        
        # Handle status requests
        if 'status' in message_lower or 'info' in message_lower:
            return self.get_status()
        
        # Handle help requests
        if 'help' in message_lower:
            return self.get_help()
        
        # Default response
        return "I'm here to answer questions about your documents. Try asking a question, or use 'help' for more information."
    
    def get_status(self) -> str:
        """
        Get current agent status and statistics.
        
        Returns:
            Formatted status string
        """
        duration = datetime.now() - self.session_info['start_time']
        minutes = int(duration.total_seconds() / 60)
        
        status = f"""
📊 **Agent Status**

🔹 Documents loaded: {len(self.session_info['documents_loaded'])}
🔹 Total chunks: {self.session_info['total_chunks']}
🔹 Queries processed: {self.session_info['queries_processed']}
🔹 Session duration: {minutes} minute(s)

📚 **Loaded Documents:**
"""
        
        if self.session_info['documents_loaded']:
            for doc in self.session_info['documents_loaded']:
                status += f"  - {doc}\n"
        else:
            status += "  (none)\n"
        
        return status.strip()
    
    def get_help(self) -> str:
        """
        Get help information about agent capabilities.
        
        Returns:
            Formatted help string
        """
        help_text = """
📖 **Document Q&A Agent Help**

**What I can do:**
- Load and analyze PDF documents
- Answer questions based on document content
- Search through multiple documents
- Provide source citations

**Available commands:**
- Ask any question about your loaded documents
- 'status' or 'info' - View current agent status
- 'help' - Show this help message
- 'clear' - Clear conversation history
- 'save <name>' - Save the current vector store
- 'load <name>' - Load a saved vector store

**Tips:**
- Load documents before asking questions
- Ask specific questions for better results
- I'll cite my sources when answering
- I can only answer based on loaded documents
        """.strip()
        return help_text
    
    def clear_history(self) -> str:
        """
        Clear conversation history.
        
        Returns:
            Confirmation message
        """
        count = len(self.conversation_history)
        self.conversation_history.clear()
        self.session_info['queries_processed'] = 0
        return f"✓ Cleared {count} conversation(s) from history."
    
    def save_vector_store(
        self,
        directory: str = "vector_stores",
        name: str = "default"
    ) -> str:
        """
        Save the current vector store to disk.
        
        Args:
            directory: Directory to save to
            name: Name for the vector store
            
        Returns:
            Status message
        """
        try:
            self.vector_store.save(directory, name)
            return f"✓ Vector store '{name}' saved successfully to {directory}/"
        except Exception as e:
            return f"✗ Error saving vector store: {str(e)}"
    
    def load_vector_store(
        self,
        directory: str = "vector_stores",
        name: str = "default"
    ) -> str:
        """
        Load a saved vector store from disk.
        
        Args:
            directory: Directory to load from
            name: Name of the vector store
            
        Returns:
            Status message
        """
        try:
            self.vector_store.load(directory, name)
            
            # Update session info
            stats = self.vector_store.get_stats()
            self.session_info['total_chunks'] = stats['total_chunks']
            
            return f"✓ Vector store '{name}' loaded successfully ({stats['total_chunks']} chunks)"
        except Exception as e:
            return f"✗ Error loading vector store: {str(e)}"
    
    def get_conversation_history(self, last_n: int = 5) -> List[Dict[str, Any]]:
        """
        Get recent conversation history.
        
        Args:
            last_n: Number of recent conversations to return
            
        Returns:
            List of recent conversations
        """
        return self.conversation_history[-last_n:]
    
    def export_session(self) -> Dict[str, Any]:
        """
        Export complete session information.
        
        Returns:
            Dictionary with session data
        """
        return {
            'session_info': {
                **self.session_info,
                'start_time': self.session_info['start_time'].isoformat()
            },
            'conversation_history': self.conversation_history,
            'vector_store_stats': self.vector_store.get_stats()
        }

