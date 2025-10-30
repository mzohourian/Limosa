#!/usr/bin/env python3
"""
Database Quality Reviewer
Comprehensive review of extracted chunks for accuracy and usability
"""

import json
import os
import re
from typing import List, Dict, Any
from collections import Counter
from datetime import datetime
from final_95_confidence import Final95ConfidenceAssistant

class DatabaseQualityReviewer:
    def __init__(self):
        """Initialize database quality reviewer"""
        print("🔍 INITIALIZING DATABASE QUALITY REVIEWER")
        print("   Mission: Verify accuracy and usability of extracted chunks")
        print("=" * 70)
        
        self.assistant = Final95ConfidenceAssistant()
        
    def load_sample_chunks(self, sample_size: int = 1000) -> List[Dict]:
        """Load a representative sample of chunks for analysis"""
        
        print(f"\n📦 LOADING SAMPLE CHUNKS FOR ANALYSIS")
        print("-" * 50)
        
        chunks_file = "maximal_results/maximal_chunks.json"
        
        if not os.path.exists(chunks_file):
            print(f"❌ Chunks file not found: {chunks_file}")
            return []
        
        try:
            with open(chunks_file, 'r', encoding='utf-8') as f:
                all_chunks = json.load(f)
            
            print(f"📥 Total chunks available: {len(all_chunks)}")
            
            # Take stratified sample
            sample_chunks = []
            step = len(all_chunks) // sample_size if len(all_chunks) > sample_size else 1
            
            for i in range(0, len(all_chunks), step):
                if len(sample_chunks) >= sample_size:
                    break
                sample_chunks.append(all_chunks[i])
            
            print(f"✅ Loaded {len(sample_chunks)} sample chunks for analysis")
            return sample_chunks
            
        except Exception as e:
            print(f"❌ Failed to load chunks: {str(e)}")
            return []
    
    def analyze_chunk_content_quality(self, chunks: List[Dict]) -> Dict[str, Any]:
        """Analyze the quality of chunk content"""
        
        print(f"\n🔍 ANALYZING CHUNK CONTENT QUALITY")
        print("-" * 50)
        
        quality_metrics = {
            'total_chunks': len(chunks),
            'text_length_stats': {},
            'medical_content_analysis': {},
            'chunk_type_distribution': {},
            'content_issues': [],
            'quality_scores': []
        }
        
        # Text length analysis
        text_lengths = [len(chunk['text']) for chunk in chunks]
        quality_metrics['text_length_stats'] = {
            'min': min(text_lengths) if text_lengths else 0,
            'max': max(text_lengths) if text_lengths else 0,
            'average': sum(text_lengths) / len(text_lengths) if text_lengths else 0,
            'chunks_too_short': sum(1 for l in text_lengths if l < 50),
            'chunks_too_long': sum(1 for l in text_lengths if l > 2000),
            'optimal_length_chunks': sum(1 for l in text_lengths if 100 <= l <= 800)
        }
        
        # Medical content analysis
        medical_keywords = [
            'mg', 'kg', 'dose', 'dosage', 'administration', 'contraindication',
            'adverse', 'side effect', 'veterinary', 'drug', 'medication',
            'treatment', 'therapy', 'clinical', 'patient', 'animal'
        ]
        
        chunks_with_medical_content = 0
        total_medical_keywords = 0
        
        for chunk in chunks:
            text_lower = chunk['text'].lower()
            medical_count = sum(1 for keyword in medical_keywords if keyword in text_lower)
            
            if medical_count > 0:
                chunks_with_medical_content += 1
                total_medical_keywords += medical_count
        
        quality_metrics['medical_content_analysis'] = {
            'chunks_with_medical_content': chunks_with_medical_content,
            'percentage_medical': chunks_with_medical_content / len(chunks) * 100 if chunks else 0,
            'average_medical_keywords_per_chunk': total_medical_keywords / len(chunks) if chunks else 0
        }
        
        # Chunk type distribution
        chunk_types = [chunk['metadata'].get('chunk_type', 'unknown') for chunk in chunks]
        quality_metrics['chunk_type_distribution'] = dict(Counter(chunk_types))
        
        # Content quality scoring
        for chunk in chunks:
            score = self._calculate_content_quality_score(chunk)
            quality_metrics['quality_scores'].append(score)
        
        avg_quality = sum(quality_metrics['quality_scores']) / len(quality_metrics['quality_scores']) if quality_metrics['quality_scores'] else 0
        quality_metrics['average_quality_score'] = avg_quality
        
        print(f"📊 CONTENT QUALITY ANALYSIS:")
        print(f"   Average text length: {quality_metrics['text_length_stats']['average']:.1f} characters")
        print(f"   Chunks with medical content: {quality_metrics['medical_content_analysis']['percentage_medical']:.1f}%")
        print(f"   Average quality score: {avg_quality:.2f}/10")
        print(f"   Optimal length chunks: {quality_metrics['text_length_stats']['optimal_length_chunks']}/{len(chunks)}")
        
        return quality_metrics
    
    def _calculate_content_quality_score(self, chunk: Dict) -> float:
        """Calculate quality score for a chunk (0-10 scale)"""
        
        text = chunk['text']
        metadata = chunk['metadata']
        score = 5.0  # Base score
        
        # Text length scoring
        length = len(text)
        if 100 <= length <= 800:
            score += 2.0
        elif 50 <= length < 100 or 800 < length <= 1200:
            score += 1.0
        elif length < 50:
            score -= 2.0
        
        # Medical content scoring
        medical_score = metadata.get('medical_score', 0)
        if medical_score >= 3:
            score += 2.0
        elif medical_score >= 1:
            score += 1.0
        
        # Relevance scoring
        relevance = metadata.get('comprehensive_relevance', 0)
        if relevance >= 15:
            score += 1.0
        elif relevance >= 10:
            score += 0.5
        
        return min(max(score, 0), 10)
    
    def identify_actual_drugs_in_chunks(self, chunks: List[Dict]) -> Dict[str, Any]:
        """Identify actual drug names mentioned in chunks"""
        
        print(f"\n💊 IDENTIFYING ACTUAL DRUG NAMES")
        print("-" * 50)
        
        # Common veterinary drug patterns
        drug_patterns = [
            r'\b([A-Z][a-z]{3,}cillin)\b',  # Antibiotics ending in -cillin
            r'\b([A-Z][a-z]{3,}mycin)\b',   # Antibiotics ending in -mycin
            r'\b([A-Z][a-z]{3,}zole)\b',    # Antifungals ending in -zole
            r'\b(Acarbose|Albendazole|Acepromazine|Albuterol|Aspirin|Ampicillin)\b',  # Known drugs
            r'\b([A-Z][a-z]{4,})\s+(?:\d+\s*mg|\d+\s*mg/kg)\b',  # Drug + dosage
        ]
        
        detected_drugs = set()
        drug_mentions = Counter()
        chunks_with_drugs = 0
        
        for chunk in chunks:
            text = chunk['text']
            chunk_drugs = set()
            
            for pattern in drug_patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    if self._is_likely_drug_name(match):
                        detected_drugs.add(match)
                        drug_mentions[match] += 1
                        chunk_drugs.add(match)
            
            if chunk_drugs:
                chunks_with_drugs += 1
        
        drug_analysis = {
            'total_unique_drugs': len(detected_drugs),
            'most_mentioned_drugs': drug_mentions.most_common(10),
            'chunks_with_drug_names': chunks_with_drugs,
            'percentage_chunks_with_drugs': chunks_with_drugs / len(chunks) * 100 if chunks else 0,
            'detected_drugs_list': sorted(list(detected_drugs))
        }
        
        print(f"💊 DRUG IDENTIFICATION RESULTS:")
        print(f"   Unique drugs identified: {len(detected_drugs)}")
        print(f"   Chunks containing drug names: {chunks_with_drugs}/{len(chunks)} ({drug_analysis['percentage_chunks_with_drugs']:.1f}%)")
        
        if drug_analysis['most_mentioned_drugs']:
            print(f"   Top mentioned drugs:")
            for drug, count in drug_analysis['most_mentioned_drugs'][:5]:
                print(f"     • {drug}: {count} mentions")
        
        return drug_analysis
    
    def _is_likely_drug_name(self, name: str) -> bool:
        """Check if detected name is likely a real drug"""
        
        if len(name) < 4 or len(name) > 20:
            return False
        
        # Must start with capital
        if not name[0].isupper():
            return False
        
        # Exclude common false positives
        exclude = [
            'Page', 'Figure', 'Table', 'Chapter', 'Section', 'Notes',
            'Dogs', 'Cats', 'Horses', 'Animals', 'Patients', 'Clinical'
        ]
        
        return name not in exclude
    
    def test_database_functionality(self) -> Dict[str, Any]:
        """Test actual database functionality with real queries"""
        
        print(f"\n🧪 TESTING DATABASE FUNCTIONALITY")
        print("-" * 50)
        
        # Comprehensive test queries
        test_queries = [
            {
                'query': 'Acarbose dosing for dogs',
                'category': 'Dosing',
                'expected_elements': ['mg', 'dose', 'dog', 'administration']
            },
            {
                'query': 'What is Albendazole used for?',
                'category': 'Indications',
                'expected_elements': ['treatment', 'indication', 'used']
            },
            {
                'query': 'Acepromazine side effects',
                'category': 'Adverse Effects',
                'expected_elements': ['adverse', 'effect', 'side']
            },
            {
                'query': 'How does Albuterol work?',
                'category': 'Pharmacology',
                'expected_elements': ['mechanism', 'action', 'work']
            },
            {
                'query': 'Aspirin contraindications in cats',
                'category': 'Safety',
                'expected_elements': ['contraindication', 'cat', 'avoid']
            },
            {
                'query': 'Antibiotic for respiratory infection in horses',
                'category': 'General Query',
                'expected_elements': ['antibiotic', 'respiratory', 'horse']
            }
        ]
        
        test_results = []
        successful_queries = 0
        total_confidence = 0
        
        for test in test_queries:
            try:
                print(f"🔬 Testing: {test['query']}")
                
                result = self.assistant.query_with_high_confidence(test['query'])
                
                confidence = min(result['confidence'], 1.0)
                drugs_found = len(result.get('drugs_found', []))
                chunks_used = result.get('high_confidence_chunks', 0)
                response = result['answer']
                
                # Check for expected elements
                response_lower = response.lower()
                elements_found = sum(1 for elem in test['expected_elements'] 
                                   if elem.lower() in response_lower)
                element_coverage = elements_found / len(test['expected_elements'])
                
                # Determine success
                success = (confidence >= 0.80 and 
                          drugs_found > 0 and 
                          chunks_used >= 3 and
                          element_coverage >= 0.5)
                
                if success:
                    successful_queries += 1
                
                total_confidence += confidence
                
                test_result = {
                    'query': test['query'],
                    'category': test['category'],
                    'confidence': confidence,
                    'drugs_found': drugs_found,
                    'chunks_used': chunks_used,
                    'element_coverage': element_coverage,
                    'success': success,
                    'response_length': len(response),
                    'response_preview': response[:200] + "..." if len(response) > 200 else response
                }
                
                test_results.append(test_result)
                
                print(f"   ✅ Confidence: {confidence:.1%}, Drugs: {drugs_found}, Chunks: {chunks_used}, Success: {'✅' if success else '❌'}")
                
            except Exception as e:
                print(f"   ❌ Query failed: {str(e)}")
                test_results.append({
                    'query': test['query'],
                    'category': test['category'],
                    'error': str(e),
                    'success': False
                })
        
        avg_confidence = total_confidence / len(test_queries) if test_queries else 0
        success_rate = successful_queries / len(test_queries) if test_queries else 0
        
        functionality_results = {
            'total_queries_tested': len(test_queries),
            'successful_queries': successful_queries,
            'success_rate': success_rate,
            'average_confidence': avg_confidence,
            'test_results': test_results,
            'database_functional': success_rate >= 0.70 and avg_confidence >= 0.80
        }
        
        print(f"\n📊 FUNCTIONALITY TEST RESULTS:")
        print(f"   Success rate: {success_rate:.1%} ({successful_queries}/{len(test_queries)})")
        print(f"   Average confidence: {avg_confidence:.1%}")
        print(f"   Database functional: {'✅ YES' if functionality_results['database_functional'] else '❌ ISSUES DETECTED'}")
        
        return functionality_results
    
    def generate_quality_report(self) -> Dict[str, Any]:
        """Generate comprehensive quality report"""
        
        print(f"\n📋 GENERATING COMPREHENSIVE QUALITY REPORT")
        print("=" * 70)
        
        # Load sample for analysis
        sample_chunks = self.load_sample_chunks(1000)
        
        if not sample_chunks:
            return {
                'status': 'failed',
                'error': 'No chunks available for analysis'
            }
        
        # Perform all analyses
        content_quality = self.analyze_chunk_content_quality(sample_chunks)
        drug_analysis = self.identify_actual_drugs_in_chunks(sample_chunks)
        functionality_test = self.test_database_functionality()
        
        # Overall assessment
        overall_score = 0
        max_score = 100
        
        # Content quality scoring (40 points)
        if content_quality['average_quality_score'] >= 7:
            overall_score += 40
        elif content_quality['average_quality_score'] >= 5:
            overall_score += 25
        elif content_quality['average_quality_score'] >= 3:
            overall_score += 15
        
        # Medical content scoring (30 points)
        medical_percentage = content_quality['medical_content_analysis']['percentage_medical']
        if medical_percentage >= 80:
            overall_score += 30
        elif medical_percentage >= 60:
            overall_score += 20
        elif medical_percentage >= 40:
            overall_score += 10
        
        # Functionality scoring (30 points)
        if functionality_test['database_functional']:
            overall_score += 30
        elif functionality_test['success_rate'] >= 0.5:
            overall_score += 15
        
        # Final assessment
        if overall_score >= 85:
            quality_grade = "EXCELLENT"
            production_ready = True
        elif overall_score >= 70:
            quality_grade = "GOOD" 
            production_ready = True
        elif overall_score >= 50:
            quality_grade = "FAIR"
            production_ready = False
        else:
            quality_grade = "POOR"
            production_ready = False
        
        quality_report = {
            'timestamp': str(datetime.now()),
            'sample_size': len(sample_chunks),
            'content_quality_analysis': content_quality,
            'drug_identification_analysis': drug_analysis,
            'functionality_test_results': functionality_test,
            'overall_assessment': {
                'quality_score': overall_score,
                'quality_grade': quality_grade,
                'production_ready': production_ready,
                'key_strengths': [],
                'areas_for_improvement': [],
                'recommendations': []
            }
        }
        
        # Identify strengths and weaknesses
        strengths = []
        improvements = []
        recommendations = []
        
        if content_quality['average_quality_score'] >= 6:
            strengths.append("High-quality content extraction")
        else:
            improvements.append("Content quality could be improved")
            recommendations.append("Review extraction filters and chunk size optimization")
        
        if medical_percentage >= 70:
            strengths.append("Strong medical content coverage")
        else:
            improvements.append("Medical content detection needs enhancement")
            recommendations.append("Expand medical keyword dictionary and improve filtering")
        
        if drug_analysis['total_unique_drugs'] >= 50:
            strengths.append("Good drug name identification")
        else:
            improvements.append("Drug identification could be enhanced")
            recommendations.append("Improve drug name detection patterns")
        
        if functionality_test['database_functional']:
            strengths.append("Database queries working effectively")
        else:
            improvements.append("Database functionality issues detected")
            recommendations.append("Review query processing and confidence thresholds")
        
        quality_report['overall_assessment']['key_strengths'] = strengths
        quality_report['overall_assessment']['areas_for_improvement'] = improvements
        quality_report['overall_assessment']['recommendations'] = recommendations
        
        # Save report
        os.makedirs("quality_review_results", exist_ok=True)
        with open("quality_review_results/database_quality_report.json", 'w') as f:
            json.dump(quality_report, f, indent=2, ensure_ascii=False)
        
        print(f"\n🎯 QUALITY REVIEW COMPLETE!")
        print(f"   Overall Score: {overall_score}/100")
        print(f"   Quality Grade: {quality_grade}")
        print(f"   Production Ready: {'✅ YES' if production_ready else '❌ NO'}")
        print(f"   Report saved: quality_review_results/database_quality_report.json")
        
        return quality_report

def main():
    """Execute comprehensive database quality review"""
    
    reviewer = DatabaseQualityReviewer()
    report = reviewer.generate_quality_report()
    
    print(f"\n🏆 DATABASE QUALITY REVIEW SUMMARY:")
    print("=" * 70)
    
    if report.get('overall_assessment'):
        assessment = report['overall_assessment']
        print(f"Quality Score: {assessment['quality_score']}/100")
        print(f"Quality Grade: {assessment['quality_grade']}")
        print(f"Production Ready: {assessment['production_ready']}")
        
        if assessment['key_strengths']:
            print(f"\n✅ Key Strengths:")
            for strength in assessment['key_strengths']:
                print(f"   • {strength}")
        
        if assessment['areas_for_improvement']:
            print(f"\n⚠️ Areas for Improvement:")
            for improvement in assessment['areas_for_improvement']:
                print(f"   • {improvement}")

if __name__ == "__main__":
    main()