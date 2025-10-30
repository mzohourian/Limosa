#!/usr/bin/env python3
"""
Maximal Veterinary Extractor
AGGRESSIVE extraction for near 100% coverage - Critical medical database
"""

import fitz
import re
import json
from typing import List, Dict, Any
from tqdm import tqdm
import os

class MaximalVeterinaryExtractor:
    def __init__(self):
        """Initialize maximal extractor for absolute maximum coverage"""
        print("🚨 INITIALIZING MAXIMAL VETERINARY EXTRACTOR")
        print("   STRATEGY: Extract EVERYTHING - No content left behind")
        print("   TARGET: 15,000+ chunks for complete medical coverage")
        print("=" * 70)
        
        # Medical keywords - if ANY of these appear, we extract the content
        self.medical_keywords = [
            'mg', 'kg', 'dose', 'dosage', 'administration', 'drug', 'medication',
            'veterinary', 'animal', 'dog', 'cat', 'horse', 'cattle', 'pig',
            'sheep', 'goat', 'bird', 'reptile', 'fish', 'exotic',
            'injection', 'oral', 'topical', 'intravenous', 'subcutaneous',
            'intramuscular', 'treatment', 'therapy', 'clinical', 'patient',
            'contraindication', 'adverse', 'side effect', 'toxicity',
            'pharmacology', 'mechanism', 'indication', 'monitoring',
            'pregnancy', 'lactation', 'pediatric', 'geriatric',
            'antibiotic', 'analgesic', 'anti-inflammatory', 'sedative',
            'anesthetic', 'anticonvulsant', 'cardiac', 'respiratory',
            'gastrointestinal', 'renal', 'hepatic', 'dermatologic'
        ]
        
        print(f"📋 Monitoring {len(self.medical_keywords)} medical keywords")
        print("✅ Maximal extractor ready")
    
    def extract_everything(self, pdf_path: str) -> List[Dict]:
        """Extract absolutely everything from the handbook"""
        
        print(f"\\n📖 MAXIMAL EXTRACTION: {pdf_path}")
        print("   Extracting every piece of potential medical content")
        print("-" * 70)
        
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        
        all_chunks = []
        chunk_id = 0
        
        print(f"📄 Processing all {total_pages} pages...")
        
        for page_num in tqdm(range(total_pages), desc="Maximal extraction"):
            try:
                page = doc.load_page(page_num)
                page_text = page.get_text()
                
                if len(page_text.strip()) < 10:  # Skip truly empty pages
                    continue
                
                # STRATEGY 1: Fixed-size overlapping chunks (most comprehensive)
                chunk_size = 400
                overlap = 150
                
                for i in range(0, len(page_text), chunk_size - overlap):
                    chunk_text = page_text[i:i + chunk_size]
                    
                    if len(chunk_text.strip()) > 30:
                        # Check if this chunk contains medical content
                        chunk_lower = chunk_text.lower()
                        medical_score = sum(1 for keyword in self.medical_keywords 
                                          if keyword in chunk_lower)
                        
                        # AGGRESSIVE: Include if ANY medical content detected
                        if medical_score >= 1:
                            chunk_entry = {
                                'chunk_id': f'max_chunk_{chunk_id}',
                                'text': f"PAGE {page_num + 1}: {chunk_text.strip()}",
                                'metadata': {
                                    'page_number': page_num + 1,
                                    'chunk_type': 'medical_content',
                                    'category': 'veterinary_drug',
                                    'medical_score': medical_score,
                                    'char_start': i,
                                    'char_end': i + len(chunk_text),
                                    'extraction_method': 'maximal_overlapping'
                                }
                            }
                            all_chunks.append(chunk_entry)
                            chunk_id += 1
                
                # STRATEGY 2: Sentence-based extraction for context
                sentences = re.split(r'[.!?]\\n', page_text)
                for sent_idx, sentence in enumerate(sentences):
                    if len(sentence.strip()) > 50:
                        sent_lower = sentence.lower()
                        medical_score = sum(1 for keyword in self.medical_keywords 
                                          if keyword in sent_lower)
                        
                        if medical_score >= 2:  # Higher threshold for sentences
                            chunk_entry = {
                                'chunk_id': f'max_sentence_{chunk_id}',
                                'text': f"PAGE {page_num + 1} CONTEXT: {sentence.strip()}",
                                'metadata': {
                                    'page_number': page_num + 1,
                                    'chunk_type': 'medical_sentence',
                                    'category': 'veterinary_drug',
                                    'medical_score': medical_score,
                                    'sentence_index': sent_idx,
                                    'extraction_method': 'sentence_based'
                                }
                            }
                            all_chunks.append(chunk_entry)
                            chunk_id += 1
                
                # STRATEGY 3: Paragraph-based extraction
                paragraphs = page_text.split('\\n\\n')
                for para_idx, paragraph in enumerate(paragraphs):
                    if len(paragraph.strip()) > 100:
                        para_lower = paragraph.lower()
                        medical_score = sum(1 for keyword in self.medical_keywords 
                                          if keyword in para_lower)
                        
                        if medical_score >= 3:  # Even higher threshold for paragraphs
                            chunk_entry = {
                                'chunk_id': f'max_paragraph_{chunk_id}',
                                'text': f"PAGE {page_num + 1} SECTION: {paragraph.strip()}",
                                'metadata': {
                                    'page_number': page_num + 1,
                                    'chunk_type': 'medical_paragraph',
                                    'category': 'veterinary_drug',
                                    'medical_score': medical_score,
                                    'paragraph_index': para_idx,
                                    'extraction_method': 'paragraph_based'
                                }
                            }
                            all_chunks.append(chunk_entry)
                            chunk_id += 1
                
                # STRATEGY 4: Full page extraction for high medical density
                page_lower = page_text.lower()
                page_medical_score = sum(1 for keyword in self.medical_keywords 
                                       if keyword in page_lower)
                
                if page_medical_score >= 5:  # High medical density pages
                    # Split page into multiple chunks for better embedding
                    page_chunks = [page_text[i:i+800] for i in range(0, len(page_text), 600)]
                    
                    for pc_idx, page_chunk in enumerate(page_chunks):
                        if len(page_chunk.strip()) > 100:
                            chunk_entry = {
                                'chunk_id': f'max_page_section_{chunk_id}',
                                'text': f"PAGE {page_num + 1} COMPREHENSIVE SECTION {pc_idx + 1}: {page_chunk.strip()}",
                                'metadata': {
                                    'page_number': page_num + 1,
                                    'chunk_type': 'comprehensive_page_section',
                                    'category': 'veterinary_drug',
                                    'medical_score': page_medical_score,
                                    'section_index': pc_idx,
                                    'extraction_method': 'comprehensive_page'
                                }
                            }
                            all_chunks.append(chunk_entry)
                            chunk_id += 1
            
            except Exception as e:
                print(f"⚠️ Page {page_num + 1} failed: {str(e)}")
                continue
        
        doc.close()
        
        print(f"\\n✅ MAXIMAL EXTRACTION COMPLETE:")
        print(f"   Total chunks extracted: {len(all_chunks)}")
        print(f"   Average chunks per page: {len(all_chunks)/total_pages:.1f}")
        print(f"   Coverage target: {len(all_chunks)/15000*100:.1f}% of maximum target")
        
        return all_chunks
    
    def enhance_chunks_with_drug_detection(self, chunks: List[Dict]) -> List[Dict]:
        """Enhance chunks with drug name detection and classification"""
        
        print(f"\\n🔍 ENHANCING {len(chunks)} CHUNKS WITH DRUG DETECTION")
        print("-" * 70)
        
        # Common drug name patterns
        drug_patterns = [
            r'\\b([A-Z][a-z]{3,}(?:cillin|mycin|zole|pine|pam|done|ide|ine|ate|ol))\\b',  # Drug suffixes
            r'\\b([A-Z][a-z]{2,}(?:\\s+[A-Z][a-z]+)*)\\s+(?:mg|µg|g|mL)',  # Drug + dosage
            r'\\b([A-Z][a-z]{4,})\\s+(?:is|was|should|may|can)\\s+(?:used|given|administered)',  # Drug + usage
            r'\\b([A-Z][a-z]{3,})\\s*\\([^)]*\\)\\s*(?:is|was)',  # Drug (synonym) is/was
            r'^\\s*([A-Z][a-z]{3,}(?:\\s+[A-Z][a-z]+)*)\\s*$',  # Standalone drug names
        ]
        
        enhanced_chunks = []
        
        for chunk in tqdm(chunks, desc="Enhancing with drug detection"):
            chunk_text = chunk['text']
            
            # Detect potential drug names
            detected_drugs = set()
            
            for pattern in drug_patterns:
                matches = re.findall(pattern, chunk_text)
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[0] if match[0] else match[1]
                    
                    if self._looks_like_drug(match):
                        detected_drugs.add(match.strip())
            
            # Enhance metadata
            chunk['metadata']['detected_drugs'] = list(detected_drugs)
            chunk['metadata']['drug_count'] = len(detected_drugs)
            
            # Classify chunk type based on content
            chunk_type = self._classify_chunk_type(chunk_text)
            chunk['metadata']['content_classification'] = chunk_type
            
            # Calculate comprehensive relevance score
            relevance_score = (
                chunk['metadata']['medical_score'] * 2 +
                len(detected_drugs) * 3 +
                self._content_quality_score(chunk_text)
            )
            chunk['metadata']['comprehensive_relevance'] = relevance_score
            
            enhanced_chunks.append(chunk)
        
        # Sort by relevance for quality
        enhanced_chunks.sort(key=lambda x: x['metadata']['comprehensive_relevance'], reverse=True)
        
        print(f"✅ Enhancement complete:")
        print(f"   Chunks with detected drugs: {sum(1 for c in enhanced_chunks if c['metadata']['drug_count'] > 0)}")
        print(f"   Average drugs per chunk: {sum(c['metadata']['drug_count'] for c in enhanced_chunks) / len(enhanced_chunks):.2f}")
        
        return enhanced_chunks
    
    def _looks_like_drug(self, text: str) -> bool:
        """Check if text looks like a drug name"""
        if len(text) < 3 or len(text) > 40:
            return False
        
        # Must start with capital letter
        if not text[0].isupper():
            return False
        
        # Exclude common non-drugs
        exclude = [
            'The', 'This', 'That', 'Table', 'Figure', 'Page', 'Chapter',
            'However', 'Therefore', 'Although', 'Because', 'During',
            'Patients', 'Animals', 'Dogs', 'Cats', 'Horses', 'Cattle'
        ]
        
        if text in exclude:
            return False
        
        # Good indicators
        good_indicators = [
            text.endswith(('cillin', 'mycin', 'zole', 'pine', 'pam', 'done', 'ide', 'ine', 'ate', 'ol')),
            any(char.isdigit() for char in text),  # Contains numbers (like dosage forms)
            len(text) >= 6,  # Reasonable drug name length
        ]
        
        return any(good_indicators)
    
    def _classify_chunk_type(self, text: str) -> str:
        """Classify the type of medical content"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['dosage', 'dose', 'mg/kg', 'administration']):
            return 'dosage_information'
        elif any(word in text_lower for word in ['contraindication', 'avoid', 'should not']):
            return 'safety_information'
        elif any(word in text_lower for word in ['adverse', 'side effect', 'toxicity']):
            return 'adverse_effects'
        elif any(word in text_lower for word in ['indication', 'used for', 'treatment']):
            return 'indications'
        elif any(word in text_lower for word in ['pharmacology', 'mechanism', 'action']):
            return 'pharmacology'
        elif any(word in text_lower for word in ['monitoring', 'laboratory', 'check']):
            return 'monitoring'
        else:
            return 'general_medical'
    
    def _content_quality_score(self, text: str) -> int:
        """Calculate content quality score"""
        score = 0
        
        # Length bonus
        if len(text) > 100:
            score += 1
        if len(text) > 300:
            score += 1
        
        # Structure bonus
        if ':' in text or '■' in text or '•' in text:
            score += 2
        
        # Specific medical info bonus
        if re.search(r'\\d+\\s*mg', text):
            score += 3
        if re.search(r'\\d+\\s*mg/kg', text):
            score += 4
        
        return score

def main():
    """Execute maximal extraction"""
    
    extractor = MaximalVeterinaryExtractor()
    pdf_path = "my_project_docs/vet/plumb_veterinary_drug_handbook.pdf"
    
    # Step 1: Maximal extraction
    all_chunks = extractor.extract_everything(pdf_path)
    
    # Step 2: Enhance with drug detection
    enhanced_chunks = extractor.enhance_chunks_with_drug_detection(all_chunks)
    
    # Step 3: Save results
    os.makedirs("maximal_results", exist_ok=True)
    
    with open("maximal_results/maximal_chunks.json", 'w', encoding='utf-8') as f:
        json.dump(enhanced_chunks, f, indent=2, ensure_ascii=False)
    
    print(f"\\n🎯 MAXIMAL EXTRACTION RESULTS:")
    print(f"   Total chunks: {len(enhanced_chunks)}")
    print(f"   Target (15,000): {'✅ ACHIEVED' if len(enhanced_chunks) >= 15000 else f'❌ Need {15000 - len(enhanced_chunks)} more'}")
    print(f"   Coverage: {len(enhanced_chunks)/15000*100:.1f}%")
    print(f"   Data saved to: maximal_results/maximal_chunks.json")
    
    # Quality metrics
    drug_chunks = [c for c in enhanced_chunks if c['metadata']['drug_count'] > 0]
    high_relevance = [c for c in enhanced_chunks if c['metadata']['comprehensive_relevance'] >= 10]
    
    print(f"\\n📊 QUALITY METRICS:")
    print(f"   Chunks with drugs: {len(drug_chunks)} ({len(drug_chunks)/len(enhanced_chunks)*100:.1f}%)")
    print(f"   High relevance chunks: {len(high_relevance)} ({len(high_relevance)/len(enhanced_chunks)*100:.1f}%)")
    
    return enhanced_chunks

if __name__ == "__main__":
    main()