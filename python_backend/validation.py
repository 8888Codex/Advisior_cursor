"""
Validation and confidence classification system for persona data
"""
from typing import Dict, List, Any, Optional, Tuple
import re
from datetime import datetime

class PersonaValidator:
    """
    Validates persona data and assigns confidence levels
    
    Features:
    - Validates required fields
    - Checks data consistency
    - Assigns confidence levels to data points
    - Validates quantitative metrics
    """
    
    @staticmethod
    def validate_persona(persona_data: Dict) -> Tuple[bool, List[str], Dict]:
        """
        Validate persona data and return validation status, errors, and enhanced data
        
        Args:
            persona_data: The persona data to validate
            
        Returns:
            Tuple of (is_valid, error_messages, enhanced_data)
        """
        errors = []
        confidence_metadata = {}
        
        # Check required fields
        required_fields = [
            "job_statement", 
            "demographics", 
            "behaviors", 
            "aspirations", 
            "goals",
            "functional_jobs",
            "emotional_jobs"
        ]
        
        for field in required_fields:
            if field not in persona_data or not persona_data[field]:
                errors.append(f"Missing required field: {field}")
        
        # If critical fields are missing, return early
        if errors:
            return False, errors, persona_data
        
        # Validate and enhance job statement
        job_statement = persona_data.get("job_statement", "")
        job_statement_confidence = PersonaValidator._validate_job_statement(job_statement)
        confidence_metadata["job_statement"] = job_statement_confidence
        
        # Validate and enhance demographics
        demographics = persona_data.get("demographics", {})
        demographics_confidence = PersonaValidator._validate_demographics(demographics)
        confidence_metadata["demographics"] = demographics_confidence
        
        # Validate and enhance goals
        goals = persona_data.get("goals", [])
        goals_confidence = PersonaValidator._validate_goals(goals)
        confidence_metadata["goals"] = goals_confidence
        
        # Validate quantitative pain points
        pain_points = persona_data.get("pain_points_quantified", [])
        pain_points_confidence = PersonaValidator._validate_pain_points(pain_points)
        confidence_metadata["pain_points_quantified"] = pain_points_confidence
        
        # Validate behaviors
        behaviors = persona_data.get("behaviors", {})
        behaviors_confidence = PersonaValidator._validate_behaviors(behaviors)
        confidence_metadata["behaviors"] = behaviors_confidence
        
        # Add confidence metadata to research_data
        if "research_data" not in persona_data:
            persona_data["research_data"] = {}
        
        persona_data["research_data"]["confidence_metadata"] = confidence_metadata
        
        # Calculate overall confidence
        confidence_scores = {
            "high": 3,
            "medium": 2,
            "low": 1
        }
        
        total_score = 0
        total_items = 0
        
        for category, level in confidence_metadata.items():
            if level in confidence_scores:
                total_score += confidence_scores[level]
                total_items += 1
        
        if total_items > 0:
            avg_score = total_score / total_items
            
            if avg_score >= 2.5:
                overall_confidence = "high"
            elif avg_score >= 1.5:
                overall_confidence = "medium"
            else:
                overall_confidence = "low"
                
            persona_data["research_data"]["confidence_level"] = overall_confidence
        
        # Add validation timestamp
        persona_data["research_data"]["validated_at"] = datetime.utcnow().isoformat()
        
        return len(errors) == 0, errors, persona_data
    
    @staticmethod
    def _validate_job_statement(job_statement: str) -> str:
        """
        Validate job statement and return confidence level
        
        Args:
            job_statement: The job statement to validate
            
        Returns:
            Confidence level: "high", "medium", or "low"
        """
        if not job_statement:
            return "low"
        
        # Check length
        if len(job_statement) < 20:
            return "low"
        
        # Check for action verbs
        action_verbs = ["encontrar", "criar", "melhorar", "otimizar", "resolver", "aumentar", "reduzir"]
        has_action_verb = any(verb in job_statement.lower() for verb in action_verbs)
        
        # Check for outcome
        outcome_indicators = ["para", "a fim de", "com o objetivo de", "visando", "buscando"]
        has_outcome = any(indicator in job_statement.lower() for indicator in outcome_indicators)
        
        if has_action_verb and has_outcome:
            return "high"
        elif has_action_verb or has_outcome:
            return "medium"
        else:
            return "low"
    
    @staticmethod
    def _validate_demographics(demographics: Dict) -> str:
        """
        Validate demographics and return confidence level
        
        Args:
            demographics: The demographics data to validate
            
        Returns:
            Confidence level: "high", "medium", or "low"
        """
        if not demographics:
            return "low"
        
        required_fields = ["age", "location", "occupation"]
        present_fields = [field for field in required_fields if field in demographics and demographics[field]]
        
        if len(present_fields) == len(required_fields):
            return "high"
        elif len(present_fields) >= len(required_fields) // 2:
            return "medium"
        else:
            return "low"
    
    @staticmethod
    def _validate_goals(goals: List[Dict]) -> str:
        """
        Validate goals and return confidence level
        
        Args:
            goals: The goals data to validate
            
        Returns:
            Confidence level: "high", "medium", or "low"
        """
        if not goals:
            return "low"
        
        # Check if goals have required fields
        complete_goals = 0
        for goal in goals:
            if "description" in goal and "timeframe" in goal:
                if "success_metrics" in goal and goal["success_metrics"]:
                    complete_goals += 1
        
        if complete_goals >= 3:
            return "high"
        elif complete_goals >= 1:
            return "medium"
        else:
            return "low"
    
    @staticmethod
    def _validate_pain_points(pain_points: List[Dict]) -> str:
        """
        Validate quantified pain points and return confidence level
        
        Args:
            pain_points: The pain points data to validate
            
        Returns:
            Confidence level: "high", "medium", or "low"
        """
        if not pain_points:
            return "low"
        
        # Check if pain points have quantitative metrics
        quantified_count = 0
        for pain in pain_points:
            if "description" in pain and "impact" in pain:
                # Check if impact contains numbers
                if re.search(r'\d+', pain["impact"]):
                    quantified_count += 1
        
        if quantified_count >= 3:
            return "high"
        elif quantified_count >= 1:
            return "medium"
        else:
            return "low"
    
    @staticmethod
    def _validate_behaviors(behaviors: Dict) -> str:
        """
        Validate behaviors and return confidence level
        
        Args:
            behaviors: The behaviors data to validate
            
        Returns:
            Confidence level: "high", "medium", or "low"
        """
        if not behaviors:
            return "low"
        
        # Check number of behavior categories and items
        category_count = len(behaviors)
        total_behaviors = sum(len(items) for items in behaviors.values())
        
        if category_count >= 3 and total_behaviors >= 9:
            return "high"
        elif category_count >= 2 and total_behaviors >= 5:
            return "medium"
        else:
            return "low"

# Singleton instance
persona_validator = PersonaValidator()
