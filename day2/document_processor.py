"""
Document Processor for PDF Ingestion and Text Chunking

This module handles PDF document loading, text extraction, and intelligent
chunking for optimal embedding and retrieval performance.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import re
from pathlib import Path


@dataclass
class DocumentChunk:
    """
    Represents a chunk of text from a document with metadata.
    
    Attributes:
        content: The text content of the chunk
        metadata: Dictionary containing source, page number, chunk index, etc.
        chunk_id: Unique identifier for the chunk
    """
    content: str
    metadata: Dict[str, Any]
    chunk_id: str


class DocumentProcessor:
    """
    Processes PDF documents for the Q&A system.
    
    Handles document loading, text extraction, cleaning, and intelligent
    chunking with overlap for better context preservation.
    """
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        min_chunk_size: int = 100
    ):
        """
        Initialize the document processor.
        
        Args:
            chunk_size: Target size for text chunks (in characters)
            chunk_overlap: Number of characters to overlap between chunks
            min_chunk_size: Minimum size for a valid chunk
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
    
    def load_pdf(self, file_path: str) -> str:
        """
        Load and extract text from a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text content
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            Exception: If PDF processing fails
        """
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            raise ImportError(
                "PyPDF2 is required for PDF processing. "
                "Install it with: pip install PyPDF2"
            )
        
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        try:
            reader = PdfReader(file_path)
            text = ""
            
            for page_num, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    # Add page marker for metadata tracking
                    text += f"\n[PAGE_{page_num}]\n{page_text}\n"
            
            if not text.strip():
                raise ValueError("No text could be extracted from the PDF")
            
            return text
            
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize extracted text.
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\?\!\:\;\-\(\)\[\]\n]', '', text)
        
        # Normalize line breaks
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    def chunk_text(
        self,
        text: str,
        source: str = "unknown"
    ) -> List[DocumentChunk]:
        """
        Split text into overlapping chunks with metadata.
        
        Uses intelligent splitting that tries to break at sentence boundaries
        while maintaining the target chunk size.
        
        Args:
            text: Text to chunk
            source: Source identifier (e.g., filename)
            
        Returns:
            List of DocumentChunk objects
        """
        chunks = []
        current_page = 1
        
        # Split by page markers first
        pages = re.split(r'\[PAGE_(\d+)\]', text)
        
        # Process pages
        page_contents = []
        for i in range(1, len(pages), 2):
            if i < len(pages):
                page_num = int(pages[i])
                page_text = pages[i + 1] if i + 1 < len(pages) else ""
                page_contents.append((page_num, page_text))
        
        # If no page markers, treat as single page
        if not page_contents:
            page_contents = [(1, text)]
        
        chunk_index = 0
        
        for page_num, page_text in page_contents:
            cleaned_text = self.clean_text(page_text)
            
            # Split into sentences for better chunking
            sentences = re.split(r'(?<=[.!?])\s+', cleaned_text)
            
            current_chunk = []
            current_length = 0
            
            for sentence in sentences:
                sentence_length = len(sentence)
                
                # If adding this sentence exceeds chunk size, create a chunk
                if current_length + sentence_length > self.chunk_size and current_chunk:
                    chunk_text = ' '.join(current_chunk)
                    
                    if len(chunk_text) >= self.min_chunk_size:
                        chunk = DocumentChunk(
                            content=chunk_text,
                            metadata={
                                'source': source,
                                'page': page_num,
                                'chunk_index': chunk_index,
                                'char_count': len(chunk_text)
                            },
                            chunk_id=f"{source}_page{page_num}_chunk{chunk_index}"
                        )
                        chunks.append(chunk)
                        chunk_index += 1
                    
                    # Keep overlap by retaining last few sentences
                    overlap_text = ' '.join(current_chunk)
                    if len(overlap_text) > self.chunk_overlap:
                        # Keep roughly chunk_overlap characters
                        current_chunk = [sentence]
                        current_length = sentence_length
                    else:
                        current_chunk = [sentence]
                        current_length = sentence_length
                else:
                    current_chunk.append(sentence)
                    current_length += sentence_length + 1  # +1 for space
            
            # Add remaining chunk
            if current_chunk:
                chunk_text = ' '.join(current_chunk)
                if len(chunk_text) >= self.min_chunk_size:
                    chunk = DocumentChunk(
                        content=chunk_text,
                        metadata={
                            'source': source,
                            'page': page_num,
                            'chunk_index': chunk_index,
                            'char_count': len(chunk_text)
                        },
                        chunk_id=f"{source}_page{page_num}_chunk{chunk_index}"
                    )
                    chunks.append(chunk)
                    chunk_index += 1
        
        return chunks
    
    def process_document(
        self,
        file_path: str
    ) -> Dict[str, Any]:
        """
        Complete document processing pipeline.
        
        Args:
            file_path: Path to the PDF document
            
        Returns:
            Dictionary containing processed chunks and metadata
        """
        # Extract filename for metadata
        filename = Path(file_path).name
        
        # Load PDF
        raw_text = self.load_pdf(file_path)
        
        # Chunk text
        chunks = self.chunk_text(raw_text, source=filename)
        
        # Calculate statistics
        total_chars = sum(len(chunk.content) for chunk in chunks)
        avg_chunk_size = total_chars / len(chunks) if chunks else 0
        
        return {
            'chunks': chunks,
            'metadata': {
                'source': filename,
                'total_chunks': len(chunks),
                'total_characters': total_chars,
                'avg_chunk_size': avg_chunk_size
            }
        }
    
    def process_multiple_documents(
        self,
        file_paths: List[str]
    ) -> Dict[str, Any]:
        """
        Process multiple PDF documents.
        
        Args:
            file_paths: List of paths to PDF documents
            
        Returns:
            Dictionary containing all chunks and aggregated metadata
        """
        all_chunks = []
        all_metadata = []
        
        for file_path in file_paths:
            try:
                result = self.process_document(file_path)
                all_chunks.extend(result['chunks'])
                all_metadata.append(result['metadata'])
            except Exception as e:
                print(f"Warning: Failed to process {file_path}: {str(e)}")
                continue
        
        total_chars = sum(len(chunk.content) for chunk in all_chunks)
        avg_chunk_size = total_chars / len(all_chunks) if all_chunks else 0
        
        return {
            'chunks': all_chunks,
            'metadata': {
                'total_documents': len(all_metadata),
                'total_chunks': len(all_chunks),
                'total_characters': total_chars,
                'avg_chunk_size': avg_chunk_size,
                'document_metadata': all_metadata
            }
        }

