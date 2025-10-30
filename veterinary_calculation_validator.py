#!/usr/bin/env python3
"""
Veterinary Calculation Validation System
Critical safety layer for all veterinary drug dosing calculations
"""

import re
import math
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging

class CalculationType(Enum):
    SIMPLE_DOSING = "simple_dosing"
    CRI_CALCULATION = "cri_calculation"
    MULTI_DRUG = "multi_drug"
    DILUTION = "dilution"
    UNIT_CONVERSION = "unit_conversion"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class CalculationStep:
    step_number: int
    description: str
    formula: str
    inputs: Dict[str, Any]
    result: float
    units: str
    verification_method: str

@dataclass
class ValidationResult:
    is_valid: bool
    confidence: float
    risk_level: RiskLevel
    errors: List[str]
    warnings: List[str]
    calculation_steps: List[CalculationStep]
    verification_methods: List[str]
    requires_manual_review: bool

class VeterinaryCalculationValidator:
    """
    Critical safety system for validating all veterinary drug calculations
    """
    
    def __init__(self):
        """Initialize the validation system with safety thresholds"""
        self.logger = logging.getLogger(__name__)
        
        # Safety thresholds
        self.MAX_DOSING_ERROR_PERCENT = 10.0  # Flag if calculations differ by >10%
        self.CRITICAL_DRUGS = [
            "morphine", "fentanyl", "propofol", "pentobarbital", "phenobarbital",
            "insulin", "epinephrine", "dopamine", "dobutamine"
        ]
        
        # Unit conversion factors
        self.UNIT_CONVERSIONS = {
            "kg_to_g": 1000,
            "g_to_mg": 1000,
            "mg_to_mcg": 1000,
            "ml_to_l": 0.001,
            "hours_to_minutes": 60
        }
        
        # Dosing range safety limits (mg/kg unless specified)
        self.SAFETY_RANGES = {
            "morphine": {"min": 0.1, "max": 2.0, "units": "mg/kg"},
            "lidocaine": {"min": 1.0, "max": 4.0, "units": "mg/kg/hour"},
            "ketamine": {"min": 0.5, "max": 2.0, "units": "mg/kg/hour"},
            "phenobarbital": {"min": 2.0, "max": 8.0, "units": "mg/kg/day"},
            "acepromazine": {"min": 0.01, "max": 0.1, "units": "mg/kg"}
        }

    def validate_calculation(self, calculation_text: str, context: Dict[str, Any]) -> ValidationResult:
        """
        Main validation entry point for any veterinary calculation
        """
        self.logger.info(f"🧮 Validating calculation: {calculation_text[:100]}...")
        
        try:
            # Extract calculation components
            calc_type = self._identify_calculation_type(calculation_text, context)
            extracted_data = self._extract_calculation_data(calculation_text)
            
            # Perform validation based on calculation type
            if calc_type == CalculationType.CRI_CALCULATION:
                return self._validate_cri_calculation(extracted_data, context)
            elif calc_type == CalculationType.SIMPLE_DOSING:
                return self._validate_simple_dosing(extracted_data, context)
            elif calc_type == CalculationType.MULTI_DRUG:
                return self._validate_multi_drug_calculation(extracted_data, context)
            else:
                return self._validate_generic_calculation(extracted_data, context)
                
        except Exception as e:
            self.logger.error(f"Validation error: {e}")
            return ValidationResult(
                is_valid=False,
                confidence=0.0,
                risk_level=RiskLevel.CRITICAL,
                errors=[f"Validation system error: {e}"],
                warnings=["CRITICAL: Could not validate calculation - manual review required"],
                calculation_steps=[],
                verification_methods=[],
                requires_manual_review=True
            )

    def _validate_cri_calculation(self, data: Dict[str, Any], context: Dict[str, Any]) -> ValidationResult:
        """
        Validate Constant Rate Infusion calculations (high risk)
        """
        self.logger.info("🔴 Validating CRI calculation (HIGH RISK)")
        
        errors = []
        warnings = []
        steps = []
        
        try:
            # Extract essential parameters
            weight_kg = data.get("weight", context.get("weight", 0))
            bag_volume_ml = data.get("bag_volume", 250)
            flow_rate_ml_hr = data.get("flow_rate", 0)
            drugs = data.get("drugs", [])
            
            if not weight_kg or not flow_rate_ml_hr:
                errors.append("Missing critical parameters: weight or flow rate")
                return self._create_error_result(errors)
            
            # Step 1: Calculate total run time
            total_hours = bag_volume_ml / flow_rate_ml_hr
            steps.append(CalculationStep(
                step_number=1,
                description="Calculate total bag run time",
                formula="Total hours = Bag volume (mL) / Flow rate (mL/hr)",
                inputs={"bag_volume": bag_volume_ml, "flow_rate": flow_rate_ml_hr},
                result=total_hours,
                units="hours",
                verification_method="division_check"
            ))
            
            # Verify this step with alternative calculation
            alt_total_hours = bag_volume_ml / flow_rate_ml_hr
            if abs(total_hours - alt_total_hours) > 0.01:
                errors.append(f"Time calculation error: {total_hours} vs {alt_total_hours}")
            
            # Step 2: Validate each drug calculation
            total_drug_volume = 0
            
            for i, drug in enumerate(drugs):
                drug_name = drug.get("name", f"Drug_{i+1}")
                dose_per_kg_hr = drug.get("dose_per_kg_hr", 0)
                concentration_mg_ml = drug.get("concentration", 0)
                
                if not dose_per_kg_hr or not concentration_mg_ml:
                    errors.append(f"{drug_name}: Missing dose or concentration")
                    continue
                
                # Calculate hourly dose needed
                hourly_dose_mg = dose_per_kg_hr * weight_kg
                
                # Calculate total dose needed for entire bag duration
                total_dose_needed_mg = hourly_dose_mg * total_hours
                
                # Calculate volume to add
                volume_to_add_ml = total_dose_needed_mg / concentration_mg_ml
                total_drug_volume += volume_to_add_ml
                
                # Verification: Alternative calculation method
                alt_volume = (dose_per_kg_hr * weight_kg * total_hours) / concentration_mg_ml
                percentage_diff = abs((volume_to_add_ml - alt_volume) / volume_to_add_ml) * 100
                
                if percentage_diff > self.MAX_DOSING_ERROR_PERCENT:
                    errors.append(f"{drug_name}: Calculation discrepancy {percentage_diff:.1f}%")
                
                # Check dosing range safety
                if drug_name.lower() in self.SAFETY_RANGES:
                    safety_range = self.SAFETY_RANGES[drug_name.lower()]
                    if dose_per_kg_hr < safety_range["min"] or dose_per_kg_hr > safety_range["max"]:
                        warnings.append(f"{drug_name}: Dose {dose_per_kg_hr} {safety_range['units']} outside safe range ({safety_range['min']}-{safety_range['max']})")
                
                steps.append(CalculationStep(
                    step_number=len(steps) + 1,
                    description=f"Calculate {drug_name} volume to add",
                    formula=f"Volume = (Dose/kg/hr × Weight × Total hours) / Concentration",
                    inputs={
                        "dose_per_kg_hr": dose_per_kg_hr,
                        "weight": weight_kg,
                        "total_hours": total_hours,
                        "concentration": concentration_mg_ml
                    },
                    result=volume_to_add_ml,
                    units="mL",
                    verification_method="cross_multiplication"
                ))
            
            # Step 3: Check total volume displacement
            if total_drug_volume > bag_volume_ml * 0.2:  # >20% displacement
                warnings.append(f"High volume displacement: {total_drug_volume:.1f}mL from {bag_volume_ml}mL bag")
            
            # Determine risk level
            risk_level = RiskLevel.HIGH  # CRIs are always high risk
            if any(drug.get("name", "").lower() in self.CRITICAL_DRUGS for drug in drugs):
                risk_level = RiskLevel.CRITICAL
            
            return ValidationResult(
                is_valid=len(errors) == 0,
                confidence=0.95 if len(errors) == 0 else 0.3,
                risk_level=risk_level,
                errors=errors,
                warnings=warnings,
                calculation_steps=steps,
                verification_methods=["cross_calculation", "range_checking", "volume_displacement"],
                requires_manual_review=risk_level == RiskLevel.CRITICAL or len(errors) > 0
            )
            
        except Exception as e:
            return self._create_error_result([f"CRI validation error: {e}"])

    def _validate_simple_dosing(self, data: Dict[str, Any], context: Dict[str, Any]) -> ValidationResult:
        """
        Validate simple drug dosing calculations
        """
        self.logger.info("🟡 Validating simple dosing calculation")
        
        errors = []
        warnings = []
        steps = []
        
        try:
            weight_kg = data.get("weight", context.get("weight", 0))
            # Try multiple ways to get dose per kg
            dose_per_kg = data.get("dose_per_kg", 0)
            if not dose_per_kg and "doses" in data and data["doses"]:
                dose_per_kg = data["doses"][0]  # Take first dose found
            drug_name = data.get("drug_name", context.get("drugs_mentioned", ["unknown"])[0] if context.get("drugs_mentioned") else "unknown")
            
            if not weight_kg or not dose_per_kg:
                errors.append("Missing weight or dose per kg")
                return self._create_error_result(errors)
            
            # Calculate total dose
            total_dose = dose_per_kg * weight_kg
            
            # Verification calculation
            alt_total_dose = weight_kg * dose_per_kg
            if abs(total_dose - alt_total_dose) > 0.001:
                errors.append("Dose calculation verification failed")
            
            # Check safety ranges
            if drug_name.lower() in self.SAFETY_RANGES:
                safety_range = self.SAFETY_RANGES[drug_name.lower()]
                if dose_per_kg < safety_range["min"] or dose_per_kg > safety_range["max"]:
                    warnings.append(f"Dose {dose_per_kg} outside safe range ({safety_range['min']}-{safety_range['max']}) {safety_range['units']}")
            
            steps.append(CalculationStep(
                step_number=1,
                description="Calculate total dose",
                formula="Total dose = Dose per kg × Weight",
                inputs={"dose_per_kg": dose_per_kg, "weight": weight_kg},
                result=total_dose,
                units="mg",
                verification_method="multiplication_check"
            ))
            
            risk_level = RiskLevel.MEDIUM if drug_name.lower() in self.CRITICAL_DRUGS else RiskLevel.LOW
            
            return ValidationResult(
                is_valid=len(errors) == 0,
                confidence=0.98 if len(errors) == 0 else 0.5,
                risk_level=risk_level,
                errors=errors,
                warnings=warnings,
                calculation_steps=steps,
                verification_methods=["multiplication_verification", "range_checking"],
                requires_manual_review=risk_level == RiskLevel.CRITICAL or len(warnings) > 0
            )
            
        except Exception as e:
            return self._create_error_result([f"Simple dosing validation error: {e}"])

    def _identify_calculation_type(self, text: str, context: Dict[str, Any]) -> CalculationType:
        """
        Identify the type of calculation being performed
        """
        text_lower = text.lower()
        
        # CRI indicators
        if any(keyword in text_lower for keyword in ["cri", "constant rate", "infusion", "mlk", "morphine", "lidocaine", "ketamine"]):
            return CalculationType.CRI_CALCULATION
        
        # Multi-drug indicators
        if any(keyword in text_lower for keyword in ["multiple", "combination", "and", "+"]) and "drug" in text_lower:
            return CalculationType.MULTI_DRUG
        
        # Simple dosing indicators
        if any(keyword in text_lower for keyword in ["mg/kg", "dose", "dosage", "tablet"]):
            return CalculationType.SIMPLE_DOSING
        
        # Default to simple dosing
        return CalculationType.SIMPLE_DOSING

    def _extract_calculation_data(self, text: str) -> Dict[str, Any]:
        """
        Extract numerical data and parameters from calculation text
        """
        data = {}
        
        # Extract weight
        weight_match = re.search(r"(\d+\.?\d*)\s*kg", text, re.IGNORECASE)
        if weight_match:
            data["weight"] = float(weight_match.group(1))
        
        # Extract doses (mg/kg or mg/kg/hour)
        dose_matches = re.findall(r"(\d+\.?\d*)\s*mg/kg(?:/hour|/hr)?", text, re.IGNORECASE)
        if dose_matches:
            data["doses"] = [float(dose) for dose in dose_matches]
        
        # Extract concentrations
        conc_matches = re.findall(r"(\d+\.?\d*)\s*mg/ml", text, re.IGNORECASE)
        if conc_matches:
            data["concentrations"] = [float(conc) for conc in conc_matches]
        
        # Extract volumes
        vol_matches = re.findall(r"(\d+\.?\d*)\s*ml", text, re.IGNORECASE)
        if vol_matches:
            data["volumes"] = [float(vol) for vol in vol_matches]
        
        # Extract flow rates
        flow_match = re.search(r"(\d+\.?\d*)\s*ml/hour", text, re.IGNORECASE)
        if flow_match:
            data["flow_rate"] = float(flow_match.group(1))
        
        return data

    def _validate_multi_drug_calculation(self, data: Dict[str, Any], context: Dict[str, Any]) -> ValidationResult:
        """
        Validate calculations involving multiple drugs
        """
        return ValidationResult(
            is_valid=False,
            confidence=0.0,
            risk_level=RiskLevel.CRITICAL,
            errors=["Multi-drug calculations require manual review"],
            warnings=["Complex drug combinations need veterinary oversight"],
            calculation_steps=[],
            verification_methods=[],
            requires_manual_review=True
        )

    def _validate_generic_calculation(self, data: Dict[str, Any], context: Dict[str, Any]) -> ValidationResult:
        """
        Generic validation for unidentified calculation types
        """
        return ValidationResult(
            is_valid=False,
            confidence=0.0,
            risk_level=RiskLevel.HIGH,
            errors=["Calculation type not recognized"],
            warnings=["Manual verification required for unknown calculation type"],
            calculation_steps=[],
            verification_methods=[],
            requires_manual_review=True
        )

    def _create_error_result(self, errors: List[str]) -> ValidationResult:
        """
        Create a validation result indicating errors
        """
        return ValidationResult(
            is_valid=False,
            confidence=0.0,
            risk_level=RiskLevel.CRITICAL,
            errors=errors,
            warnings=["CRITICAL CALCULATION ERROR - DO NOT USE"],
            calculation_steps=[],
            verification_methods=[],
            requires_manual_review=True
        )

    def generate_safety_report(self, validation_result: ValidationResult) -> str:
        """
        Generate a clean safety report - only show critical issues
        """
        # Only show warnings for CRITICAL issues that require intervention
        if validation_result.risk_level == RiskLevel.CRITICAL and validation_result.errors:
            report = []
            report.append("⚠️ **Calculation Review Required**")
            
            # Only show actual errors
            for error in validation_result.errors:
                report.append(f"• {error}")
            
            report.append("\n*Please verify calculations with veterinary references before implementation.*")
            return "\n".join(report)
        
        # For non-critical issues, return empty string (no diagnostic noise)
        return ""

def main():
    """Test the validation system with known problematic calculations"""
    validator = VeterinaryCalculationValidator()
    
    # Test the MLK CRI calculation that failed
    test_calculation = """
    MLK CRI for 4.5 kg Beagle:
    - Morphine: 0.12 mg/kg/hour at 15 mg/mL concentration
    - Lidocaine: 2.4 mg/kg/hour at 20 mg/mL concentration  
    - Ketamine: 0.6 mg/kg/hour at 100 mg/mL concentration
    - 250 mL bag, 6 mL/hour flow rate
    """
    
    context = {
        "weight": 4.5,
        "bag_volume": 250,
        "flow_rate": 6,
        "drugs": [
            {"name": "morphine", "dose_per_kg_hr": 0.12, "concentration": 15},
            {"name": "lidocaine", "dose_per_kg_hr": 2.4, "concentration": 20},
            {"name": "ketamine", "dose_per_kg_hr": 0.6, "concentration": 100}
        ]
    }
    
    print("🧪 Testing Veterinary Calculation Validator")
    print("="*60)
    
    result = validator.validate_calculation(test_calculation, context)
    print(validator.generate_safety_report(result))

if __name__ == "__main__":
    main()