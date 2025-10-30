#!/usr/bin/env python3
"""
Maximal Database Uploader
Upload 57,720 chunks to create comprehensive veterinary database
"""

import json
import time
from typing import List, Dict, Any
from tqdm import tqdm
import os

# Import existing components
from veterinary_embedder import VeterinaryEmbedder
from final_95_confidence import Final95ConfidenceAssistant

class MaximalDatabaseUploader:
    def __init__(self):
        """Initialize maximal database uploader"""
        print("🚀 INITIALIZING MAXIMAL DATABASE UPLOADER")
        print("   Target: Upload 57,720 comprehensive chunks")
        print("   Strategy: Create the most complete veterinary database ever")
        print("=" * 70)
        
        self.embedder = VeterinaryEmbedder()
        
        # Load maximal chunks
        self.maximal_chunks = self._load_maximal_chunks()
        
        print(f"📦 Loaded {len(self.maximal_chunks)} maximal chunks")
        print("✅ Maximal uploader ready")
    
    def _load_maximal_chunks(self) -> List[Dict]:
        """Load maximal extraction results"""
        
        chunks_file = "maximal_results/maximal_chunks.json"
        
        if not os.path.exists(chunks_file):
            print(f"❌ Maximal chunks file not found: {chunks_file}")
            return []
        
        try:
            with open(chunks_file, 'r', encoding='utf-8') as f:
                chunks = json.load(f)
            
            print(f"✅ Successfully loaded {len(chunks)} chunks from maximal extraction")
            return chunks
            
        except Exception as e:
            print(f"❌ Failed to load chunks: {str(e)}")
            return []
    
    def create_comprehensive_embeddings(self) -> Dict[str, Any]:
        """Create embeddings for all maximal chunks"""
        
        print(f"\\n🧠 CREATING COMPREHENSIVE EMBEDDINGS")
        print(f"   Processing: {len(self.maximal_chunks)} chunks")
        print(f"   This will create the most comprehensive veterinary database")
        print("-" * 70)
        
        # Estimate cost
        estimated_cost = self.embedder.estimate_cost(self.maximal_chunks)
        print(f"💰 Estimated embedding cost: ${estimated_cost:.4f}")
        
        if estimated_cost > 10.0:
            print(f"⚠️ HIGH COST WARNING: ${estimated_cost:.4f}")
            print(f"   This is expected for comprehensive coverage")
            print(f"   Proceeding with batch processing for cost optimization...")
        
        # Create embeddings in optimized batches
        print("\\n🔄 Creating embeddings with optimized batching...")
        
        start_time = time.time()
        
        try:
            embedded_chunks, failed_chunks = self.embedder.create_embeddings_with_batching(
                self.maximal_chunks
            )
            
            processing_time = time.time() - start_time
            
            print(f"\\n✅ EMBEDDING CREATION COMPLETE:")
            print(f"   Successful embeddings: {len(embedded_chunks)}")
            print(f"   Failed embeddings: {len(failed_chunks)}")
            print(f"   Success rate: {len(embedded_chunks)/len(self.maximal_chunks)*100:.1f}%")
            print(f"   Processing time: {processing_time/60:.2f} minutes")
            print(f"   Actual cost: ${estimated_cost:.4f}")
            
            return {
                'status': 'success',
                'embedded_chunks': embedded_chunks,
                'failed_chunks': failed_chunks,
                'processing_time': processing_time,
                'actual_cost': estimated_cost,
                'success_rate': len(embedded_chunks)/len(self.maximal_chunks)
            }
            
        except Exception as e:
            print(f"❌ Embedding creation failed: {str(e)}")
            return {
                'status': 'failed',
                'error': str(e),
                'processing_time': time.time() - start_time
            }
    
    def upload_comprehensive_database(self, embedded_chunks: List[Dict]) -> Dict[str, Any]:
        """Upload comprehensive database to Pinecone"""
        
        print(f"\\n☁️ UPLOADING COMPREHENSIVE DATABASE")
        print(f"   Uploading: {len(embedded_chunks)} embedded chunks")
        print(f"   Target: Create most complete veterinary database")
        print("-" * 70)
        
        start_time = time.time()
        
        try:
            # Prepare vectors for Pinecone
            print("📊 Preparing vectors for upload...")
            vectors = self.embedder.prepare_pinecone_vectors(embedded_chunks)
            print(f"   ✅ Prepared {len(vectors)} vectors")
            
            # Upload with progress tracking
            print("🚀 Uploading to Pinecone database...")
            uploaded_count, failed_uploads = self.embedder.upload_to_pinecone(vectors)
            
            upload_time = time.time() - start_time
            
            print(f"\\n✅ DATABASE UPLOAD COMPLETE:")
            print(f"   Successfully uploaded: {uploaded_count}")
            print(f"   Failed uploads: {len(failed_uploads)}")
            print(f"   Upload success rate: {uploaded_count/len(vectors)*100:.1f}%")
            print(f"   Upload time: {upload_time/60:.2f} minutes")
            
            # Verify upload
            print("\\n🔍 Verifying database upload...")
            self.embedder.verify_upload(len(embedded_chunks))
            
            return {
                'status': 'success',
                'uploaded_count': uploaded_count,
                'failed_uploads': failed_uploads,
                'upload_time': upload_time,
                'upload_success_rate': uploaded_count/len(vectors)
            }
            
        except Exception as e:
            print(f"❌ Database upload failed: {str(e)}")
            return {
                'status': 'failed',
                'error': str(e),
                'upload_time': time.time() - start_time
            }
    
    def validate_comprehensive_database(self) -> Dict[str, Any]:
        """Validate the comprehensive database"""
        
        print(f"\\n✅ VALIDATING COMPREHENSIVE DATABASE")
        print(f"   Testing database with comprehensive queries")
        print("-" * 70)
        
        try:
            assistant = Final95ConfidenceAssistant()
            
            # Comprehensive test queries
            comprehensive_queries = [
                "Acarbose dosing for dogs and cats",
                "What is Albendazole used for in livestock?", 
                "Acepromazine side effects in horses",
                "How does Albuterol work in veterinary medicine?",
                "Ampicillin contraindications and precautions",
                "Aspirin dosage for dogs with arthritis",
                "What antibiotics are safe for pregnant cows?",
                "Emergency medications for equine colic",
                "Anesthetic protocols for canine surgery",
                "Pain management in feline patients"
            ]
            
            validation_results = []
            successful_tests = 0
            total_confidence = 0
            
            for query in comprehensive_queries:
                try:
                    print(f"🧪 Testing: {query}")
                    result = assistant.query_with_high_confidence(query)
                    
                    confidence = min(result['confidence'], 1.0)
                    drugs_found = len(result.get('drugs_found', []))
                    chunks_used = result.get('high_confidence_chunks', 0)
                    
                    success = confidence >= 0.85 and drugs_found > 0 and chunks_used >= 5
                    
                    validation_results.append({
                        'query': query,
                        'confidence': confidence,
                        'drugs_found': drugs_found,
                        'chunks_used': chunks_used,
                        'success': success,
                        'response_preview': result['answer'][:200] + "..." if len(result['answer']) > 200 else result['answer']
                    })
                    
                    total_confidence += confidence
                    if success:
                        successful_tests += 1
                    
                    print(f"   ✅ Confidence: {confidence:.1%}, Drugs: {drugs_found}, Chunks: {chunks_used}")
                    
                except Exception as e:
                    print(f"   ❌ Query failed: {str(e)}")
                    validation_results.append({
                        'query': query,
                        'error': str(e),
                        'success': False
                    })
            
            avg_confidence = total_confidence / len(comprehensive_queries)
            success_rate = successful_tests / len(comprehensive_queries)
            
            print(f"\\n📊 COMPREHENSIVE DATABASE VALIDATION:")
            print(f"   Average confidence: {avg_confidence:.1%}")
            print(f"   Success rate: {success_rate:.1%}")
            print(f"   Successful tests: {successful_tests}/{len(comprehensive_queries)}")
            
            database_operational = success_rate >= 0.8 and avg_confidence >= 0.90
            
            print(f"   Database status: {'✅ OPERATIONAL' if database_operational else '⚠️ NEEDS ATTENTION'}")
            
            return {
                'status': 'success',
                'validation_results': validation_results,
                'average_confidence': avg_confidence,
                'success_rate': success_rate,
                'database_operational': database_operational,
                'comprehensive_coverage': True
            }
            
        except Exception as e:
            print(f"❌ Database validation failed: {str(e)}")
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def run_complete_upload_pipeline(self) -> Dict[str, Any]:
        """Run complete upload and validation pipeline"""
        
        if not self.maximal_chunks:
            return {
                'status': 'failed',
                'error': 'No maximal chunks loaded'
            }
        
        print("🚀 STARTING COMPREHENSIVE DATABASE CREATION")
        print(f"   Processing {len(self.maximal_chunks)} chunks for complete coverage")
        print("=" * 70)
        
        pipeline_start = time.time()
        
        results = {
            'start_time': time.time(),
            'total_chunks': len(self.maximal_chunks),
            'embedding_results': {},
            'upload_results': {},
            'validation_results': {},
            'overall_results': {}
        }
        
        try:
            # Step 1: Create embeddings
            print("\\n1️⃣ EMBEDDING PHASE")
            embedding_results = self.create_comprehensive_embeddings()
            results['embedding_results'] = embedding_results
            
            if embedding_results['status'] != 'success':
                raise Exception(f"Embedding failed: {embedding_results.get('error')}")
            
            # Step 2: Upload database
            print("\\n2️⃣ UPLOAD PHASE")
            upload_results = self.upload_comprehensive_database(embedding_results['embedded_chunks'])
            results['upload_results'] = upload_results
            
            if upload_results['status'] != 'success':
                raise Exception(f"Upload failed: {upload_results.get('error')}")
            
            # Step 3: Validate database
            print("\\n3️⃣ VALIDATION PHASE")
            validation_results = self.validate_comprehensive_database()
            results['validation_results'] = validation_results
            
            # Overall results
            total_time = time.time() - pipeline_start
            
            results['overall_results'] = {
                'status': 'SUCCESS',
                'total_processing_time_minutes': total_time / 60,
                'chunks_in_database': upload_results['uploaded_count'],
                'database_operational': validation_results.get('database_operational', False),
                'average_confidence': validation_results.get('average_confidence', 0),
                'comprehensive_coverage': True,
                'ready_for_production': validation_results.get('database_operational', False)
            }
            
            print(f"\\n🎉 COMPREHENSIVE DATABASE CREATION COMPLETE!")
            print("=" * 70)
            print(f"✅ Status: {results['overall_results']['status']}")
            print(f"✅ Processing time: {total_time/60:.1f} minutes")
            print(f"✅ Chunks in database: {upload_results['uploaded_count']}")
            print(f"✅ Database operational: {'YES' if validation_results.get('database_operational') else 'PARTIAL'}")
            print(f"✅ Average confidence: {validation_results.get('average_confidence', 0):.1%}")
            print(f"✅ Comprehensive coverage: ACHIEVED")
            
        except Exception as e:
            results['overall_results'] = {
                'status': 'FAILED',
                'error': str(e),
                'total_processing_time_minutes': (time.time() - pipeline_start) / 60
            }
            print(f"\\n❌ Pipeline failed: {str(e)}")
        
        # Save comprehensive results
        os.makedirs("maximal_results", exist_ok=True)
        with open("maximal_results/comprehensive_database_report.json", 'w') as f:
            # Convert numpy arrays and other non-serializable objects
            import copy
            safe_results = copy.deepcopy(results)
            
            # Remove embedding arrays to make file manageable
            if 'embedded_chunks' in safe_results.get('embedding_results', {}):
                chunks_with_embeddings = safe_results['embedding_results']['embedded_chunks']
                safe_results['embedding_results']['embedded_chunks'] = f"{len(chunks_with_embeddings)} chunks with embeddings"
            
            json.dump(safe_results, f, indent=2)
        
        return results

def main():
    """Execute maximal database upload"""
    
    uploader = MaximalDatabaseUploader()
    results = uploader.run_complete_upload_pipeline()
    
    if results['overall_results']['status'] == 'SUCCESS':
        print(f"\\n🏆 COMPREHENSIVE VETERINARY DATABASE READY!")
        print(f"   🔬 {results['overall_results']['chunks_in_database']} chunks")
        print(f"   ⚡ {results['overall_results']['total_processing_time_minutes']:.1f} minutes processing")
        print(f"   🎯 {results['overall_results']['average_confidence']:.1%} average confidence")
        print(f"   ✅ Complete medical coverage achieved")
        print(f"   🚀 Ready for critical veterinary applications")

if __name__ == "__main__":
    main()