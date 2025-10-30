#!/usr/bin/env python3
"""
Pharmacological Reasoning Engine
Addresses CYP450 interactions and mechanism-based drug reasoning
"""

import re
import json
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum
import logging

class InteractionType(Enum):
    CYP450_INDUCTION = "cyp450_induction"
    CYP450_INHIBITION = "cyp450_inhibition"
    HEPATIC_METABOLISM = "hepatic_metabolism"
    RENAL_ELIMINATION = "renal_elimination"
    PROTEIN_BINDING = "protein_binding"
    PHARMACODYNAMIC = "pharmacodynamic"
    CONTRAINDICATION = "contraindication"

class InteractionSeverity(Enum):
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    CONTRAINDICATED = "contraindicated"

@dataclass
class DrugMechanism:
    drug_name: str
    cyp450_effects: List[str]  # ['inducer', 'inhibitor', 'substrate']
    cyp450_enzymes: List[str]  # ['3A4', '2D6', '2C9', etc.]
    hepatic_metabolism_percent: Optional[float]
    renal_elimination_percent: Optional[float]
    protein_binding_percent: Optional[float]
    therapeutic_class: str
    contraindications: List[str]

@dataclass
class DrugInteraction:
    drug1: str
    drug2: str
    interaction_type: InteractionType
    severity: InteractionSeverity
    mechanism: str
    clinical_effect: str
    management: str
    confidence: float

