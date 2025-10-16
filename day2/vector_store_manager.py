"""
Vector Store Manager for Document Embeddings

This module manages vector embeddings and similarity search using FAISS
and OpenAI embeddings for efficient document retrieval.
"""

from typing import List, Dict, Any, Optional, Tuple
import os
import json
import pickle
from pathlib import Path
from document_processor import DocumentChunk


class VectorStoreManager:
    """
    Manages vector embeddings and similarity search for document chunks.
    
    Uses OpenAI embeddings and FAISS for efficient similarity search.
    Supports persistence and retrieval of vector stores.
    """
    
    def __init__(
        self,
        embedding_model: str = "text-embedding-3-small",
        dimension: int = 1536
    ):
        """
        Initialize the vector store manager.
        
        Args:
            embedding_model: OpenAI embedding model to use
            dimension: Dimension of embedding vectors
        """
        self.embedding_model = embedding_model
        self.dimension = dimension
        self.index = None
        self.chunks = []
        self.embeddings = []
        
        # Initialize OpenAI client
        self._init_openai_client()
        
        # Initialize FAISS index
        self._init_faiss_index()
    
    def _init_openai_client(self) -> None:
        """
        Initialize OpenAI client with API key from environment.
        
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
    
    def _init_faiss_index(self) -> None:
        """
        Initialize FAISS index for similarity search.
        
        Raises:
            ImportError: If FAISS is not installed
        """
        try:
            import faiss
        except ImportError:
            raise ImportError(
                "FAISS is required. Install it with: pip install faiss-cpu"
            )
        
        # Create a flat L2 index (most accurate for small to medium datasets)
        self.index = faiss.IndexFlatL2(self.dimension)
    
    def create_embedding(self, text: str) -> List[float]:
        """
        Create an embedding vector for a text string.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as list of floats
            
        Raises:
            Exception: If embedding generation fails
        """
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Failed to create embedding: {str(e)}")
    
    def create_embeddings_batch(
        self,
        texts: List[str],
        batch_size: int = 100
    ) -> List[List[float]]:
        """
        Create embeddings for multiple texts in batches.
        
        Args:
            texts: List of texts to embed
            batch_size: Number of texts to process in each batch
            
        Returns:
            List of embedding vectors
        """
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            try:
                response = self.client.embeddings.create(
                    model=self.embedding_model,
                    input=batch
                )
                batch_embeddings = [item.embedding for item in response.data]
                embeddings.extend(batch_embeddings)
            except Exception as e:
                print(f"Warning: Batch {i // batch_size + 1} failed: {str(e)}")
                # Create zero vectors for failed batch
                embeddings.extend([[0.0] * self.dimension] * len(batch))
        
        return embeddings
    
    def add_documents(
        self,
        chunks: List[DocumentChunk],
        show_progress: bool = True
    ) -> None:
        """
        Add document chunks to the vector store.
        
        Args:
            chunks: List of DocumentChunk objects to add
            show_progress: Whether to show progress messages
            
        Side effects:
            Updates the FAISS index and internal chunk storage
        """
        if not chunks:
            print("No chunks to add")
            return
        
        if show_progress:
            print(f"Creating embeddings for {len(chunks)} chunks...")
        
        # Extract text content from chunks
        texts = [chunk.content for chunk in chunks]
        
        # Create embeddings
        embeddings = self.create_embeddings_batch(texts)
        
        if show_progress:
            print(f"Adding {len(embeddings)} embeddings to vector store...")
        
        # Convert to numpy array for FAISS
        import numpy as np
        embeddings_array = np.array(embeddings, dtype='float32')
        
        # Add to FAISS index
        self.index.add(embeddings_array)
        
        # Store chunks and embeddings
        self.chunks.extend(chunks)
        self.embeddings.extend(embeddings)
        
        if show_progress:
            print(f"✓ Successfully added {len(chunks)} chunks to vector store")
    
    def search(
        self,
        query: str,
        k: int = 5
    ) -> List[Tuple[DocumentChunk, float]]:
        """
        Search for similar document chunks using a query.
        
        Args:
            query: Search query text
            k: Number of results to return
            
        Returns:
            List of (DocumentChunk, similarity_score) tuples
        """
        if not self.chunks:
            return []
        
        # Create embedding for query
        query_embedding = self.create_embedding(query)
        
        # Convert to numpy array
        import numpy as np
        query_array = np.array([query_embedding], dtype='float32')
        
        # Search in FAISS index
        distances, indices = self.index.search(query_array, k)
        
        # Prepare results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.chunks):  # Valid index
                chunk = self.chunks[idx]
                # Convert L2 distance to similarity score (lower is better)
                # Normalize to 0-1 range where 1 is most similar
                distance = float(distances[0][i])
                similarity = 1 / (1 + distance)  # Simple normalization
                results.append((chunk, similarity))
        
        return results
    
    def get_context_for_query(
        self,
        query: str,
        k: int = 5,
        max_context_length: int = 4000
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Get relevant context for a query, formatted for LLM consumption.
        
        Args:
            query: Search query
            k: Number of chunks to retrieve
            max_context_length: Maximum total length of context
            
        Returns:
            Tuple of (context_text, source_metadata)
        """
        results = self.search(query, k=k)
        
        if not results:
            return "", []
        
        context_parts = []
        sources = []
        current_length = 0
        
        for chunk, similarity in results:
            chunk_text = chunk.content
            chunk_length = len(chunk_text)
            
            # Stop if we exceed max context length
            if current_length + chunk_length > max_context_length:
                break
            
            context_parts.append(chunk_text)
            current_length += chunk_length
            
            # Add source metadata
            sources.append({
                'source': chunk.metadata.get('source', 'unknown'),
                'page': chunk.metadata.get('page', 'unknown'),
                'similarity': round(similarity, 3)
            })
        
        context = "\n\n---\n\n".join(context_parts)
        return context, sources
    
    def save(self, directory: str, name: str = "vector_store") -> None:
        """
        Save the vector store to disk.
        
        Args:
            directory: Directory to save the store
            name: Base name for the saved files
            
        Side effects:
            Creates files in the specified directory
        """
        import faiss
        import numpy as np
        
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        index_path = path / f"{name}.faiss"
        faiss.write_index(self.index, str(index_path))
        
        # Save chunks
        chunks_path = path / f"{name}_chunks.pkl"
        with open(chunks_path, 'wb') as f:
            pickle.dump(self.chunks, f)
        
        # Save metadata
        metadata_path = path / f"{name}_metadata.json"
        metadata = {
            'embedding_model': self.embedding_model,
            'dimension': self.dimension,
            'num_chunks': len(self.chunks),
            'num_embeddings': len(self.embeddings)
        }
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✓ Vector store saved to {directory}/")
    
    def load(self, directory: str, name: str = "vector_store") -> None:
        """
        Load a vector store from disk.
        
        Args:
            directory: Directory containing the saved store
            name: Base name of the saved files
            
        Side effects:
            Replaces current vector store with loaded data
            
        Raises:
            FileNotFoundError: If store files don't exist
        """
        import faiss
        
        path = Path(directory)
        
        # Load FAISS index
        index_path = path / f"{name}.faiss"
        if not index_path.exists():
            raise FileNotFoundError(f"Vector store not found: {index_path}")
        
        self.index = faiss.read_index(str(index_path))
        
        # Load chunks
        chunks_path = path / f"{name}_chunks.pkl"
        with open(chunks_path, 'rb') as f:
            self.chunks = pickle.load(f)
        
        # Load metadata
        metadata_path = path / f"{name}_metadata.json"
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        print(f"✓ Vector store loaded: {metadata['num_chunks']} chunks")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector store.
        
        Returns:
            Dictionary with store statistics
        """
        return {
            'total_chunks': len(self.chunks),
            'total_embeddings': len(self.embeddings),
            'embedding_model': self.embedding_model,
            'dimension': self.dimension,
            'index_size': self.index.ntotal if self.index else 0
        }

