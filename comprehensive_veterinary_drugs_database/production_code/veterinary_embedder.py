#!/usr/bin/env python3
"""
Veterinary Drug Database Embedder
Specialized embedder for veterinary drug chunks with batch processing
"""

import json
import os
import time
from datetime import datetime
from typing import List, Dict
import openai
from pinecone import Pinecone
from tqdm import tqdm

class VeterinaryEmbedder:
    def __init__(self):
        """Initialize the veterinary embedder"""
        print("🐾 Initializing Veterinary Drug Embedder...")
        
        # Configuration optimized for large datasets
        self.embedding_model = "text-embedding-ada-002"
        self.batch_size = 20  # Smaller batches to avoid token limits
        self.max_retries = 3
        self.retry_delay = 1  # seconds
        
        # Initialize clients
        self.openai_client = self._init_openai()
        self.pinecone_index = self._init_pinecone()
        
        print("✅ Veterinary Drug Embedder ready!")

    def _init_openai(self):
        """Initialize OpenAI client with error handling"""
        try:
            client = openai.OpenAI()
            # Test connection
            test_response = client.embeddings.create(
                input="test veterinary drug",
                model=self.embedding_model
            )
            print("✅ OpenAI client initialized and tested")
            return client
        except Exception as e:
            print(f"❌ OpenAI initialization failed: {str(e)}")
            print("💡 Check your OPENAI_API_KEY environment variable")
            raise

    def _init_pinecone(self):
        """Initialize Pinecone with veterinary index"""
        try:
            pc = Pinecone()
            
            # Use existing index or create vet-specific one
            index_name = "veterinary-drugs"
            
            try:
                # Try to get existing vet index
                index = pc.Index(index_name)
                stats = index.describe_index_stats()
                print(f"✅ Connected to existing Pinecone index: {index_name}")
                print(f"   Current vectors: {stats.get('total_vector_count', 0)}")
                return index
            except:
                # Fall back to main project index
                print("ℹ️ Using main project-docs index")
                index = pc.Index("project-docs")
                stats = index.describe_index_stats()
                print(f"✅ Connected to Pinecone index: project-docs")
                return index
                
        except Exception as e:
            print(f"❌ Pinecone initialization failed: {str(e)}")
            print("💡 Check your PINECONE_API_KEY environment variable")
            raise

    def load_drug_chunks(self) -> List[Dict]:
        """Load veterinary drug chunks"""
        chunks_file = "chunks/veterinary_drug_chunks.json"
        
        if not os.path.exists(chunks_file):
            print(f"❌ Chunks file not found: {chunks_file}")
            print("💡 Run 'python veterinary_drug_extractor.py' first")
            return []
        
        try:
            with open(chunks_file, 'r', encoding='utf-8') as f:
                chunks = json.load(f)
            
            print(f"📥 Loaded {len(chunks)} veterinary drug chunks")
            return chunks
            
        except Exception as e:
            print(f"❌ Error loading chunks: {str(e)}")
            return []

    def estimate_cost(self, chunks: List[Dict]) -> float:
        """Estimate OpenAI API cost for embeddings"""
        total_tokens = sum(len(chunk['text'].split()) * 1.3 for chunk in chunks)  # Rough token estimate
        cost_per_1k_tokens = 0.0001  # text-embedding-ada-002 pricing
        estimated_cost = (total_tokens / 1000) * cost_per_1k_tokens
        
        print(f"💰 Estimated cost: ${estimated_cost:.4f}")
        print(f"   Total chunks: {len(chunks)}")
        print(f"   Estimated tokens: {int(total_tokens)}")
        
        return estimated_cost

    def create_embeddings_with_batching(self, chunks: List[Dict]) -> List[Dict]:
        """Create embeddings with robust batch processing"""
        print(f"🧠 Creating embeddings for {len(chunks)} chunks...")
        
        embedded_chunks = []
        failed_chunks = []
        
        # Process in batches
        for i in tqdm(range(0, len(chunks), self.batch_size), desc="Creating embeddings"):
            batch = chunks[i:i + self.batch_size]
            batch_texts = [chunk['text'] for chunk in batch]
            
            # Retry logic for each batch
            batch_embeddings = None
            for attempt in range(self.max_retries):
                try:
                    response = self.openai_client.embeddings.create(
                        input=batch_texts,
                        model=self.embedding_model
                    )
                    batch_embeddings = [data.embedding for data in response.data]
                    break
                    
                except openai.RateLimitError as e:
                    wait_time = self.retry_delay * (2 ** attempt)  # Exponential backoff
                    print(f"    ⏳ Rate limit hit, waiting {wait_time}s... (attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(wait_time)
                    
                except Exception as e:
                    print(f"    ⚠️ Batch {i//self.batch_size + 1} attempt {attempt + 1} failed: {str(e)}")
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                    else:
                        print(f"    ❌ Batch {i//self.batch_size + 1} failed after {self.max_retries} attempts")
                        failed_chunks.extend(batch)
            
            # Add embeddings to successful chunks
            if batch_embeddings:
                for chunk, embedding in zip(batch, batch_embeddings):
                    embedded_chunk = chunk.copy()
                    embedded_chunk['embedding'] = embedding
                    embedded_chunk['embedding_metadata'] = {
                        'model': self.embedding_model,
                        'created_date': datetime.now().isoformat(),
                        'batch_id': i // self.batch_size
                    }
                    embedded_chunks.append(embedded_chunk)
            
            # Small delay between batches
            time.sleep(0.1)
        
        print(f"✅ Successfully embedded {len(embedded_chunks)} chunks")
        if failed_chunks:
            print(f"⚠️ Failed to embed {len(failed_chunks)} chunks")
        
        return embedded_chunks, failed_chunks

    def prepare_pinecone_vectors(self, embedded_chunks: List[Dict]) -> List[Dict]:
        """Prepare vectors for Pinecone upload with veterinary-specific metadata"""
        print("📦 Preparing vectors for Pinecone...")
        
        vectors = []
        for chunk in embedded_chunks:
            # Enhanced metadata for veterinary drugs
            metadata = {
                'text': chunk['text'][:1000],  # Truncate text for metadata limit
                'drug_name': chunk['metadata'].get('drug_name', 'unknown'),
                'chunk_type': chunk['metadata'].get('chunk_type', 'general'),
                'category': 'veterinary_drug',
                'source_file': chunk['metadata'].get('source_file', ''),
                'page_number': chunk['metadata'].get('page_number', 0),
                'section_name': chunk['metadata'].get('section_name', ''),
                'species': chunk['metadata'].get('species', ''),
                'extraction_date': chunk['metadata'].get('extraction_date', ''),
                'embedding_date': datetime.now().isoformat()
            }
            
            # Clean metadata (remove None values and ensure string types)
            clean_metadata = {}
            for key, value in metadata.items():
                if value is not None:
                    clean_metadata[key] = str(value) if not isinstance(value, (str, int, float, bool)) else value
            
            vector = {
                'id': chunk['chunk_id'],
                'values': chunk['embedding'],
                'metadata': clean_metadata
            }
            vectors.append(vector)
        
        print(f"📦 Prepared {len(vectors)} vectors for upload")
        return vectors

    def upload_to_pinecone(self, vectors: List[Dict]):
        """Upload vectors to Pinecone with progress tracking"""
        print(f"📤 Uploading {len(vectors)} vectors to Pinecone...")
        
        upload_batch_size = 100  # Pinecone batch size
        total_batches = (len(vectors) + upload_batch_size - 1) // upload_batch_size
        
        uploaded_count = 0
        failed_uploads = []
        
        for i in tqdm(range(0, len(vectors), upload_batch_size), desc="Uploading batches"):
            batch = vectors[i:i + upload_batch_size]
            
            try:
                self.pinecone_index.upsert(vectors=batch)
                uploaded_count += len(batch)
                time.sleep(0.2)  # Rate limiting
                
            except Exception as e:
                print(f"❌ Upload batch {i//upload_batch_size + 1} failed: {str(e)}")
                failed_uploads.extend(batch)
        
        print(f"✅ Successfully uploaded {uploaded_count} vectors")
        if failed_uploads:
            print(f"⚠️ Failed to upload {len(failed_uploads)} vectors")
        
        return uploaded_count, failed_uploads

    def verify_upload(self, expected_count: int):
        """Verify the upload was successful"""
        print("🔍 Verifying upload...")
        
        try:
            stats = self.pinecone_index.describe_index_stats()
            total_vectors = stats.get('total_vector_count', 0)
            
            print(f"📊 Index statistics:")
            print(f"   Total vectors in index: {total_vectors}")
            print(f"   Expected veterinary vectors: {expected_count}")
            
            # Test a sample query
            test_query = [0.1] * 1536  # Dummy embedding for testing
            test_results = self.pinecone_index.query(
                vector=test_query,
                top_k=5,
                include_metadata=True,
                filter={'category': 'veterinary_drug'}
            )
            
            vet_drug_count = len([match for match in test_results['matches'] 
                                if match['metadata'].get('category') == 'veterinary_drug'])
            
            print(f"   Veterinary drug vectors found: {vet_drug_count}")
            
            if vet_drug_count > 0:
                print("✅ Upload verification successful!")
            else:
                print("⚠️ Warning: No veterinary drug vectors found in test query")
                
        except Exception as e:
            print(f"⚠️ Could not verify upload: {str(e)}")

    def save_embedded_chunks(self, embedded_chunks: List[Dict]):
        """Save embedded chunks for backup"""
        output_file = "vet_database/embedded_veterinary_chunks.json"
        os.makedirs("vet_database", exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(embedded_chunks, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Embedded chunks saved to {output_file}")

def main():
    """Main embedding pipeline"""
    print("🐾 VETERINARY DRUG EMBEDDER")
    print("=" * 50)
    
    embedder = VeterinaryEmbedder()
    
    # Load chunks
    chunks = embedder.load_drug_chunks()
    if not chunks:
        return
    
    # Estimate cost
    estimated_cost = embedder.estimate_cost(chunks)
    if estimated_cost > 5.0:  # Higher threshold for large datasets
        response = input(f"⚠️ Estimated cost is ${estimated_cost:.2f}. Continue? (y/n): ")
        if response.lower() != 'y':
            print("❌ Operation cancelled")
            return
    
    try:
        # Create embeddings
        embedded_chunks, failed_chunks = embedder.create_embeddings_with_batching(chunks)
        
        if not embedded_chunks:
            print("❌ No embeddings created successfully")
            return
        
        # Prepare vectors
        vectors = embedder.prepare_pinecone_vectors(embedded_chunks)
        
        # Upload to Pinecone
        uploaded_count, failed_uploads = embedder.upload_to_pinecone(vectors)
        
        # Verify upload
        embedder.verify_upload(len(embedded_chunks))
        
        # Save backup
        embedder.save_embedded_chunks(embedded_chunks)
        
        # Final summary
        print(f"\n🎉 VETERINARY DRUG EMBEDDING COMPLETE!")
        print(f"📊 Final Summary:")
        print(f"   Total chunks processed: {len(chunks)}")
        print(f"   Successfully embedded: {len(embedded_chunks)}")
        print(f"   Uploaded to Pinecone: {uploaded_count}")
        print(f"   Failed embeddings: {len(failed_chunks)}")
        print(f"   Failed uploads: {len(failed_uploads)}")
        print(f"   Estimated cost: ${estimated_cost:.4f}")
        
        print(f"\n✅ Your veterinary drug database is ready!")
        print(f"💡 Next: Run 'python veterinary_assistant.py' to test queries")
        
    except Exception as e:
        print(f"❌ Embedding process failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()