class PharmacologicalReasoningEngine:
    """
    Advanced drug interaction detection based on pharmacological mechanisms
    """
    
    def __init__(self):
        """Initialize the pharmacological reasoning engine"""
        self.logger = logging.getLogger(__name__)
        
        # Initialize drug mechanism database
        self.drug_mechanisms = self._initialize_drug_mechanisms()
        
        # Initialize interaction rules
        self.interaction_rules = self._initialize_interaction_rules()
        
        print("🧬 Pharmacological Reasoning Engine initialized")
        print(f"📊 Drug mechanisms loaded: {len(self.drug_mechanisms)} (comprehensive veterinary database)")
        print(f"⚗️ Interaction rules loaded: {len(self.interaction_rules)} (mechanism-based detection)")
        print("   🎯 CYP450 enzyme interactions, protein binding displacement")
        print("   🎯 Therapeutic class conflicts, renal elimination competition")
        print("   🎯 Veterinary-specific interactions with high clinical relevance")

    def _initialize_drug_mechanisms(self) -> Dict[str, DrugMechanism]:
        """
        Initialize comprehensive drug mechanism database
        """
        mechanisms = {}
        
        # Veterinary CNS drugs
        mechanisms["phenobarbital"] = DrugMechanism(
            drug_name="phenobarbital",
            cyp450_effects=["inducer"],
            cyp450_enzymes=["3A4", "2C9", "2C19", "2B6"],
            hepatic_metabolism_percent=75.0,
            renal_elimination_percent=25.0,
            protein_binding_percent=50.0,
            therapeutic_class="anticonvulsant",
            contraindications=["severe_liver_disease", "porphyria"]
        )
        
        mechanisms["diazepam"] = DrugMechanism(
            drug_name="diazepam",
            cyp450_effects=["substrate"],
            cyp450_enzymes=["3A4", "2C19"],
            hepatic_metabolism_percent=95.0,
            renal_elimination_percent=5.0,
            protein_binding_percent=95.0,
            therapeutic_class="benzodiazepine",
            contraindications=["severe_liver_disease"]
        )
        
        # Antibiotics
        mechanisms["amoxicillin"] = DrugMechanism(
            drug_name="amoxicillin",
            cyp450_effects=["minimal"],
            cyp450_enzymes=[],
            hepatic_metabolism_percent=10.0,
            renal_elimination_percent=90.0,
            protein_binding_percent=20.0,
            therapeutic_class="beta_lactam_antibiotic",
            contraindications=["penicillin_allergy"]
        )
        
        mechanisms["clavulanate"] = DrugMechanism(
            drug_name="clavulanate",
            cyp450_effects=["minimal"],
            cyp450_enzymes=[],
            hepatic_metabolism_percent=30.0,
            renal_elimination_percent=70.0,
            protein_binding_percent=25.0,
            therapeutic_class="beta_lactamase_inhibitor",
            contraindications=["penicillin_allergy"]
        )
        
        mechanisms["chloramphenicol"] = DrugMechanism(
            drug_name="chloramphenicol",
            cyp450_effects=["inhibitor"],
            cyp450_enzymes=["3A4", "2C9"],
            hepatic_metabolism_percent=90.0,
            renal_elimination_percent=10.0,
            protein_binding_percent=60.0,
            therapeutic_class="antibiotic",
            contraindications=["bone_marrow_suppression"]
        )
        
        # Analgesics
        mechanisms["morphine"] = DrugMechanism(
            drug_name="morphine",
            cyp450_effects=["substrate"],
            cyp450_enzymes=["2D6"],
            hepatic_metabolism_percent=85.0,
            renal_elimination_percent=15.0,
            protein_binding_percent=35.0,
            therapeutic_class="opioid_analgesic",
            contraindications=["respiratory_depression"]
        )
        
        mechanisms["tramadol"] = DrugMechanism(
            drug_name="tramadol",
            cyp450_effects=["substrate"],
            cyp450_enzymes=["2D6", "3A4"],
            hepatic_metabolism_percent=90.0,
            renal_elimination_percent=10.0,
            protein_binding_percent=20.0,
            therapeutic_class="opioid_analgesic",
            contraindications=["seizure_disorder"]
        )
        
        # Sedatives
        mechanisms["acepromazine"] = DrugMechanism(
            drug_name="acepromazine",
            cyp450_effects=["substrate"],
            cyp450_enzymes=["3A4"],
            hepatic_metabolism_percent=95.0,
            renal_elimination_percent=5.0,
            protein_binding_percent=90.0,
            therapeutic_class="phenothiazine",
            contraindications=["hypotension", "seizure_disorder"]
        )
        
        # NSAIDs and Anti-inflammatories
        mechanisms["carprofen"] = DrugMechanism(
            drug_name="carprofen",
            cyp450_effects=["substrate"],
            cyp450_enzymes=["2C9"],
            hepatic_metabolism_percent=95.0,
            renal_elimination_percent=5.0,
            protein_binding_percent=99.0,
            therapeutic_class="nsaid",
            contraindications=["cats", "kidney_disease", "liver_disease", "bleeding_disorders"]
        )
        
        mechanisms["meloxicam"] = DrugMechanism(
            drug_name="meloxicam",
            cyp450_effects=["substrate"],
            cyp450_enzymes=["2C9"],
            hepatic_metabolism_percent=95.0,
            renal_elimination_percent=5.0,
            protein_binding_percent=99.0,
            therapeutic_class="nsaid",
            contraindications=["kidney_disease", "liver_disease", "dehydration"]
        )
        
        mechanisms["firocoxib"] = DrugMechanism(
            drug_name="firocoxib",
            cyp450_effects=["substrate"],
            cyp450_enzymes=["2C9", "3A4"],
            hepatic_metabolism_percent=90.0,
            renal_elimination_percent=10.0,
            protein_binding_percent=96.0,
            therapeutic_class="cox2_nsaid",
            contraindications=["kidney_disease", "liver_disease"]
        )
        
        mechanisms["gabapentin"] = DrugMechanism(
            drug_name="gabapentin",
            cyp450_effects=["minimal"],
            cyp450_enzymes=[],
            hepatic_metabolism_percent=0.0,
            renal_elimination_percent=100.0,
            protein_binding_percent=3.0,
            therapeutic_class="anticonvulsant_analgesic",
            contraindications=["severe_kidney_disease"]
        )
        
        mechanisms["pregabalin"] = DrugMechanism(
            drug_name="pregabalin",
            cyp450_effects=["minimal"],
            cyp450_enzymes=[],
            hepatic_metabolism_percent=0.0,
            renal_elimination_percent=100.0,
            protein_binding_percent=0.0,
            therapeutic_class="anticonvulsant_analgesic",
            contraindications=["severe_kidney_disease"]
        )
        
        # Anesthetics and Analgesics
        mechanisms["lidocaine"] = DrugMechanism(
            drug_name="lidocaine",
            cyp450_effects=["substrate"],
            cyp450_enzymes=["3A4", "1A2"],
            hepatic_metabolism_percent=95.0,
            renal_elimination_percent=5.0,
            protein_binding_percent=70.0,
            therapeutic_class="local_anesthetic",
            contraindications=["heart_block", "severe_liver_disease"]
        )
        
        mechanisms["bupivacaine"] = DrugMechanism(
            drug_name="bupivacaine",
            cyp450_effects=["substrate"],
            cyp450_enzymes=["3A4"],
            hepatic_metabolism_percent=95.0,
            renal_elimination_percent=5.0,
            protein_binding_percent=95.0,
            therapeutic_class="local_anesthetic",
            contraindications=["heart_block", "severe_liver_disease"]
        )
        
        mechanisms["ketamine"] = DrugMechanism(
            drug_name="ketamine",
            cyp450_effects=["substrate"],
            cyp450_enzymes=["3A4", "2B6"],
            hepatic_metabolism_percent=90.0,
            renal_elimination_percent=10.0,
            protein_binding_percent=12.0,
            therapeutic_class="nmda_antagonist",
            contraindications=["increased_intracranial_pressure"]
        )
        
        mechanisms["propofol"] = DrugMechanism(
            drug_name="propofol",
            cyp450_effects=["substrate"],
            cyp450_enzymes=["2B6", "2C9"],
            hepatic_metabolism_percent=88.0,
            renal_elimination_percent=2.0,
            protein_binding_percent=98.0,
            therapeutic_class="general_anesthetic",
            contraindications=["severe_cardiac_disease"]
        )
        
        mechanisms["fentanyl"] = DrugMechanism(
            drug_name="fentanyl",
            cyp450_effects=["substrate"],
            cyp450_enzymes=["3A4"],
            hepatic_metabolism_percent=95.0,
            renal_elimination_percent=5.0,
            protein_binding_percent=84.0,
            therapeutic_class="opioid_analgesic",
            contraindications=["respiratory_depression", "severe_liver_disease"]
        )
        
        mechanisms["buprenorphine"] = DrugMechanism(
            drug_name="buprenorphine",
            cyp450_effects=["substrate"],
            cyp450_enzymes=["3A4"],
            hepatic_metabolism_percent=95.0,
            renal_elimination_percent=5.0,
            protein_binding_percent=96.0,
            therapeutic_class="partial_opioid_agonist",
            contraindications=["severe_liver_disease"]
        )
        
        mechanisms["butorphanol"] = DrugMechanism(
            drug_name="butorphanol",
            cyp450_effects=["substrate"],
            cyp450_enzymes=["3A4"],
            hepatic_metabolism_percent=85.0,
            renal_elimination_percent=15.0,
            protein_binding_percent=80.0,
            therapeutic_class="opioid_analgesic",
            contraindications=["severe_liver_disease"]
        )
        
        # Antibiotics
        mechanisms["doxycycline"] = DrugMechanism(
            drug_name="doxycycline",
            cyp450_effects=["minimal"],
            cyp450_enzymes=[],
            hepatic_metabolism_percent=30.0,
            renal_elimination_percent=40.0,
            protein_binding_percent=90.0,
            therapeutic_class="tetracycline",
            contraindications=["pregnancy", "young_animals"]
        )
        
        mechanisms["enrofloxacin"] = DrugMechanism(
            drug_name="enrofloxacin",
            cyp450_effects=["inhibitor"],
            cyp450_enzymes=["1A2"],
            hepatic_metabolism_percent=70.0,
            renal_elimination_percent=30.0,
            protein_binding_percent=40.0,
            therapeutic_class="fluoroquinolone",
            contraindications=["cartilage_disorders", "young_animals"]
        )
        
        mechanisms["ciprofloxacin"] = DrugMechanism(
            drug_name="ciprofloxacin",
            cyp450_effects=["inhibitor"],
            cyp450_enzymes=["1A2"],
            hepatic_metabolism_percent=50.0,
            renal_elimination_percent=50.0,
            protein_binding_percent=40.0,
            therapeutic_class="fluoroquinolone",
            contraindications=["cartilage_disorders", "young_animals"]
        )
        
        mechanisms["cephalexin"] = DrugMechanism(
            drug_name="cephalexin",
            cyp450_effects=["minimal"],
            cyp450_enzymes=[],
            hepatic_metabolism_percent=10.0,
            renal_elimination_percent=90.0,
            protein_binding_percent=15.0,
            therapeutic_class="cephalosporin",
            contraindications=["penicillin_allergy"]
        )
        
        mechanisms["metronidazole"] = DrugMechanism(
            drug_name="metronidazole",
            cyp450_effects=["inhibitor"],
            cyp450_enzymes=["2C9"],
            hepatic_metabolism_percent=80.0,
            renal_elimination_percent=20.0,
            protein_binding_percent=10.0,
            therapeutic_class="nitroimidazole",
            contraindications=["severe_liver_disease", "neurological_disorders"]
        )
        
        mechanisms["azithromycin"] = DrugMechanism(
            drug_name="azithromycin",
            cyp450_effects=["mild_inhibitor"],
            cyp450_enzymes=["3A4"],
            hepatic_metabolism_percent=50.0,
            renal_elimination_percent=12.0,
            protein_binding_percent=50.0,
            therapeutic_class="macrolide",
            contraindications=["severe_liver_disease"]
        )
        
        # Cardiovascular drugs
        mechanisms["enalapril"] = DrugMechanism(
            drug_name="enalapril",
            cyp450_effects=["minimal"],
            cyp450_enzymes=[],
            hepatic_metabolism_percent=50.0,
            renal_elimination_percent=50.0,
            protein_binding_percent=50.0,
            therapeutic_class="ace_inhibitor",
            contraindications=["pregnancy", "bilateral_renal_artery_stenosis"]
        )
        
        mechanisms["pimobendan"] = DrugMechanism(
            drug_name="pimobendan",
            cyp450_effects=["substrate"],
            cyp450_enzymes=["3A4"],
            hepatic_metabolism_percent=85.0,
            renal_elimination_percent=15.0,
            protein_binding_percent=95.0,
            therapeutic_class="inodilator",
            contraindications=["hypertrophic_cardiomyopathy"]
        )
        
        mechanisms["furosemide"] = DrugMechanism(
            drug_name="furosemide",
            cyp450_effects=["minimal"],
            cyp450_enzymes=[],
            hepatic_metabolism_percent=10.0,
            renal_elimination_percent=90.0,
            protein_binding_percent=95.0,
            therapeutic_class="loop_diuretic",
            contraindications=["anuria", "severe_electrolyte_imbalance"]
        )
        
        mechanisms["diltiazem"] = DrugMechanism(
            drug_name="diltiazem",
            cyp450_effects=["inhibitor", "substrate"],
            cyp450_enzymes=["3A4"],
            hepatic_metabolism_percent=90.0,
            renal_elimination_percent=10.0,
            protein_binding_percent=80.0,
            therapeutic_class="calcium_channel_blocker",
            contraindications=["heart_block", "severe_hypotension"]
        )
        
        mechanisms["atenolol"] = DrugMechanism(
            drug_name="atenolol",
            cyp450_effects=["minimal"],
            cyp450_enzymes=[],
            hepatic_metabolism_percent=10.0,
            renal_elimination_percent=90.0,
            protein_binding_percent=5.0,
            therapeutic_class="beta_blocker",
            contraindications=["asthma", "severe_bradycardia"]
        )
        
        # Anticonvulsants
        mechanisms["levetiracetam"] = DrugMechanism(
            drug_name="levetiracetam",
            cyp450_effects=["minimal"],
            cyp450_enzymes=[],
            hepatic_metabolism_percent=24.0,
            renal_elimination_percent=66.0,
            protein_binding_percent=10.0,
            therapeutic_class="anticonvulsant",
            contraindications=["severe_kidney_disease"]
        )
        
        mechanisms["zonisamide"] = DrugMechanism(
            drug_name="zonisamide",
            cyp450_effects=["substrate"],
            cyp450_enzymes=["3A4"],
            hepatic_metabolism_percent=85.0,
            renal_elimination_percent=15.0,
            protein_binding_percent=40.0,
            therapeutic_class="anticonvulsant",
            contraindications=["sulfonamide_allergy"]
        )
        
        # Emergency/Critical Care drugs
        mechanisms["dopamine"] = DrugMechanism(
            drug_name="dopamine",
            cyp450_effects=["substrate"],
            cyp450_enzymes=["2D6"],
            hepatic_metabolism_percent=75.0,
            renal_elimination_percent=25.0,
            protein_binding_percent=0.0,
            therapeutic_class="catecholamine",
            contraindications=["pheochromocytoma", "ventricular_fibrillation"]
        )
        
        mechanisms["dobutamine"] = DrugMechanism(
            drug_name="dobutamine",
            cyp450_effects=["substrate"],
            cyp450_enzymes=["2D6"],
            hepatic_metabolism_percent=85.0,
            renal_elimination_percent=15.0,
            protein_binding_percent=0.0,
            therapeutic_class="catecholamine",
            contraindications=["hypertrophic_cardiomyopathy"]
        )
        
        mechanisms["epinephrine"] = DrugMechanism(
            drug_name="epinephrine",
            cyp450_effects=["substrate"],
            cyp450_enzymes=["2D6"],
            hepatic_metabolism_percent=90.0,
            renal_elimination_percent=10.0,
            protein_binding_percent=0.0,
            therapeutic_class="catecholamine",
            contraindications=["ventricular_fibrillation"]
        )
        
        # Antifungals (known CYP450 inhibitors)
        mechanisms["ketoconazole"] = DrugMechanism(
            drug_name="ketoconazole",
            cyp450_effects=["inhibitor"],
            cyp450_enzymes=["3A4"],
            hepatic_metabolism_percent=95.0,
            renal_elimination_percent=5.0,
            protein_binding_percent=84.0,
            therapeutic_class="antifungal",
            contraindications=["liver_disease"]
        )
        
        mechanisms["itraconazole"] = DrugMechanism(
            drug_name="itraconazole",
            cyp450_effects=["inhibitor"],
            cyp450_enzymes=["3A4"],
            hepatic_metabolism_percent=95.0,
            renal_elimination_percent=5.0,
            protein_binding_percent=99.0,
            therapeutic_class="antifungal",
            contraindications=["liver_disease", "heart_failure"]
        )
        
        mechanisms["fluconazole"] = DrugMechanism(
            drug_name="fluconazole",
            cyp450_effects=["inhibitor"],
            cyp450_enzymes=["2C9", "2C19"],
            hepatic_metabolism_percent=80.0,
            renal_elimination_percent=20.0,
            protein_binding_percent=12.0,
            therapeutic_class="antifungal",
            contraindications=["liver_disease"]
        )
        
        mechanisms["voriconazole"] = DrugMechanism(
            drug_name="voriconazole",
            cyp450_effects=["inhibitor", "substrate"],
            cyp450_enzymes=["2C19", "2C9", "3A4"],
            hepatic_metabolism_percent=95.0,
            renal_elimination_percent=5.0,
            protein_binding_percent=58.0,
            therapeutic_class="antifungal",
            contraindications=["liver_disease"]
        )
        
        mechanisms["terbinafine"] = DrugMechanism(
            drug_name="terbinafine",
            cyp450_effects=["inhibitor"],
            cyp450_enzymes=["2D6"],
            hepatic_metabolism_percent=85.0,
            renal_elimination_percent=15.0,
            protein_binding_percent=99.0,
            therapeutic_class="antifungal",
            contraindications=["liver_disease"]
        )
        
        return mechanisms

    def _initialize_interaction_rules(self) -> List[Dict]:
        """
        Initialize comprehensive mechanism-based interaction rules
        """
        rules = [
            # CYP450 Enzyme Interactions
            {
                "rule_type": "cyp450_induction_effect",
                "condition": lambda drug1, drug2: (
                    "inducer" in self.drug_mechanisms.get(drug1, DrugMechanism("", [], [], None, None, None, "", [])).cyp450_effects and
                    "substrate" in self.drug_mechanisms.get(drug2, DrugMechanism("", [], [], None, None, None, "", [])).cyp450_effects and
                    bool(set(self.drug_mechanisms.get(drug1, DrugMechanism("", [], [], None, None, None, "", [])).cyp450_enzymes) & 
                        set(self.drug_mechanisms.get(drug2, DrugMechanism("", [], [], None, None, None, "", [])).cyp450_enzymes))
                ),
                "interaction_type": InteractionType.CYP450_INDUCTION,
                "severity": InteractionSeverity.MODERATE,
                "mechanism": "CYP450 enzyme induction increases metabolism of substrate drug",
                "clinical_effect": "Decreased plasma concentration and efficacy of substrate drug",
                "management": "Monitor therapeutic response, may need dose adjustment"
            },
            {
                "rule_type": "cyp450_inhibition_effect", 
                "condition": lambda drug1, drug2: (
                    "inhibitor" in self.drug_mechanisms.get(drug1, DrugMechanism("", [], [], None, None, None, "", [])).cyp450_effects and
                    "substrate" in self.drug_mechanisms.get(drug2, DrugMechanism("", [], [], None, None, None, "", [])).cyp450_effects and
                    bool(set(self.drug_mechanisms.get(drug1, DrugMechanism("", [], [], None, None, None, "", [])).cyp450_enzymes) & 
                        set(self.drug_mechanisms.get(drug2, DrugMechanism("", [], [], None, None, None, "", [])).cyp450_enzymes))
                ),
                "interaction_type": InteractionType.CYP450_INHIBITION,
                "severity": InteractionSeverity.MAJOR,
                "mechanism": "CYP450 enzyme inhibition decreases metabolism of substrate drug",
                "clinical_effect": "Increased plasma concentration and potential toxicity of substrate drug",
                "management": "Reduce substrate drug dose, monitor for toxicity"
            },
            
            # Protein Binding Displacement Interactions
            {
                "rule_type": "protein_binding_displacement",
                "condition": lambda drug1, drug2: (
                    self.drug_mechanisms.get(drug1, DrugMechanism("", [], [], None, None, None, "", [])).protein_binding_percent and
                    self.drug_mechanisms.get(drug2, DrugMechanism("", [], [], None, None, None, "", [])).protein_binding_percent and
                    self.drug_mechanisms.get(drug1, DrugMechanism("", [], [], None, None, None, "", [])).protein_binding_percent > 95 and
                    self.drug_mechanisms.get(drug2, DrugMechanism("", [], [], None, None, None, "", [])).protein_binding_percent > 95
                ),
                "interaction_type": InteractionType.PROTEIN_BINDING,
                "severity": InteractionSeverity.MODERATE,
                "mechanism": "Highly protein-bound drugs compete for binding sites",
                "clinical_effect": "Displacement increases free drug concentration and activity",
                "management": "Monitor for enhanced effects, consider dose reduction"
            },
            
            # NSAID Class Interactions
            {
                "rule_type": "nsaid_combination",
                "condition": lambda drug1, drug2: (
                    self.drug_mechanisms.get(drug1, DrugMechanism("", [], [], None, None, None, "", [])).therapeutic_class in ["nsaid", "cox2_nsaid"] and
                    self.drug_mechanisms.get(drug2, DrugMechanism("", [], [], None, None, None, "", [])).therapeutic_class in ["nsaid", "cox2_nsaid"]
                ),
                "interaction_type": InteractionType.PHARMACODYNAMIC,
                "severity": InteractionSeverity.MAJOR,
                "mechanism": "Additive COX inhibition and GI/renal toxicity",
                "clinical_effect": "Increased risk of GI ulceration, bleeding, and nephrotoxicity",
                "management": "AVOID concurrent NSAID use - select single NSAID"
            },
            
            # Opioid Combination CNS Depression
            {
                "rule_type": "opioid_cns_depression",
                "condition": lambda drug1, drug2: (
                    self.drug_mechanisms.get(drug1, DrugMechanism("", [], [], None, None, None, "", [])).therapeutic_class in ["opioid_analgesic", "partial_opioid_agonist"] and
                    self.drug_mechanisms.get(drug2, DrugMechanism("", [], [], None, None, None, "", [])).therapeutic_class in ["benzodiazepine", "phenothiazine", "general_anesthetic"]
                ),
                "interaction_type": InteractionType.PHARMACODYNAMIC,
                "severity": InteractionSeverity.MAJOR,
                "mechanism": "Additive CNS and respiratory depression",
                "clinical_effect": "Enhanced sedation, respiratory depression, hypotension",
                "management": "Reduce doses of both drugs, monitor respiratory status closely"
            },
            
            # ACE Inhibitor + Diuretic Hypotension
            {
                "rule_type": "ace_diuretic_hypotension",
                "condition": lambda drug1, drug2: (
                    self.drug_mechanisms.get(drug1, DrugMechanism("", [], [], None, None, None, "", [])).therapeutic_class == "ace_inhibitor" and
                    self.drug_mechanisms.get(drug2, DrugMechanism("", [], [], None, None, None, "", [])).therapeutic_class == "loop_diuretic"
                ),
                "interaction_type": InteractionType.PHARMACODYNAMIC,
                "severity": InteractionSeverity.MODERATE,
                "mechanism": "Additive hypotensive effects",
                "clinical_effect": "Enhanced blood pressure reduction, risk of hypotension",
                "management": "Start with lower doses, monitor blood pressure closely"
            },
            
            # Fluoroquinolone + NSAIDs CNS Stimulation
            {
                "rule_type": "fluoroquinolone_nsaid_seizure",
                "condition": lambda drug1, drug2: (
                    self.drug_mechanisms.get(drug1, DrugMechanism("", [], [], None, None, None, "", [])).therapeutic_class == "fluoroquinolone" and
                    self.drug_mechanisms.get(drug2, DrugMechanism("", [], [], None, None, None, "", [])).therapeutic_class in ["nsaid", "cox2_nsaid"]
                ),
                "interaction_type": InteractionType.PHARMACODYNAMIC,
                "severity": InteractionSeverity.MODERATE,
                "mechanism": "GABA receptor antagonism increases seizure risk",
                "clinical_effect": "Increased risk of CNS stimulation and seizures",
                "management": "Use with caution, monitor for neurological signs"
            },
            
            # Hepatic Metabolism Concern
            {
                "rule_type": "hepatic_compromise_concern",
                "condition": lambda drug1, drug2: (
                    self.drug_mechanisms.get(drug1, DrugMechanism("", [], [], None, None, None, "", [])).hepatic_metabolism_percent and
                    self.drug_mechanisms.get(drug1, DrugMechanism("", [], [], None, None, None, "", [])).hepatic_metabolism_percent > 70
                ),
                "interaction_type": InteractionType.HEPATIC_METABOLISM,
                "severity": InteractionSeverity.MODERATE,
                "mechanism": "High hepatic metabolism dependency",
                "clinical_effect": "Reduced clearance in hepatic impairment",
                "management": "Dose reduction may be needed in liver disease"
            },
            
            # Renal Elimination Competition
            {
                "rule_type": "renal_elimination_competition",
                "condition": lambda drug1, drug2: (
                    self.drug_mechanisms.get(drug1, DrugMechanism("", [], [], None, None, None, "", [])).renal_elimination_percent and
                    self.drug_mechanisms.get(drug2, DrugMechanism("", [], [], None, None, None, "", [])).renal_elimination_percent and
                    self.drug_mechanisms.get(drug1, DrugMechanism("", [], [], None, None, None, "", [])).renal_elimination_percent > 80 and
                    self.drug_mechanisms.get(drug2, DrugMechanism("", [], [], None, None, None, "", [])).renal_elimination_percent > 80
                ),
                "interaction_type": InteractionType.RENAL_ELIMINATION,
                "severity": InteractionSeverity.MODERATE,
                "mechanism": "Competition for renal elimination pathways",
                "clinical_effect": "Potential for drug accumulation in renal impairment",
                "management": "Dose adjustment required in kidney disease"
            },
            
            # Antifungal CYP450 Inhibition (High Risk)
            {
                "rule_type": "antifungal_cyp450_inhibition",
                "condition": lambda drug1, drug2: (
                    self.drug_mechanisms.get(drug1, DrugMechanism("", [], [], None, None, None, "", [])).therapeutic_class == "antifungal" and
                    "substrate" in self.drug_mechanisms.get(drug2, DrugMechanism("", [], [], None, None, None, "", [])).cyp450_effects and
                    bool(set(self.drug_mechanisms.get(drug1, DrugMechanism("", [], [], None, None, None, "", [])).cyp450_enzymes) & 
                        set(self.drug_mechanisms.get(drug2, DrugMechanism("", [], [], None, None, None, "", [])).cyp450_enzymes))
                ),
                "interaction_type": InteractionType.CYP450_INHIBITION,
                "severity": InteractionSeverity.MAJOR,
                "mechanism": "Potent antifungal CYP450 inhibition",
                "clinical_effect": "Significant increase in substrate drug concentration",
                "management": "Consider substrate dose reduction by 50-75%, monitor closely"
            },
            
            # Beta-lactam Antibiotic Synergy
            {
                "rule_type": "beta_lactam_synergy",
                "condition": lambda drug1, drug2: (
                    self.drug_mechanisms.get(drug1, DrugMechanism("", [], [], None, None, None, "", [])).therapeutic_class == "beta_lactam_antibiotic" and
                    self.drug_mechanisms.get(drug2, DrugMechanism("", [], [], None, None, None, "", [])).therapeutic_class == "beta_lactamase_inhibitor"
                ),
                "interaction_type": InteractionType.PHARMACODYNAMIC,
                "severity": InteractionSeverity.MINOR,
                "mechanism": "Beta-lactamase inhibition enhances antibiotic efficacy",
                "clinical_effect": "Improved antimicrobial spectrum and effectiveness",
                "management": "Beneficial interaction - continue combination"
            }
        ]
        
        return rules

    def analyze_drug_interactions(self, drugs: List[str], patient_conditions: Optional[List[str]] = None) -> List[DrugInteraction]:
        """
        Comprehensive drug interaction analysis based on pharmacological mechanisms
        """
        self.logger.info(f"🔍 Analyzing interactions for drugs: {drugs}")
        
        interactions = []
        patient_conditions = patient_conditions or []
        
        # Normalize drug names
        normalized_drugs = [self._normalize_drug_name(drug) for drug in drugs]
        
        # Analyze all drug pairs
        for i in range(len(normalized_drugs)):
            for j in range(i + 1, len(normalized_drugs)):
                drug1, drug2 = normalized_drugs[i], normalized_drugs[j]
                
                # Get drug pair interactions
                pair_interactions = self._analyze_drug_pair(drug1, drug2, patient_conditions)
                interactions.extend(pair_interactions)
        
        # Sort by severity
        interactions.sort(key=lambda x: ["minor", "moderate", "major", "contraindicated"].index(x.severity.value), reverse=True)
        
        return interactions

    def _analyze_drug_pair(self, drug1: str, drug2: str, conditions: List[str]) -> List[DrugInteraction]:
        """
        Analyze interactions between two specific drugs
        """
        interactions = []
        
        # Get drug mechanisms
        mech1 = self.drug_mechanisms.get(drug1)
        mech2 = self.drug_mechanisms.get(drug2)
        
        if not mech1 or not mech2:
            # If we don't have mechanism data, return potential interaction note
            interactions.append(DrugInteraction(
                drug1=drug1,
                drug2=drug2,
                interaction_type=InteractionType.PHARMACODYNAMIC,
                severity=InteractionSeverity.MINOR,
                mechanism="Insufficient mechanism data available",
                clinical_effect="Potential interaction cannot be fully assessed",
                management="Monitor patient closely, consult additional references",
                confidence=0.3
            ))
            return interactions
        
        # Apply interaction rules
        for rule in self.interaction_rules:
            try:
                if rule["condition"](drug1, drug2) or rule["condition"](drug2, drug1):
                    interaction = DrugInteraction(
                        drug1=drug1,
                        drug2=drug2,
                        interaction_type=rule["interaction_type"],
                        severity=rule["severity"],
                        mechanism=rule["mechanism"],
                        clinical_effect=rule["clinical_effect"],
                        management=rule["management"],
                        confidence=0.8
                    )
                    interactions.append(interaction)
            except Exception as e:
                self.logger.warning(f"Error applying rule {rule['rule_type']}: {e}")
        
        # Check for specific high-confidence interactions
        high_confidence_interactions = self._check_specific_interactions(drug1, drug2)
        interactions.extend(high_confidence_interactions)
        
        return interactions

    def _check_specific_interactions(self, drug1: str, drug2: str) -> List[DrugInteraction]:
        """
        Check for specific well-documented veterinary interactions
        """
        interactions = []
        
        # Phenobarbital + CYP450 substrates (Strong Inducer)
        if drug1 == "phenobarbital" or drug2 == "phenobarbital":
            other_drug = drug2 if drug1 == "phenobarbital" else drug1
            other_mech = self.drug_mechanisms.get(other_drug)
            
            if other_mech and "substrate" in other_mech.cyp450_effects:
                interactions.append(DrugInteraction(
                    drug1="phenobarbital",
                    drug2=other_drug,
                    interaction_type=InteractionType.CYP450_INDUCTION,
                    severity=InteractionSeverity.MODERATE,
                    mechanism="Phenobarbital strongly induces CYP450 enzymes, increasing metabolism of substrate drugs",
                    clinical_effect=f"Decreased {other_drug} plasma concentration and therapeutic effect",
                    management=f"Monitor {other_drug} therapeutic response, may need dose increase",
                    confidence=0.9
                ))
        
        # Chloramphenicol + CYP450 substrates (Strong Inhibitor)
        if drug1 == "chloramphenicol" or drug2 == "chloramphenicol":
            other_drug = drug2 if drug1 == "chloramphenicol" else drug1
            other_mech = self.drug_mechanisms.get(other_drug)
            
            if other_mech and "substrate" in other_mech.cyp450_effects:
                interactions.append(DrugInteraction(
                    drug1="chloramphenicol",
                    drug2=other_drug,
                    interaction_type=InteractionType.CYP450_INHIBITION,
                    severity=InteractionSeverity.MAJOR,
                    mechanism="Chloramphenicol inhibits CYP450 enzymes, decreasing metabolism of substrate drugs",
                    clinical_effect=f"Increased {other_drug} plasma concentration and risk of toxicity",
                    management=f"Reduce {other_drug} dose, monitor for toxicity signs",
                    confidence=0.95
                ))
        
        # Ketoconazole/Itraconazole + CYP3A4 substrates (Potent Inhibitors)
        antifungals = ["ketoconazole", "itraconazole"]
        if drug1 in antifungals or drug2 in antifungals:
            antifungal = drug1 if drug1 in antifungals else drug2
            other_drug = drug2 if drug1 in antifungals else drug1
            other_mech = self.drug_mechanisms.get(other_drug)
            
            if other_mech and "substrate" in other_mech.cyp450_effects and "3A4" in other_mech.cyp450_enzymes:
                interactions.append(DrugInteraction(
                    drug1=antifungal,
                    drug2=other_drug,
                    interaction_type=InteractionType.CYP450_INHIBITION,
                    severity=InteractionSeverity.MAJOR,
                    mechanism=f"{antifungal.title()} potently inhibits CYP3A4, severely reducing {other_drug} metabolism",
                    clinical_effect=f"2-10 fold increase in {other_drug} concentration, high toxicity risk",
                    management=f"Reduce {other_drug} dose by 75% or avoid combination",
                    confidence=0.95
                ))
        
        # Enrofloxacin + Theophylline (Classic CYP1A2 Interaction)
        if (drug1 == "enrofloxacin" and drug2 == "theophylline") or (drug1 == "theophylline" and drug2 == "enrofloxacin"):
            interactions.append(DrugInteraction(
                drug1="enrofloxacin",
                drug2="theophylline",
                interaction_type=InteractionType.CYP450_INHIBITION,
                severity=InteractionSeverity.MAJOR,
                mechanism="Enrofloxacin inhibits CYP1A2, reducing theophylline metabolism",
                clinical_effect="Theophylline toxicity: seizures, arrhythmias, gastrointestinal upset",
                management="Reduce theophylline dose by 50%, monitor plasma levels",
                confidence=0.95
            ))
        
        # Tramadol + MAOIs/SSRIs (Serotonin Syndrome Risk)
        serotonergic_drugs = ["fluoxetine", "sertraline", "selegiline"]
        if drug1 == "tramadol" and drug2 in serotonergic_drugs:
            interactions.append(DrugInteraction(
                drug1="tramadol",
                drug2=drug2,
                interaction_type=InteractionType.PHARMACODYNAMIC,
                severity=InteractionSeverity.MAJOR,
                mechanism="Tramadol increases serotonin, MAOIs/SSRIs block serotonin reuptake",
                clinical_effect="Serotonin syndrome: hyperthermia, agitation, muscle rigidity",
                management="AVOID combination or use extreme caution with monitoring",
                confidence=0.9
            ))
        
        # Digoxin + Furosemide (Electrolyte-mediated interaction)
        if (drug1 == "digoxin" and drug2 == "furosemide") or (drug1 == "furosemide" and drug2 == "digoxin"):
            interactions.append(DrugInteraction(
                drug1="furosemide",
                drug2="digoxin",
                interaction_type=InteractionType.PHARMACODYNAMIC,
                severity=InteractionSeverity.MODERATE,
                mechanism="Furosemide-induced hypokalemia increases digoxin sensitivity",
                clinical_effect="Enhanced digoxin effects, risk of cardiac arrhythmias",
                management="Monitor potassium levels, supplement potassium as needed",
                confidence=0.85
            ))
        
        # Metronidazole + Warfarin (Classic CYP2C9 Interaction)
        if (drug1 == "metronidazole" and drug2 == "warfarin") or (drug1 == "warfarin" and drug2 == "metronidazole"):
            interactions.append(DrugInteraction(
                drug1="metronidazole",
                drug2="warfarin",
                interaction_type=InteractionType.CYP450_INHIBITION,
                severity=InteractionSeverity.MAJOR,
                mechanism="Metronidazole inhibits CYP2C9, reducing warfarin metabolism",
                clinical_effect="Enhanced anticoagulation, increased bleeding risk",
                management="Reduce warfarin dose, monitor coagulation times closely",
                confidence=0.9
            ))
        
        # NSAID + ACE Inhibitor (Renal Protection Loss)
        nsaids = ["carprofen", "meloxicam", "firocoxib"]
        ace_inhibitors = ["enalapril", "benazepril"]
        if drug1 in nsaids and drug2 in ace_inhibitors:
            interactions.append(DrugInteraction(
                drug1=drug1,
                drug2=drug2,
                interaction_type=InteractionType.PHARMACODYNAMIC,
                severity=InteractionSeverity.MODERATE,
                mechanism="NSAIDs reduce prostaglandin-mediated renal protection by ACE inhibitors",
                clinical_effect="Reduced renal function, potential acute kidney injury",
                management="Monitor renal function closely, ensure adequate hydration",
                confidence=0.85
            ))
        
        return interactions

    def _normalize_drug_name(self, drug_name: str) -> str:
        """
        Normalize drug names for consistent matching
        """
        # Convert to lowercase and remove common suffixes
        normalized = drug_name.lower().strip()
        
        # Handle combination drugs
        if "clavamox" in normalized:
            return "amoxicillin"  # Primary component
        
        # Remove common formulation suffixes
        suffixes = ["_tablet", "_injection", "_oral", "_iv", "_im", "_sc"]
        for suffix in suffixes:
            normalized = normalized.replace(suffix, "")
        
        return normalized

    def get_hepatic_metabolism_principle(self, drug_name: str) -> Dict[str, any]:
        """
        Get hepatic metabolism information for a drug
        """
        normalized_name = self._normalize_drug_name(drug_name)
        mechanism = self.drug_mechanisms.get(normalized_name)
        
        if not mechanism:
            return {
                "drug": drug_name,
                "hepatic_metabolism_percent": None,
                "principle": "Insufficient data available",
                "clinical_significance": "Unknown - consult additional references"
            }
        
        hepatic_percent = mechanism.hepatic_metabolism_percent or 0
        
        principle = ""
        clinical_significance = ""
        
        if hepatic_percent >= 75:
            principle = "High hepatic metabolism dependency - primarily eliminated by liver enzymes"
            clinical_significance = "Significant dose reduction required in hepatic impairment to prevent accumulation and toxicity"
        elif hepatic_percent >= 50:
            principle = "Moderate hepatic metabolism dependency - partially eliminated by liver"
            clinical_significance = "Moderate dose adjustment may be needed in hepatic impairment"
        elif hepatic_percent >= 25:
            principle = "Low hepatic metabolism dependency - minimally affected by liver function"
            clinical_significance = "Minor dose adjustment may be sufficient in hepatic impairment"
        else:
            principle = "Minimal hepatic metabolism - primarily eliminated by other routes"
            clinical_significance = "Hepatic impairment unlikely to significantly affect dosing"
        
        return {
            "drug": drug_name,
            "hepatic_metabolism_percent": hepatic_percent,
            "principle": principle,
            "clinical_significance": clinical_significance,
            "contraindications": mechanism.contraindications
        }

    def generate_interaction_report(self, interactions: List[DrugInteraction]) -> str:
        """
        Generate a comprehensive interaction report
        """
        if not interactions:
            return "🟢 No significant drug interactions detected based on pharmacological mechanisms."
        
        report = []
        report.append("🔬 PHARMACOLOGICAL INTERACTION ANALYSIS")
        report.append("=" * 60)
        
        # Group by severity
        severity_groups = {}
        for interaction in interactions:
            severity = interaction.severity.value
            if severity not in severity_groups:
                severity_groups[severity] = []
            severity_groups[severity].append(interaction)
        
        # Report by severity (most severe first)
        severity_order = ["contraindicated", "major", "moderate", "minor"]
        
        for severity in severity_order:
            if severity in severity_groups:
                severity_emoji = {
                    "contraindicated": "🚨",
                    "major": "🔴", 
                    "moderate": "🟡",
                    "minor": "🟢"
                }
                
                report.append(f"\n{severity_emoji[severity]} {severity.upper()} INTERACTIONS:")
                report.append("-" * 40)
                
                for interaction in severity_groups[severity]:
                    report.append(f"📋 {interaction.drug1.title()} + {interaction.drug2.title()}")
                    report.append(f"   🧬 Mechanism: {interaction.mechanism}")
                    report.append(f"   ⚠️ Clinical Effect: {interaction.clinical_effect}")
                    report.append(f"   💊 Management: {interaction.management}")
                    report.append(f"   🎯 Confidence: {interaction.confidence:.0%}")
                    report.append("")
        
        report.append("📚 PHARMACOLOGICAL PRINCIPLES APPLIED:")
        report.append("• CYP450 enzyme induction/inhibition effects")
        report.append("• Hepatic metabolism pathway analysis")
        report.append("• Mechanism-based interaction prediction")
        report.append("• Clinical significance assessment")
        
        return "\n".join(report)

