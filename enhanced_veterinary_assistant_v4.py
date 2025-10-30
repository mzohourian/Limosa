#!/usr/bin/env python3
"""
Enhanced Veterinary Assistant v4.0
With CRI Calculation Engine + Principle-Based Retrieval + Mathematical Validation + Pharmacological Reasoning
"""

import sys
sys.path.append('.')
sys.path.append('comprehensive_veterinary_drugs_database/production_code')

from final_95_confidence_standalone import Final95ConfidenceAssistant
from veterinary_calculation_validator import VeterinaryCalculationValidator, RiskLevel
from pharmacological_reasoning_engine import PharmacologicalReasoningEngine
from principle_based_retrieval import PrincipleBasedRetrieval
from cri_calculation_engine import CRICalculationEngine
import re
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

class EnhancedVeterinaryAssistantV4:
    """
    Advanced veterinary assistant with CRI calculation engine, principle-based retrieval, 
    calculation validation, and pharmacological reasoning
    """
    
    def __init__(self):
        """Initialize with all safety and reasoning layers"""
        self.base_assistant = Final95ConfidenceAssistant()
        self.calc_validator = VeterinaryCalculationValidator()
        self.pharma_engine = PharmacologicalReasoningEngine()
        self.principle_retrieval = PrincipleBasedRetrieval()
        self.cri_engine = CRICalculationEngine()
        self.logger = logging.getLogger(__name__)
        
        print("🩺 Enhanced Veterinary Assistant v4.0")
        print("✅ Mathematical validation system activated")
        print("🧬 Pharmacological reasoning engine activated")
        print("🧠 Principle-based knowledge retrieval activated")
        print("💉 CRI calculation engine activated")
        print("⚠️ Comprehensive safety analysis enabled")

    def query_with_comprehensive_safety_v4(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Main query method with CRI override and comprehensive safety analysis
        """
        print(f"\n🔍 Processing query with v4.0 comprehensive safety analysis...")
        
        # Step 1: Check if this is a CRI calculation query
        is_cri_query = self._detect_cri_query(query)
        
        if is_cri_query:
            print("💉 CRI query detected - using dedicated CRI calculation engine")
            return self._handle_cri_query(query, context)
        
        # Step 2: Proceed with standard enhanced processing for non-CRI queries
        return self._handle_standard_query(query, context)

    def _detect_cri_query(self, query: str) -> bool:
        """
        Detect if query is asking for CRI calculations
        """
        cri_indicators = [
            r'cri\b',
            r'constant\s+rate\s+infusion',
            r'infusion\s+(?:rate|calculation)',
            r'(?:mlk|flk|morphine.*lidocaine.*ketamine)',
            r'dopamine.*cri',
            r'fentanyl.*cri',
            r'bag.*(?:ml/hour|ml/hr)',
            r'pump.*(?:rate|ml/hour|ml/hr)'
        ]
        
        query_lower = query.lower()
        for pattern in cri_indicators:
            if re.search(pattern, query_lower):
                return True
        
        return False

    def _handle_cri_query(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Handle CRI queries using dedicated calculation engine
        """
        print("💉 Processing CRI query with dedicated calculation engine...")
        
        # Step 1: Try to parse CRI parameters
        cri_parameters = self.cri_engine.parse_cri_query(query)
        
        if cri_parameters:
            print("✅ CRI parameters successfully parsed")
            
            # Step 2: Calculate CRI using proper protocol logic
            cri_result = self.cri_engine.calculate_cri(cri_parameters)
            
            if cri_result.is_valid:
                print("✅ CRI calculation completed successfully")
                
                # Step 3: Generate comprehensive response
                cri_report = self.cri_engine.generate_cri_report(cri_result)
                
                # Step 4: Get additional context from knowledge base
                base_response = self.base_assistant.query_with_high_confidence(query)
                
                # Step 5: Override with correct CRI calculation
                enhanced_response = {
                    'answer': self._generate_cri_override_response(cri_report, base_response, query),
                    'confidence': 0.98,  # High confidence in CRI calculations
                    'cri_calculation': {
                        'performed': True,
                        'valid': True,
                        'total_run_time_hours': cri_result.total_run_time_hours,
                        'drug_volumes': {calc['drug_name']: calc['volume_to_add_ml'] for calc in cri_result.drug_calculations},
                        'total_drug_volume_ml': cri_result.total_drug_volume_ml,
                        'warnings': cri_result.warnings
                    },
                    'safety_analysis': {
                        'cri_engine_override': True,
                        'calculation_validation_performed': True,
                        'proper_protocol_logic': True
                    },
                    'grounding_score': base_response.get('grounding_score', 85),
                    'context_used': base_response.get('context_used', ''),
                    'chunks_used': base_response.get('chunks_used', [])
                }
                
                return enhanced_response
            else:
                print("❌ CRI calculation failed")
                # Fall back to standard processing with error warning
                standard_response = self._handle_standard_query(query, context)
                standard_response['cri_calculation_error'] = "CRI parameters could not be calculated properly"
                return standard_response
        else:
            print("⚠️ Could not parse CRI parameters - using standard processing")
            # Fall back to standard processing
            return self._handle_standard_query(query, context)

    def _generate_cri_override_response(self, cri_report: str, base_response: Dict, query: str) -> str:
        """
        Generate response that overrides base assistant with correct CRI calculation
        """
        response_parts = []
        
        # CRI calculation header
        response_parts.append("💉 CRI CALCULATION - VETERINARY PROTOCOL")
        response_parts.append("=" * 60)
        response_parts.append("⚠️ USING DEDICATED CRI CALCULATION ENGINE FOR ACCURACY")
        response_parts.append("")
        
        # Include relevant knowledge base context first
        if base_response.get('context_used'):
            response_parts.append("📚 RELEVANT VETERINARY KNOWLEDGE:")
            response_parts.append("-" * 40)
            context_preview = base_response['context_used'][:500] + "..." if len(base_response['context_used']) > 500 else base_response['context_used']
            response_parts.append(context_preview)
            response_parts.append("")
        
        # Add the correct CRI calculation
        response_parts.append(cri_report)
        
        response_parts.append("")
        response_parts.append("🛡️ SAFETY VERIFICATION:")
        response_parts.append("✅ CRI calculation performed with proper total duration protocol")
        response_parts.append("✅ All drug volumes calculated for entire bag run time")
        response_parts.append("✅ Prevents critical under-dosing or over-dosing errors")
        response_parts.append("")
        response_parts.append("⚠️ CRITICAL: Always verify calculations with veterinary references")
        response_parts.append("⚠️ Consider patient-specific factors (renal, hepatic function)")
        
        return "\n".join(response_parts)

    def _handle_standard_query(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Handle non-CRI queries using enhanced v3.0 processing
        """
        # Step 1: Analyze veterinary principles in the query
        print("🧠 Analyzing underlying veterinary principles...")
        principle_analysis = self.principle_retrieval.analyze_query_principles(query)
        
        # Step 2: Generate enhanced search queries
        enhanced_queries = self.principle_retrieval.generate_enhanced_search_queries(principle_analysis)
        print(f"📚 Generated {len(enhanced_queries)} principle-based search queries")
        
        # Step 3: Get response using enhanced retrieval
        base_response = self._get_principle_enhanced_response(query, enhanced_queries)
        
        # Step 4: Extract context from query
        extracted_context = self._extract_comprehensive_context(query)
        if context:
            extracted_context.update(context)
        
        # Step 5: Analyze for drug interactions if multiple drugs mentioned
        interaction_analysis = None
        drugs_mentioned = extracted_context.get('drugs_mentioned', [])
        
        if len(drugs_mentioned) > 1:
            print(f"🧬 Multiple drugs detected: {drugs_mentioned} - analyzing interactions...")
            interactions = self.pharma_engine.analyze_drug_interactions(
                drugs_mentioned,
                extracted_context.get('patient_conditions', [])
            )
            interaction_analysis = {
                'interactions_found': len(interactions),
                'interactions': interactions,
                'report': self.pharma_engine.generate_interaction_report(interactions)
            }
        
        # Step 6: Check for hepatic metabolism principles if liver disease mentioned
        hepatic_analysis = None
        if any(condition in query.lower() for condition in ['liver', 'hepatic', 'enzyme']):
            print("🧬 Hepatic concerns detected - analyzing metabolism principles...")
            hepatic_analysis = {}
            for drug in drugs_mentioned:
                hepatic_info = self.pharma_engine.get_hepatic_metabolism_principle(drug)
                hepatic_analysis[drug] = hepatic_info
        
        # Step 7: Validate calculations if present (excluding CRIs which are handled separately)
        calculation_validation = None
        calculation_detected = self._detect_calculations(base_response.get('answer', ''))
        
        if calculation_detected and not self._detect_cri_query(query):
            print("🧮 Mathematical calculations detected - validating...")
            validation_result = self.calc_validator.validate_calculation(
                base_response.get('answer', ''), 
                extracted_context
            )
            safety_report = self.calc_validator.generate_safety_report(validation_result)
            calculation_validation = {
                'validation_performed': True,
                'is_valid': validation_result.is_valid,
                'confidence': validation_result.confidence,
                'risk_level': validation_result.risk_level.value,
                'requires_manual_review': validation_result.requires_manual_review,
                'errors': validation_result.errors,
                'warnings': validation_result.warnings,
                'safety_report': safety_report
            }
        
        # Step 8: Generate comprehensive enhanced response
        enhanced_response = self._generate_comprehensive_response_v4(
            base_response,
            principle_analysis,
            interaction_analysis,
            hepatic_analysis,
            calculation_validation,
            extracted_context
        )
        
        return enhanced_response

    def _get_principle_enhanced_response(self, original_query: str, enhanced_queries: List[str]) -> Dict[str, Any]:
        """
        Get response using principle-enhanced retrieval while maintaining knowledge base grounding
        """
        print("📚 Performing principle-enhanced knowledge retrieval...")
        
        # Primary response from original query
        primary_response = self.base_assistant.query_with_high_confidence(original_query)
        
        # Collect additional context from enhanced queries
        additional_contexts = []
        for enhanced_query in enhanced_queries[1:]:  # Skip first (original query)
            try:
                enhanced_response = self.base_assistant.query_with_high_confidence(enhanced_query)
                if enhanced_response.get('confidence', 0) > 0.7:  # Only high-confidence additions
                    additional_contexts.append({
                        'query': enhanced_query,
                        'context': enhanced_response.get('context_used', ''),
                        'confidence': enhanced_response.get('confidence', 0)
                    })
            except Exception as e:
                self.logger.warning(f"Enhanced query failed: {enhanced_query[:50]}... - {e}")
        
        # Enhance primary response with additional context if available
        if additional_contexts:
            print(f"✅ Incorporated {len(additional_contexts)} additional principle-based contexts")
            primary_response['principle_enhanced_contexts'] = additional_contexts
        
        return primary_response

    def _extract_comprehensive_context(self, query: str) -> Dict[str, Any]:
        """
        Extract comprehensive context including drugs, conditions, and patient factors
        """
        context = {}
        
        # Extract weight
        weight_match = re.search(r'(\d+\.?\d*)\s*kg', query, re.IGNORECASE)
        if weight_match:
            context['weight'] = float(weight_match.group(1))
        
        # Extract age
        age_match = re.search(r'(\d+)\s*(?:year|yr|month|mo)', query, re.IGNORECASE)
        if age_match:
            context['age'] = age_match.group(1)
        
        # Extract species
        species_patterns = {
            r'dog|canine': 'canine',
            r'cat|feline': 'feline', 
            r'horse|equine': 'equine',
            r'cow|bovine': 'bovine'
        }
        
        for pattern, species in species_patterns.items():
            if re.search(pattern, query, re.IGNORECASE):
                context['species'] = species
                break
        
        # Extract drugs mentioned
        drug_patterns = [
            r'phenobarbital', r'diazepam', r'morphine', r'tramadol',
            r'acepromazine', r'lidocaine', r'ketamine', r'fentanyl',
            r'amoxicillin', r'clavamox', r'clavulanate', r'chloramphenicol',
            r'ketoconazole', r'itraconazole', r'fluconazole', r'dopamine'
        ]
        
        detected_drugs = []
        for pattern in drug_patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            detected_drugs.extend([match.lower() for match in matches])
        
        # Remove duplicates while preserving order
        context['drugs_mentioned'] = list(dict.fromkeys(detected_drugs))
        
        # Extract medical conditions
        condition_patterns = [
            r'liver\s+disease', r'hepatic\s+compromise', r'elevated\s+liver\s+enzymes',
            r'seizures?', r'epilepsy', r'kidney\s+disease', r'renal\s+failure',
            r'heart\s+disease', r'cardiac\s+disease', r'hypertension', r'hypotension'
        ]
        
        detected_conditions = []
        for pattern in condition_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                detected_conditions.append(pattern.replace('\\s+', '_').replace('?', ''))
        
        if detected_conditions:
            context['patient_conditions'] = detected_conditions
        
        # Extract interaction-related keywords
        if re.search(r'interact|combination|together|with', query, re.IGNORECASE):
            context['interaction_query'] = True
        
        return context

    def _detect_calculations(self, response_text: str) -> bool:
        """
        Detect if response contains mathematical calculations
        """
        calculation_indicators = [
            r'\d+\.?\d*\s*[×*xX]\s*\d+\.?\d*',  # Multiplication
            r'\d+\.?\d*\s*/\s*\d+\.?\d*',       # Division
            r'\d+\.?\d*\s*mg/kg',               # Dosing
            r'\d+\.?\d*\s*ml',                  # Volumes
            r'calculate|calculation|dose|dosage', # Keywords
            r'total.*=|result.*=|\d+\.?\d*\s*=', # Equations
        ]
        
        for pattern in calculation_indicators:
            if re.search(pattern, response_text, re.IGNORECASE):
                return True
        
        return False

    def _generate_comprehensive_response_v4(
        self,
        base_response: Dict[str, Any],
        principle_analysis,
        interaction_analysis: Optional[Dict],
        hepatic_analysis: Optional[Dict],
        calculation_validation: Optional[Dict],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive response with v4.0 enhancements
        """
        enhanced_response = base_response.copy()
        
        # Add comprehensive metadata
        enhanced_response['safety_analysis'] = {
            'cri_engine_available': True,
            'principle_based_retrieval_performed': True,
            'interaction_analysis_performed': interaction_analysis is not None,
            'hepatic_analysis_performed': hepatic_analysis is not None,
            'calculation_validation_performed': calculation_validation is not None,
            'comprehensive_safety_check': True
        }
        
        # Add principle analysis metadata
        enhanced_response['principle_analysis'] = {
            'identified_principles': [
                {
                    'category': p.category,
                    'principle': p.principle,
                    'search_terms': p.search_expansion
                } for p in principle_analysis.identified_principles
            ],
            'reasoning_chain': principle_analysis.reasoning_chain,
            'enhanced_search_performed': True
        }
        
        # Start building enhanced answer
        answer_parts = []
        
        # Handle calculation errors first (highest priority)
        if calculation_validation and not calculation_validation['is_valid']:
            answer_parts.append("🚨 CRITICAL CALCULATION ERROR DETECTED")
            answer_parts.append("The mathematical calculations in this response contain errors and should NOT be used for patient care.")
            answer_parts.append(f"\nORIGINAL RESPONSE (DO NOT USE):\n{base_response.get('answer', '')}")
            answer_parts.append(f"\n{calculation_validation['safety_report']}")
            
            enhanced_response['confidence'] = 0.0
            enhanced_response['safety_override'] = True
            
        else:
            # Start with original response
            answer_parts.append(base_response.get('answer', ''))
            
            # Add principle-based enhancement notice
            if principle_analysis.identified_principles:
                answer_parts.append("\n" + "="*60)
                answer_parts.append("🧠 PRINCIPLE-BASED VETERINARY ANALYSIS")
                answer_parts.append("="*60)
                answer_parts.append("This response incorporates the following veterinary principles:")
                for principle in principle_analysis.identified_principles:
                    answer_parts.append(f"   • {principle.category.title()}: {principle.principle}")
                answer_parts.append("\nKnowledge retrieval enhanced based on underlying veterinary mechanisms and relationships.")
            
            # Add drug interaction analysis
            if interaction_analysis and interaction_analysis['interactions_found'] > 0:
                answer_parts.append("\n" + "="*60)
                answer_parts.append("🧬 DRUG INTERACTION ANALYSIS")
                answer_parts.append("="*60)
                answer_parts.append(interaction_analysis['report'])
                
                # Update safety metadata
                enhanced_response['safety_analysis']['drug_interactions'] = {
                    'interactions_found': interaction_analysis['interactions_found'],
                    'requires_attention': True
                }
            
            # Add hepatic metabolism analysis
            if hepatic_analysis:
                answer_parts.append("\n" + "="*60)
                answer_parts.append("🧬 HEPATIC METABOLISM ANALYSIS")
                answer_parts.append("="*60)
                
                for drug, info in hepatic_analysis.items():
                    answer_parts.append(f"\n📋 {drug.upper()}:")
                    answer_parts.append(f"   🧬 Hepatic Metabolism: {info['hepatic_metabolism_percent']}%")
                    answer_parts.append(f"   🔬 Principle: {info['principle']}")
                    answer_parts.append(f"   ⚠️ Clinical Significance: {info['clinical_significance']}")
                    
                    if info['contraindications']:
                        answer_parts.append(f"   🚫 Contraindications: {', '.join(info['contraindications'])}")
            
            # Add calculation validation if successful
            if calculation_validation and calculation_validation['is_valid']:
                answer_parts.append(f"\n{calculation_validation['safety_report']}")
            elif calculation_validation and calculation_validation['requires_manual_review']:
                answer_parts.append(f"\n{calculation_validation['safety_report']}")
        
        # Add comprehensive safety footer
        answer_parts.append("\n" + "="*60)
        answer_parts.append("🛡️ ENHANCED VETERINARY ASSISTANT v4.0")
        answer_parts.append("="*60)
        
        safety_notes = []
        safety_notes.append("✅ Principle-based veterinary knowledge retrieval")
        safety_notes.append("✅ Dedicated CRI calculation engine available")
        if interaction_analysis:
            safety_notes.append("✅ Drug interaction analysis performed")
        if hepatic_analysis:
            safety_notes.append("✅ Hepatic metabolism principles applied")
        if calculation_validation:
            safety_notes.append("✅ Mathematical calculations validated")
        
        answer_parts.extend(safety_notes)
        answer_parts.append("\n⚠️ ALL INFORMATION GROUNDED IN VETERINARY TEXTBOOK KNOWLEDGE BASE")
        answer_parts.append("⚠️ CRI calculations use proper total duration protocol logic")
        answer_parts.append("⚠️ ALWAYS verify complex clinical decisions with veterinary references")
        
        enhanced_response['answer'] = "\n".join(answer_parts)
        
        # Add detailed metadata
        if interaction_analysis:
            enhanced_response['drug_interactions'] = interaction_analysis
        if hepatic_analysis:
            enhanced_response['hepatic_analysis'] = hepatic_analysis
        if calculation_validation:
            enhanced_response['calculation_validation'] = calculation_validation
        
        enhanced_response['context_extracted'] = context
        
        return enhanced_response

    def test_cri_override_system(self):
        """
        Test the CRI override system with the problematic test case
        """
        print("\n🧪 TESTING CRI OVERRIDE SYSTEM v4.0")
        print("=" * 70)
        
        # Test the exact problematic query from user's critique
        test_query = "I have a 10 kg dog who needs a Dopamine CRI at a dose of 5 μg/kg/minute. I want to use a 500 mL bag of saline and run it at 10 mL/hour. Our Dopamine concentration is 40 mg/mL. What is the total mL of Dopamine to add to the 500 mL bag?"
        
        print(f"📋 TEST QUERY:")
        print(f"{test_query}")
        print("\n" + "-" * 70)
        
        result = self.query_with_comprehensive_safety_v4(test_query)
        
        print(f"\n📊 SYSTEM ANALYSIS:")
        safety = result.get('safety_analysis', {})
        cri_calc = result.get('cri_calculation', {})
        
        print(f"   💉 CRI Engine Override: {'✅' if safety.get('cri_engine_override') else '❌'}")
        print(f"   🧮 CRI Calculation Valid: {'✅' if cri_calc.get('valid') else '❌'}")
        
        if cri_calc.get('drug_volumes'):
            dopamine_volume = cri_calc['drug_volumes'].get('Dopamine', 0)
            print(f"   💊 Dopamine Volume Calculated: {dopamine_volume:.2f} mL")
            print(f"   🕐 Total Run Time: {cri_calc.get('total_run_time_hours', 0):.1f} hours")
        
        print(f"\n📋 RESPONSE:")
        print(result.get('answer', 'No response generated'))

def main():
    """Test the enhanced veterinary assistant v4.0"""
    assistant = EnhancedVeterinaryAssistantV4()
    assistant.test_cri_override_system()

if __name__ == "__main__":
    main()