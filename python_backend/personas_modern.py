"""
Modern Persona Builder Endpoints - JTBD and BAG Frameworks
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Optional
from datetime import datetime
import uuid

from python_backend.models_persona import PersonaModern, PersonaModernCreate
from python_backend.reddit_research import reddit_research
from python_backend.storage import storage
from python_backend.auth import get_current_user, get_current_user_optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from slowapi import Limiter
from slowapi.util import get_remote_address
from python_backend.validation import persona_validator

# Create router
router = APIRouter(prefix="/api/personas-modern", tags=["personas-modern"])

# Get limiter from main app
limiter = Limiter(key_func=get_remote_address)

# Optional security for development
security = HTTPBearer(auto_error=False)

@router.post("", response_model=PersonaModern)
@limiter.limit("5/hour")  # More restrictive limit due to API costs
async def create_modern_persona(
    request: Request, 
    data: PersonaModernCreate, 
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    """
    Create a modern persona using JTBD and BAG frameworks.
    
    Uses Perplexity API for research and Claude for structuring.
    
    Modes:
    - quick: Basic insights with JTBD and BAG frameworks
    - strategic: Comprehensive analysis with quantified data
    
    Frameworks:
    - hybrid: Combines JTBD and BAG (recommended)
    - jtbd: Focus on Jobs to Be Done
    - bag: Focus on Behaviors, Aspirations, Goals
    """
    # For development, always use default_user
    user_id = "default_user"
    
    try:
        # Conduct research based on mode
        if data.mode == "quick":
            research_data = await reddit_research.research_quick(
                target_description=data.targetDescription,
                industry=data.industry
            )
        else:  # strategic
            research_data = await reddit_research.research_strategic(
                target_description=data.targetDescription,
                industry=data.industry,
                additional_context=data.additionalContext
            )
        
        # Generate persona name if not provided
        persona_name = f"Persona: {data.targetDescription[:50]}"
        
        # Create persona ID
        persona_id = str(uuid.uuid4())
        
        # Create timestamps
        now = datetime.utcnow()
        
        # Convert research data to PersonaModern model
        # This handles the transformation from the API response to our model
        persona_data = {
            "id": persona_id,
            "userId": user_id,
            "name": persona_name,
            "researchMode": data.mode,
            "created_at": now,
            "updated_at": now
        }
        
        # Merge with research data
        persona_data.update(research_data)
        
        # Validate and enhance persona data
        is_valid, validation_errors, enhanced_data = persona_validator.validate_persona(persona_data)
        
        # Log validation results
        if not is_valid:
            print(f"[WARNING] Persona validation errors: {validation_errors}")
            # We still continue with creation even if there are validation errors
        
        # Create PersonaModern instance with enhanced data
        persona = PersonaModern(**enhanced_data)
        
        # Save to storage
        saved_persona = await storage.create_persona_modern(user_id, persona)
        
        return saved_persona
    
    except ValueError as e:
        # Missing API keys or validation errors
        error_msg = str(e)
        if "API_KEY" in error_msg or "api_key" in error_msg.lower():
            raise HTTPException(
                status_code=503,
                detail=f"Service temporarily unavailable: {error_msg}"
            )
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        print(f"Error creating modern persona: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create persona: {str(e)}"
        )

@router.get("", response_model=List[PersonaModern])
async def get_modern_personas(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    """Get all modern personas for a user"""
    # For development, always use default_user
    user_id = "default_user"
    
    try:
        personas = await storage.get_personas_modern(user_id)
        return personas
    except Exception as e:
        print(f"Error getting modern personas: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get personas: {str(e)}"
        )

@router.get("/{persona_id}", response_model=PersonaModern)
async def get_modern_persona(
    persona_id: str,
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    """Get a specific modern persona by ID"""
    try:
        persona = await storage.get_persona_modern(persona_id)
        if not persona:
            raise HTTPException(status_code=404, detail="Persona not found")
        
        # For development, skip authorization check
        # In production, uncomment this:
        # if user_id and persona.userId != user_id and user_id != "default_user":
        #     raise HTTPException(status_code=403, detail="Not authorized to access this persona")
        
        return persona
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting modern persona: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get persona: {str(e)}"
        )

@router.delete("/{persona_id}", status_code=204)
async def delete_modern_persona(
    persona_id: str,
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    """Delete a modern persona"""
    try:
        persona = await storage.get_persona_modern(persona_id)
        if not persona:
            raise HTTPException(status_code=404, detail="Persona not found")
        
        # For development, skip authorization check
        # In production, uncomment this:
        # if persona.userId != user_id and user_id != "default_user":
        #     raise HTTPException(status_code=403, detail="Not authorized to delete this persona")
        
        await storage.delete_persona_modern(persona_id)
        return None
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting modern persona: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete persona: {str(e)}"
        )
