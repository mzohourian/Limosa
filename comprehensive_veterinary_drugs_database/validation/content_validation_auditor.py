#!/usr/bin/env python3
"""
Content Validation Auditor
Alternative approach to verify extraction accuracy through content analysis
"""

import json
import os
import re
from typing import List, Dict, Any
from collections import Counter
import random
from datetime import datetime

class ContentValidationAuditor:
    def __init__(self):
        """Initialize content validation auditor"""
        print("🔍 INITIALIZING CONTENT VALIDATION AUDITOR")
        print("   Mission: Validate extraction quality through content analysis")
        print("   Approach: Analyze patterns, completeness, and consistency")
        print("=" * 70)
        
        self.chunks_file = "maximal_results/maximal_chunks.json"
        self.chunks = self._load_chunks()
        
        print(f"📦 Loaded {len(self.chunks)} chunks for validation")
        print("✅ Content validation auditor ready")
    
    def _load_chunks(self) -> List[Dict]:
        """Load extracted chunks"""
        
        if not os.path.exists(self.chunks_file):
            print(f"❌ Chunks file not found: {self.chunks_file}")
            return []
        
        try:
            with open(self.chunks_file, 'r', encoding='utf-8') as f:
                chunks = json.load(f)
            
            print(f"✅ Successfully loaded {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            print(f"❌ Failed to load chunks: {str(e)}")
            return []
    
    def analyze_content_patterns(self) -> Dict[str, Any]:
        """Analyze content patterns to detect extraction quality"""
        
        print(f"\n🔍 ANALYZING CONTENT PATTERNS")
        print("-" * 50)
        
        pattern_analysis = {
            'drug_sections': 0,
            'dosing_information': 0,
            'contraindications': 0,
            'adverse_effects': 0,
            'pharmacology': 0,
            'administration_routes': 0,
            'species_specific': 0,
            'chemical_names': 0,
            'proper_medical_structure': 0,
            'incomplete_sentences': 0,
            'truncated_content': 0
        }
        
        # Define patterns for medical content
        drug_patterns = [
            r'\b[A-Z][a-z]{3,}(?:cillin|mycin|zole|prazole|dipine|olol|sartan)\b',
            r'\b(?:ACEPROMAZINE|ALBENDAZOLE|INSULIN|ASPIRIN|DIGOXIN)\b',
        ]
        
        dosing_patterns = [
            r'\d+(?:\.\d+)?\s*(?:mg|g|ml|units?)/kg',
            r'\d+(?:\.\d+)?\s*(?:mg|g|ml|units?)\s*(?:PO|IV|IM|SC|SQ)',
            r'(?:dose|dosage|administer)\s*:?\s*\d+',
            r'(?:daily|twice daily|q\d+h|BID|TID|QID)'
        ]
        
        contraindication_patterns = [
            r'(?:contraindicated|contraindication|avoid|not recommended)',
            r'(?:hypersensitivity|allergy|allergic)',
            r'(?:pregnancy|lactation|breeding)',
            r'(?:renal|hepatic|cardiac)\s*(?:impairment|failure|disease)'
        ]
        
        adverse_patterns = [
            r'(?:adverse|side)\s*effect',
            r'(?:vomiting|diarrhea|lethargy|ataxia)',
            r'(?:depression|sedation|excitement)',
            r'(?:toxicity|overdose|poisoning)'
        ]
        
        pharmacology_patterns = [
            r'(?:mechanism|action|receptor|binding)',
            r'(?:absorption|distribution|metabolism|elimination)',
            r'(?:half-life|clearance|bioavailability)',
            r'(?:pharmacokinetics|pharmacodynamics)'
        ]
        
        administration_patterns = [
            r'\b(?:PO|IV|IM|SC|SQ|topical|oral|intravenous|intramuscular|subcutaneous)\b',
            r'(?:route|administration|apply|inject|give)',
            r'(?:tablet|capsule|injection|solution|cream|ointment)'
        ]
        
        species_patterns = [
            r'\b(?:dog|canine|cat|feline|horse|equine|cow|bovine|sheep|ovine|pig|swine)\b',
            r'(?:dogs|cats|horses|cattle|livestock)',
            r'(?:small animal|large animal|companion animal)'
        ]
        
        print("🔬 Analyzing content patterns...")
        
        for i, chunk in enumerate(self.chunks):
            text = chunk['text'].lower()
            
            # Count drug-related patterns
            for pattern in drug_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    pattern_analysis['drug_sections'] += 1
                    break
            
            # Count dosing information
            for pattern in dosing_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    pattern_analysis['dosing_information'] += 1
                    break
            
            # Count contraindications
            for pattern in contraindication_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    pattern_analysis['contraindications'] += 1
                    break
            
            # Count adverse effects
            for pattern in adverse_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    pattern_analysis['adverse_effects'] += 1
                    break
            
            # Count pharmacology
            for pattern in pharmacology_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    pattern_analysis['pharmacology'] += 1
                    break
            
            # Count administration routes
            for pattern in administration_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    pattern_analysis['administration_routes'] += 1
                    break
            
            # Count species-specific info
            for pattern in species_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    pattern_analysis['species_specific'] += 1
                    break
            
            # Check for structural quality
            if len(text) > 100 and any(keyword in text for keyword in ['indication', 'dosage', 'contraindication', 'adverse', 'pharmacology']):
                pattern_analysis['proper_medical_structure'] += 1
            
            # Check for incomplete sentences
            if text.endswith(('...', 'see', 'refer', 'continued')) or len(text.split()) < 5:
                pattern_analysis['incomplete_sentences'] += 1
            
            # Check for truncated content
            if len(text) < 50 or text.count(' ') < 8:
                pattern_analysis['truncated_content'] += 1
            
            if i % 5000 == 0:
                print(f"   Processed {i:,}/{len(self.chunks):,} chunks...")
        
        # Calculate percentages
        total_chunks = len(self.chunks)
        pattern_percentages = {}
        for key, count in pattern_analysis.items():
            pattern_percentages[f"{key}_percentage"] = count / total_chunks * 100
        
        print(f"\n📊 CONTENT PATTERN ANALYSIS RESULTS:")
        print(f"   Drug sections: {pattern_analysis['drug_sections']:,} ({pattern_percentages['drug_sections_percentage']:.1f}%)")
        print(f"   Dosing information: {pattern_analysis['dosing_information']:,} ({pattern_percentages['dosing_information_percentage']:.1f}%)")
        print(f"   Contraindications: {pattern_analysis['contraindications']:,} ({pattern_percentages['contraindications_percentage']:.1f}%)")
        print(f"   Adverse effects: {pattern_analysis['adverse_effects']:,} ({pattern_percentages['adverse_effects_percentage']:.1f}%)")
        print(f"   Pharmacology: {pattern_analysis['pharmacology']:,} ({pattern_percentages['pharmacology_percentage']:.1f}%)")
        print(f"   Species-specific: {pattern_analysis['species_specific']:,} ({pattern_percentages['species_specific_percentage']:.1f}%)")
        print(f"   Proper structure: {pattern_analysis['proper_medical_structure']:,} ({pattern_percentages['proper_medical_structure_percentage']:.1f}%)")
        print(f"   Quality issues: {pattern_analysis['incomplete_sentences'] + pattern_analysis['truncated_content']:,}")
        
        return {**pattern_analysis, **pattern_percentages}
    
    def validate_drug_completeness(self) -> Dict[str, Any]:
        """Validate completeness of drug information"""
        
        print(f"\n💊 VALIDATING DRUG COMPLETENESS")
        print("-" * 50)
        
        # Identify all drugs mentioned
        drug_mentions = Counter()
        drug_contexts = {}
        
        drug_patterns = [
            r'\b([A-Z][a-z]{3,}cillin)\b',  # Antibiotics
            r'\b([A-Z][a-z]{3,}mycin)\b',   # Antibiotics
            r'\b([A-Z][a-z]{3,}zole)\b',    # Antifungals
            r'\b(ACEPROMAZINE|ALBENDAZOLE|INSULIN|ASPIRIN|DIGOXIN|AMPICILLIN)\b',
            r'\b([A-Z][a-z]{4,15})\s+(?:\d+\s*mg|\d+\s*ml|dose|dosage)\b'
        ]
        
        print("🔬 Identifying drug mentions...")
        
        for chunk in self.chunks:
            text = chunk['text']
            
            for pattern in drug_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    if self._is_valid_drug_name(match):
                        drug_name = match.title()
                        drug_mentions[drug_name] += 1
                        
                        if drug_name not in drug_contexts:
                            drug_contexts[drug_name] = {
                                'dosing_info': 0,
                                'contraindications': 0,
                                'adverse_effects': 0,
                                'pharmacology': 0,
                                'species_info': 0,
                                'sample_chunks': []
                            }
                        
                        # Analyze context for this drug
                        text_lower = text.lower()
                        if any(word in text_lower for word in ['mg/kg', 'dose', 'dosage', 'administer']):
                            drug_contexts[drug_name]['dosing_info'] += 1
                        if any(word in text_lower for word in ['contraindicated', 'avoid', 'not recommended']):
                            drug_contexts[drug_name]['contraindications'] += 1
                        if any(word in text_lower for word in ['adverse', 'side effect', 'toxicity']):
                            drug_contexts[drug_name]['adverse_effects'] += 1
                        if any(word in text_lower for word in ['mechanism', 'pharmacology', 'receptor']):
                            drug_contexts[drug_name]['pharmacology'] += 1
                        if any(word in text_lower for word in ['dog', 'cat', 'horse', 'canine', 'feline']):
                            drug_contexts[drug_name]['species_info'] += 1
                        
                        if len(drug_contexts[drug_name]['sample_chunks']) < 3:
                            drug_contexts[drug_name]['sample_chunks'].append(text[:200] + "...")
        
        # Analyze completeness for top drugs
        top_drugs = drug_mentions.most_common(20)
        completeness_analysis = {}
        
        for drug_name, mention_count in top_drugs:
            if drug_name in drug_contexts:
                context = drug_contexts[drug_name]
                completeness_score = 0
                
                # Score based on information types present
                if context['dosing_info'] > 0:
                    completeness_score += 25
                if context['contraindications'] > 0:
                    completeness_score += 25
                if context['adverse_effects'] > 0:
                    completeness_score += 20
                if context['pharmacology'] > 0:
                    completeness_score += 15
                if context['species_info'] > 0:
                    completeness_score += 15
                
                completeness_analysis[drug_name] = {
                    'mention_count': mention_count,
                    'completeness_score': completeness_score,
                    'context_breakdown': context,
                    'completeness_grade': 'EXCELLENT' if completeness_score >= 80 else
                                        'GOOD' if completeness_score >= 60 else
                                        'FAIR' if completeness_score >= 40 else 'POOR'
                }
        
        print(f"\n📊 DRUG COMPLETENESS ANALYSIS:")
        print(f"   Total unique drugs: {len(drug_mentions)}")
        print(f"   Top 10 drugs by mentions:")
        for drug_name, count in top_drugs[:10]:
            if drug_name in completeness_analysis:
                score = completeness_analysis[drug_name]['completeness_score']
                grade = completeness_analysis[drug_name]['completeness_grade']
                print(f"     • {drug_name}: {count} mentions, {score}/100 ({grade})")
        
        return {
            'total_unique_drugs': len(drug_mentions),
            'top_drugs': top_drugs[:20],
            'completeness_analysis': completeness_analysis,
            'average_completeness': sum(data['completeness_score'] for data in completeness_analysis.values()) / len(completeness_analysis) if completeness_analysis else 0
        }
    
    def _is_valid_drug_name(self, name: str) -> bool:
        """Check if detected name is likely a real drug"""
        
        if len(name) < 4 or len(name) > 20:
            return False
        
        # Must start with capital
        if not name[0].isupper():
            return False
        
        # Exclude common false positives
        exclude = [
            'Page', 'Figure', 'Table', 'Chapter', 'Section', 'Notes', 'References',
            'Dogs', 'Cats', 'Horses', 'Animals', 'Patients', 'Clinical', 'Treatment',
            'Because', 'However', 'Therefore', 'Although', 'During', 'After', 'Before',
            'Administration', 'Indication', 'Contraindication', 'Adverse', 'Dosage'
        ]
        
        return name not in exclude
    
    def validate_content_integrity(self) -> Dict[str, Any]:
        """Validate content integrity and coherence"""
        
        print(f"\n🔍 VALIDATING CONTENT INTEGRITY")
        print("-" * 50)
        
        integrity_metrics = {
            'chunks_with_complete_sentences': 0,
            'chunks_with_medical_terminology': 0,
            'chunks_with_proper_formatting': 0,
            'chunks_with_dosage_units': 0,
            'chunks_with_species_mentions': 0,
            'suspicious_chunks': [],
            'high_quality_chunks': 0
        }
        
        medical_terms = [
            'administration', 'contraindication', 'indication', 'dosage', 'pharmacokinetics',
            'metabolism', 'distribution', 'elimination', 'bioavailability', 'efficacy',
            'therapeutic', 'clinical', 'veterinary', 'treatment', 'diagnosis'
        ]
        
        dosage_units = ['mg', 'ml', 'units', 'kg', 'po', 'iv', 'im', 'sc']
        species = ['dog', 'cat', 'horse', 'cattle', 'canine', 'feline', 'equine', 'bovine']
        
        print("🔬 Analyzing content integrity...")
        
        sample_chunks = random.sample(self.chunks, min(5000, len(self.chunks)))
        
        for chunk in sample_chunks:
            text = chunk['text']
            text_lower = text.lower()
            
            # Check for complete sentences
            if text.endswith('.') and len(text.split('.')) >= 2:
                integrity_metrics['chunks_with_complete_sentences'] += 1
            
            # Check for medical terminology
            if any(term in text_lower for term in medical_terms):
                integrity_metrics['chunks_with_medical_terminology'] += 1
            
            # Check for proper formatting
            if re.search(r'[A-Z][a-z]+:', text) or re.search(r'\d+\.\s+', text):
                integrity_metrics['chunks_with_proper_formatting'] += 1
            
            # Check for dosage units
            if any(unit in text_lower for unit in dosage_units):
                integrity_metrics['chunks_with_dosage_units'] += 1
            
            # Check for species mentions
            if any(sp in text_lower for sp in species):
                integrity_metrics['chunks_with_species_mentions'] += 1
            
            # Identify suspicious chunks
            if (len(text) < 50 or 
                text.count('?') > 3 or 
                text.count('...') > 2 or
                len(set(text.split())) < len(text.split()) * 0.5):  # Too repetitive
                integrity_metrics['suspicious_chunks'].append({
                    'text': text[:100] + "...",
                    'length': len(text),
                    'issue': 'Short/repetitive/truncated'
                })
            
            # High quality chunks
            quality_score = 0
            quality_score += 1 if len(text) > 100 else 0
            quality_score += 1 if any(term in text_lower for term in medical_terms) else 0
            quality_score += 1 if any(unit in text_lower for unit in dosage_units) else 0
            quality_score += 1 if any(sp in text_lower for sp in species) else 0
            quality_score += 1 if text.count('.') >= 2 else 0
            
            if quality_score >= 4:
                integrity_metrics['high_quality_chunks'] += 1
        
        # Calculate percentages
        sample_size = len(sample_chunks)
        for key in ['chunks_with_complete_sentences', 'chunks_with_medical_terminology', 
                   'chunks_with_proper_formatting', 'chunks_with_dosage_units',
                   'chunks_with_species_mentions', 'high_quality_chunks']:
            integrity_metrics[f"{key}_percentage"] = integrity_metrics[key] / sample_size * 100
        
        print(f"\n📊 CONTENT INTEGRITY RESULTS:")
        print(f"   Complete sentences: {integrity_metrics['chunks_with_complete_sentences']}/{sample_size} ({integrity_metrics['chunks_with_complete_sentences_percentage']:.1f}%)")
        print(f"   Medical terminology: {integrity_metrics['chunks_with_medical_terminology']}/{sample_size} ({integrity_metrics['chunks_with_medical_terminology_percentage']:.1f}%)")
        print(f"   Proper formatting: {integrity_metrics['chunks_with_proper_formatting']}/{sample_size} ({integrity_metrics['chunks_with_proper_formatting_percentage']:.1f}%)")
        print(f"   Dosage information: {integrity_metrics['chunks_with_dosage_units']}/{sample_size} ({integrity_metrics['chunks_with_dosage_units_percentage']:.1f}%)")
        print(f"   Species mentions: {integrity_metrics['chunks_with_species_mentions']}/{sample_size} ({integrity_metrics['chunks_with_species_mentions_percentage']:.1f}%)")
        print(f"   High quality chunks: {integrity_metrics['high_quality_chunks']}/{sample_size} ({integrity_metrics['high_quality_chunks_percentage']:.1f}%)")
        print(f"   Suspicious chunks: {len(integrity_metrics['suspicious_chunks'])}")
        
        return integrity_metrics
    
    def generate_final_validation_report(self, pattern_analysis: Dict, drug_completeness: Dict, integrity_analysis: Dict) -> Dict[str, Any]:
        """Generate comprehensive validation report"""
        
        print(f"\n📋 GENERATING FINAL VALIDATION REPORT")
        print("=" * 70)
        
        # Calculate overall scores
        content_coverage_score = (
            pattern_analysis['drug_sections_percentage'] * 0.2 +
            pattern_analysis['dosing_information_percentage'] * 0.25 +
            pattern_analysis['contraindications_percentage'] * 0.15 +
            pattern_analysis['adverse_effects_percentage'] * 0.15 +
            pattern_analysis['pharmacology_percentage'] * 0.1 +
            pattern_analysis['species_specific_percentage'] * 0.15
        )
        
        drug_quality_score = min(drug_completeness['average_completeness'], 100)
        
        integrity_score = (
            integrity_analysis['chunks_with_complete_sentences_percentage'] * 0.2 +
            integrity_analysis['chunks_with_medical_terminology_percentage'] * 0.3 +
            integrity_analysis['chunks_with_dosage_units_percentage'] * 0.2 +
            integrity_analysis['chunks_with_species_mentions_percentage'] * 0.15 +
            integrity_analysis['high_quality_chunks_percentage'] * 0.15
        )
        
        overall_score = (content_coverage_score * 0.4 + drug_quality_score * 0.3 + integrity_score * 0.3)
        
        # Determine grade
        if overall_score >= 85:
            grade = "EXCELLENT"
            production_ready = True
        elif overall_score >= 75:
            grade = "GOOD"
            production_ready = True
        elif overall_score >= 65:
            grade = "FAIR"
            production_ready = False
        else:
            grade = "POOR"
            production_ready = False
        
        # Identify strengths and issues
        strengths = []
        issues = []
        
        if pattern_analysis['drug_sections_percentage'] > 30:
            strengths.append("Strong drug content coverage")
        if pattern_analysis['dosing_information_percentage'] > 25:
            strengths.append("Comprehensive dosing information")
        if drug_completeness['average_completeness'] > 70:
            strengths.append("Complete drug profiles")
        if integrity_analysis['high_quality_chunks_percentage'] > 70:
            strengths.append("High content quality")
        
        if pattern_analysis['contraindications_percentage'] < 10:
            issues.append("Limited contraindication coverage")
        if pattern_analysis['adverse_effects_percentage'] < 15:
            issues.append("Insufficient adverse effect information")
        if len(integrity_analysis['suspicious_chunks']) > 100:
            issues.append("Content quality concerns detected")
        
        final_report = {
            'validation_timestamp': str(datetime.now()),
            'overall_grade': grade,
            'overall_score': round(overall_score, 1),
            'production_ready': production_ready,
            'component_scores': {
                'content_coverage': round(content_coverage_score, 1),
                'drug_quality': round(drug_quality_score, 1),
                'content_integrity': round(integrity_score, 1)
            },
            'key_strengths': strengths,
            'identified_issues': issues,
            'detailed_analysis': {
                'pattern_analysis': pattern_analysis,
                'drug_completeness': drug_completeness,
                'integrity_analysis': integrity_analysis
            },
            'recommendations': self._generate_recommendations(overall_score, strengths, issues)
        }
        
        return final_report
    
    def _generate_recommendations(self, score: float, strengths: List[str], issues: List[str]) -> List[str]:
        """Generate recommendations based on analysis"""
        
        recommendations = []
        
        if score >= 85:
            recommendations.append("Database quality is excellent - ready for critical veterinary use")
            recommendations.append("Consider periodic validation to maintain quality standards")
        elif score >= 75:
            recommendations.append("Database quality is good - suitable for production with minor improvements")
        else:
            recommendations.append("Database needs improvement before production deployment")
        
        if "Limited contraindication coverage" in issues:
            recommendations.append("Enhance extraction of contraindication information")
        
        if "Insufficient adverse effect information" in issues:
            recommendations.append("Improve adverse effect detection and extraction")
        
        if "Content quality concerns detected" in issues:
            recommendations.append("Review and improve chunking strategy to reduce fragmented content")
        
        if not strengths:
            recommendations.append("Comprehensive review of extraction methodology required")
        
        return recommendations
    
    def run_comprehensive_validation(self) -> Dict[str, Any]:
        """Run comprehensive content validation"""
        
        if not self.chunks:
            return {'error': 'No chunks available for validation'}
        
        print(f"\n🚀 RUNNING COMPREHENSIVE CONTENT VALIDATION")
        print("=" * 70)
        
        try:
            # Step 1: Analyze content patterns
            print("\n1️⃣ CONTENT PATTERN ANALYSIS")
            pattern_analysis = self.analyze_content_patterns()
            
            # Step 2: Validate drug completeness
            print("\n2️⃣ DRUG COMPLETENESS VALIDATION")
            drug_completeness = self.validate_drug_completeness()
            
            # Step 3: Validate content integrity
            print("\n3️⃣ CONTENT INTEGRITY VALIDATION")
            integrity_analysis = self.validate_content_integrity()
            
            # Step 4: Generate final report
            print("\n4️⃣ FINAL REPORT GENERATION")
            final_report = self.generate_final_validation_report(
                pattern_analysis, drug_completeness, integrity_analysis
            )
            
            # Save results
            os.makedirs("audit_results", exist_ok=True)
            with open("audit_results/content_validation_report.json", 'w') as f:
                json.dump(final_report, f, indent=2, ensure_ascii=False)
            
            print(f"\n🎯 COMPREHENSIVE VALIDATION COMPLETE!")
            print(f"   Overall Grade: {final_report['overall_grade']}")
            print(f"   Overall Score: {final_report['overall_score']}/100")
            print(f"   Production Ready: {'✅ YES' if final_report['production_ready'] else '❌ NO'}")
            print(f"   Report saved: audit_results/content_validation_report.json")
            
            return final_report
            
        except Exception as e:
            print(f"❌ Validation failed: {str(e)}")
            return {'error': str(e)}

def main():
    """Execute comprehensive content validation"""
    
    auditor = ContentValidationAuditor()
    results = auditor.run_comprehensive_validation()
    
    if 'error' not in results:
        print(f"\n🏆 FINAL VALIDATION SUMMARY:")
        print("=" * 70)
        print(f"Overall Grade: {results['overall_grade']}")
        print(f"Overall Score: {results['overall_score']}/100")
        
        if results['key_strengths']:
            print(f"\n✅ Key Strengths:")
            for strength in results['key_strengths']:
                print(f"   • {strength}")
        
        if results['identified_issues']:
            print(f"\n⚠️ Identified Issues:")
            for issue in results['identified_issues']:
                print(f"   • {issue}")
        
        if results['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in results['recommendations']:
                print(f"   • {rec}")

if __name__ == "__main__":
    main()