def main():
    """Test the pharmacological reasoning engine"""
    engine = PharmacologicalReasoningEngine()
    
    print("\n🧪 TESTING PHARMACOLOGICAL REASONING ENGINE")
    print("=" * 60)
    
    # Test Case 1: Phenobarbital + Clavamox (from user critique)
    print("📋 Test Case 1: Phenobarbital + Clavamox Interaction")
    print("-" * 50)
    
    drugs = ["phenobarbital", "clavamox"]
    interactions = engine.analyze_drug_interactions(drugs)
    
    report = engine.generate_interaction_report(interactions)
    print(report)
    
    # Test Case 2: Hepatic metabolism principle
    print(f"\n📋 Test Case 2: Hepatic Metabolism Principle")
    print("-" * 50)
    
    hepatic_info = engine.get_hepatic_metabolism_principle("phenobarbital")
    print(f"🧬 Drug: {hepatic_info['drug']}")
    print(f"📊 Hepatic Metabolism: {hepatic_info['hepatic_metabolism_percent']}%")
    print(f"🔬 Principle: {hepatic_info['principle']}")
    print(f"⚠️ Clinical Significance: {hepatic_info['clinical_significance']}")
    
    if hepatic_info['contraindications']:
        print(f"🚫 Contraindications: {', '.join(hepatic_info['contraindications'])}")

if __name__ == "__main__":
    main()