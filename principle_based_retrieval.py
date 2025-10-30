#!/usr/bin/env python3
"""
Principle-Based Knowledge Retrieval System
Uses Claude's reasoning to identify veterinary principles and expand search terms
while maintaining complete grounding in the knowledge base
"""

import sys
sys.path.append('.')
sys.path.append('comprehensive_veterinary_drugs_database/production_code')

import json
import re
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
import logging
from anthropic import Anthropic
import os

@dataclass
class VeterinaryPrinciple:
    category: str  # pathophysiology, pharmacology, anatomy, diagnosis, etc.
    principle: str
    related_terms: List[str]
    search_expansion: List[str]

@dataclass
class PrincipleSearchResult:
    original_query: str
    identified_principles: List[VeterinaryPrinciple]
    expanded_search_terms: List[str]
    reasoning_chain: List[str]

class PrincipleBasedRetrieval:
    """
    Enhanced knowledge retrieval using veterinary principle recognition
    """
    
    def __init__(self):
        """Initialize the principle-based retrieval system"""
        self.logger = logging.getLogger(__name__)
        
        # Initialize Anthropic client
        try:
            self.anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        except Exception as e:
            self.logger.warning(f"Could not initialize Anthropic client: {e}")
            self.anthropic_client = None
        
        # Core veterinary principle database
        self.principle_database = self._initialize_principle_database()
        
        print("🧠 Principle-Based Retrieval System initialized")
        print(f"📚 Veterinary principles loaded: {len(self.principle_database)}")

    def _initialize_principle_database(self) -> Dict[str, List[VeterinaryPrinciple]]:
        """
        Initialize database of core veterinary principles for search expansion
        """
        principles = {
            "pharmacology": [
                VeterinaryPrinciple(
                    category="pharmacology",
                    principle="hepatic_metabolism",
                    related_terms=["liver", "hepatic", "metabolism", "clearance"],
                    search_expansion=["CYP450", "first-pass metabolism", "hepatic clearance", "liver enzymes", "metabolic pathways"]
                ),
                VeterinaryPrinciple(
                    category="pharmacology", 
                    principle="drug_interactions",
                    related_terms=["interaction", "combination", "concurrent"],
                    search_expansion=["enzyme induction", "enzyme inhibition", "competitive inhibition", "pharmacokinetic interaction", "pharmacodynamic interaction"]
                ),
                VeterinaryPrinciple(
                    category="pharmacology",
                    principle="renal_elimination",
                    related_terms=["kidney", "renal", "elimination", "excretion"],
                    search_expansion=["glomerular filtration", "tubular secretion", "renal clearance", "nephrotoxicity"]
                ),
                VeterinaryPrinciple(
                    category="pharmacology",
                    principle="protein_binding",
                    related_terms=["albumin", "protein", "binding", "displacement"],
                    search_expansion=["plasma protein binding", "free drug concentration", "hypoalbuminemia", "drug displacement"]
                )
            ],
            "pathophysiology": [
                VeterinaryPrinciple(
                    category="pathophysiology",
                    principle="inflammatory_response",
                    related_terms=["inflammation", "inflammatory", "immune"],
                    search_expansion=["cytokines", "prostaglandins", "complement cascade", "acute phase response", "leukocyte activation"]
                ),
                VeterinaryPrinciple(
                    category="pathophysiology",
                    principle="cardiovascular_regulation",
                    related_terms=["heart", "cardiac", "circulation", "blood pressure"],
                    search_expansion=["preload", "afterload", "contractility", "cardiac output", "peripheral resistance"]
                ),
                VeterinaryPrinciple(
                    category="pathophysiology",
                    principle="respiratory_physiology",
                    related_terms=["lung", "respiratory", "breathing", "oxygen"],
                    search_expansion=["gas exchange", "ventilation-perfusion", "oxygen transport", "respiratory mechanics"]
                )
            ],
            "diagnosis": [
                VeterinaryPrinciple(
                    category="diagnosis",
                    principle="differential_diagnosis",
                    related_terms=["diagnosis", "differential", "rule out"],
                    search_expansion=["clinical signs", "diagnostic tests", "disease progression", "ruling out conditions"]
                ),
                VeterinaryPrinciple(
                    category="diagnosis", 
                    principle="laboratory_interpretation",
                    related_terms=["lab", "laboratory", "blood", "chemistry"],
                    search_expansion=["reference ranges", "sensitivity", "specificity", "predictive value", "test accuracy"]
                )
            ],
            "anatomy": [
                VeterinaryPrinciple(
                    category="anatomy",
                    principle="species_differences",
                    related_terms=["canine", "feline", "equine", "bovine"],
                    search_expansion=["anatomical variations", "physiological differences", "species-specific", "comparative anatomy"]
                )
            ]
        }
        
        return principles

    def analyze_query_principles(self, query: str) -> PrincipleSearchResult:
        """
        Analyze query to identify underlying veterinary principles using Claude's reasoning
        """
        self.logger.info(f"🧠 Analyzing veterinary principles in query: {query[:100]}...")
        
        # First, identify principles using local database
        local_principles = self._identify_local_principles(query)
        
        # Then enhance with Claude's reasoning if available
        if self.anthropic_client:
            claude_analysis = self._get_claude_principle_analysis(query, local_principles)
            enhanced_principles = self._merge_principle_analyses(local_principles, claude_analysis)
        else:
            enhanced_principles = local_principles
        
        # Generate expanded search terms
        expanded_terms = self._generate_expanded_search_terms(query, enhanced_principles)
        
        # Build reasoning chain
        reasoning_chain = self._build_reasoning_chain(query, enhanced_principles)
        
        return PrincipleSearchResult(
            original_query=query,
            identified_principles=enhanced_principles,
            expanded_search_terms=expanded_terms,
            reasoning_chain=reasoning_chain
        )

    def _identify_local_principles(self, query: str) -> List[VeterinaryPrinciple]:
        """
        Identify veterinary principles using local pattern matching
        """
        identified = []
        query_lower = query.lower()
        
        for category, principles in self.principle_database.items():
            for principle in principles:
                # Check if any related terms appear in query
                if any(term in query_lower for term in principle.related_terms):
                    identified.append(principle)
        
        return identified

    def _get_claude_principle_analysis(self, query: str, local_principles: List[VeterinaryPrinciple]) -> Dict:
        """
        Get Claude's analysis of veterinary principles in the query
        """
        try:
            local_principle_names = [p.principle for p in local_principles]
            
            prompt = f"""You are a veterinary medical expert analyzing a clinical query to identify underlying veterinary principles that should guide knowledge retrieval from a veterinary textbook database.

Query: "{query}"

Already identified principles: {local_principle_names}

Your task: Identify additional veterinary principles, concepts, and related search terms that are relevant to this query but might not be explicitly mentioned. Think about:

1. **Pharmacological principles** (if drugs mentioned): metabolism pathways, drug interactions, pharmacokinetics
2. **Pathophysiological principles** (if diseases mentioned): underlying mechanisms, cascade effects
3. **Anatomical principles** (if procedures/locations mentioned): anatomical relationships, species differences
4. **Diagnostic principles** (if symptoms mentioned): differential diagnosis, test interpretation

Respond in JSON format:
{{
    "additional_principles": [
        {{
            "category": "pharmacology|pathophysiology|anatomy|diagnosis",
            "principle": "principle_name",
            "reasoning": "why this principle is relevant",
            "search_terms": ["term1", "term2", "term3"]
        }}
    ],
    "clinical_reasoning": "Brief explanation of the clinical reasoning chain"
}}

Focus on principles that would help retrieve relevant information from veterinary textbooks. Do not add external medical knowledge - only suggest what concepts to search for."""

            response = self.anthropic_client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=1000,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return json.loads(response.content[0].text)
            
        except Exception as e:
            self.logger.warning(f"Claude principle analysis failed: {e}")
            return {"additional_principles": [], "clinical_reasoning": ""}

    def _merge_principle_analyses(self, local_principles: List[VeterinaryPrinciple], claude_analysis: Dict) -> List[VeterinaryPrinciple]:
        """
        Merge local and Claude principle analyses
        """
        merged = local_principles.copy()
        
        for claude_principle in claude_analysis.get("additional_principles", []):
            # Convert Claude's principle to our format
            principle = VeterinaryPrinciple(
                category=claude_principle.get("category", "general"),
                principle=claude_principle.get("principle", ""),
                related_terms=claude_principle.get("search_terms", [])[:3],  # Take first 3
                search_expansion=claude_principle.get("search_terms", [])
            )
            
            # Avoid duplicates
            if not any(p.principle == principle.principle for p in merged):
                merged.append(principle)
        
        return merged

    def _generate_expanded_search_terms(self, original_query: str, principles: List[VeterinaryPrinciple]) -> List[str]:
        """
        Generate expanded search terms based on identified principles
        """
        expanded_terms = []
        
        # Start with original query terms
        query_terms = self._extract_key_terms(original_query)
        expanded_terms.extend(query_terms)
        
        # Add principle-based expansions
        for principle in principles:
            expanded_terms.extend(principle.related_terms)
            expanded_terms.extend(principle.search_expansion)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_terms = []
        for term in expanded_terms:
            if term.lower() not in seen:
                seen.add(term.lower())
                unique_terms.append(term)
        
        return unique_terms[:15]  # Limit to top 15 terms

    def _extract_key_terms(self, query: str) -> List[str]:
        """
        Extract key medical terms from query
        """
        # Remove common words
        stopwords = {"a", "an", "the", "is", "are", "was", "were", "has", "have", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "can", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        
        # Split and filter
        words = re.findall(r'\b[a-zA-Z]+\b', query.lower())
        key_terms = [word for word in words if word not in stopwords and len(word) > 2]
        
        return key_terms[:8]  # Top 8 terms

    def _build_reasoning_chain(self, query: str, principles: List[VeterinaryPrinciple]) -> List[str]:
        """
        Build a logical reasoning chain for the search strategy
        """
        chain = []
        
        chain.append(f"Original query focuses on: {self._extract_key_terms(query)}")
        
        if principles:
            chain.append("Identified underlying veterinary principles:")
            for principle in principles:
                chain.append(f"  • {principle.category}: {principle.principle}")
        
        chain.append("Search expansion strategy:")
        chain.append("  • Direct terms from query")
        chain.append("  • Related veterinary concepts")
        chain.append("  • Underlying pathophysiological mechanisms")
        chain.append("  • Species-specific considerations")
        
        return chain

    def generate_enhanced_search_queries(self, principle_result: PrincipleSearchResult) -> List[str]:
        """
        Generate multiple enhanced search queries based on principle analysis
        """
        queries = []
        
        # Original query
        queries.append(principle_result.original_query)
        
        # Principle-focused queries
        for principle in principle_result.identified_principles:
            # Combine original key terms with principle terms
            key_terms = self._extract_key_terms(principle_result.original_query)[:3]
            principle_terms = principle.related_terms[:2]
            
            combined_query = " ".join(key_terms + principle_terms)
            queries.append(combined_query)
        
        # Mechanism-focused queries
        mechanism_terms = []
        for principle in principle_result.identified_principles:
            mechanism_terms.extend(principle.search_expansion[:2])
        
        if mechanism_terms:
            original_key = self._extract_key_terms(principle_result.original_query)[:2]
            mechanism_query = " ".join(original_key + mechanism_terms[:3])
            queries.append(mechanism_query)
        
        # Remove duplicates
        unique_queries = []
        for query in queries:
            if query not in unique_queries:
                unique_queries.append(query)
        
        return unique_queries[:5]  # Limit to 5 queries

def main():
    """Test the principle-based retrieval system"""
    retrieval_system = PrincipleBasedRetrieval()
    
    print("\n🧪 TESTING PRINCIPLE-BASED RETRIEVAL SYSTEM")
    print("=" * 70)
    
    test_queries = [
        "What are the drug interactions between phenobarbital and clavamox in dogs with liver disease?",
        "How should I calculate morphine dosing for a cat with kidney disease?",
        "What causes elevated liver enzymes in seizure patients on long-term anticonvulsants?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📋 TEST CASE {i}")
        print("-" * 50)
        print(f"Query: {query}")
        
        # Analyze principles
        principle_result = retrieval_system.analyze_query_principles(query)
        
        print(f"\n🧠 Identified Principles:")
        for principle in principle_result.identified_principles:
            print(f"   • {principle.category}: {principle.principle}")
        
        print(f"\n🔍 Expanded Search Terms:")
        print(f"   {', '.join(principle_result.expanded_search_terms)}")
        
        print(f"\n🤔 Reasoning Chain:")
        for step in principle_result.reasoning_chain:
            print(f"   {step}")
        
        # Generate enhanced queries
        enhanced_queries = retrieval_system.generate_enhanced_search_queries(principle_result)
        print(f"\n📚 Enhanced Search Queries:")
        for j, enhanced_query in enumerate(enhanced_queries, 1):
            print(f"   {j}. {enhanced_query}")

if __name__ == "__main__":
    main()