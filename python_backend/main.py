from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
import os
import shutil
from pathlib import Path
from PIL import Image
import io

from models import (
    Expert, ExpertCreate, ExpertType,
    Conversation, ConversationCreate,
    Message, MessageCreate, MessageSend, MessageResponse,
    BusinessProfile, BusinessProfileCreate
)
from storage import storage
from crew_agent import LegendAgentFactory
from seed import seed_legends

app = FastAPI(title="AdvisorIA - Marketing Legends API")

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize with seeded legends
@app.on_event("startup")
async def startup_event():
    print("Seeding marketing legends...")
    await seed_legends(storage)
    print(f"Seeded {len(await storage.get_experts())} marketing legends successfully.")

# Health check
@app.get("/")
async def root():
    return {"message": "AdvisorIA Marketing Legends API", "status": "running"}

# Expert endpoints
@app.get("/api/experts", response_model=List[Expert])
async def get_experts():
    """Get all marketing legend experts"""
    return await storage.get_experts()

@app.get("/api/experts/{expert_id}", response_model=Expert)
async def get_expert(expert_id: str):
    """Get a specific expert by ID"""
    expert = await storage.get_expert(expert_id)
    if not expert:
        raise HTTPException(status_code=404, detail="Expert not found")
    return expert

@app.post("/api/experts", response_model=Expert, status_code=201)
async def create_expert(data: ExpertCreate):
    """Create a new custom expert (cognitive clone)"""
    try:
        expert = await storage.create_expert(data)
        return expert
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create expert: {str(e)}")

@app.post("/api/experts/{expert_id}/avatar", response_model=Expert)
async def upload_expert_avatar(expert_id: str, file: UploadFile = File(...)):
    """Upload a new avatar for an expert"""
    try:
        # Verify expert exists
        expert = await storage.get_expert(expert_id)
        if not expert:
            raise HTTPException(status_code=404, detail="Expert not found")
        
        # Validate file type
        allowed_types = ["image/png", "image/jpeg", "image/jpg", "image/webp"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed types: PNG, JPG, WEBP"
            )
        
        # Read and validate file size (max 5MB)
        max_size = 5 * 1024 * 1024  # 5MB
        contents = await file.read()
        if len(contents) > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size is 5MB."
            )
        
        # Validate file is actually an image using Pillow
        # This prevents malicious files disguised as images
        try:
            image = Image.open(io.BytesIO(contents))
            image.verify()  # Verify it's a valid image
            
            # Re-open for processing (verify() invalidates the image)
            image = Image.open(io.BytesIO(contents))
            
            # Validate image format matches expected types
            if not image.format or image.format.lower() not in ['png', 'jpeg', 'webp']:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid image format: {image.format or 'unknown'}. Allowed: PNG, JPEG, WEBP"
                )
            
            # Normalize extension based on ACTUAL detected format (not client-supplied)
            # This prevents mismatches between file extension and content
            format_to_ext = {
                'png': '.png',
                'jpeg': '.jpg',  # Canonical: always save as .jpg not .jpeg
                'webp': '.webp'
            }
            
            # Get extension with safe fallback for unknown formats
            detected_format = image.format.lower() if image.format else 'unknown'
            ext = format_to_ext.get(detected_format)
            
            if not ext:
                # Should never happen due to format validation above, but be defensive
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported image format after validation: {detected_format}"
                )
            
            # Optionally resize large images to prevent storage issues
            max_dimension = 2048
            if image.width > max_dimension or image.height > max_dimension:
                image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
            
            # Create avatars directory if it doesn't exist
            # Use absolute path to project root, not relative to python_backend
            project_root = Path(__file__).parent.parent
            avatars_dir = project_root / "attached_assets" / "avatars"
            avatars_dir.mkdir(parents=True, exist_ok=True)
            
            # Remove ALL old avatar files regardless of extension
            # Include .jpeg (legacy) even though we now save as .jpg
            for old_ext in [".png", ".jpg", ".jpeg", ".webp"]:
                old_file = avatars_dir / f"{expert_id}{old_ext}"
                if old_file.exists() and old_ext != ext:
                    old_file.unlink()
            
            # Save file with expert_id as filename
            file_path = avatars_dir / f"{expert_id}{ext}"
            
            # Save the validated and potentially resized image
            # This also strips any malicious metadata/payloads
            image.save(file_path, format=image.format, optimize=True)
            
        except Exception as img_error:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid image file: {str(img_error)}"
            )
        
        # Update expert's avatar path
        avatar_url = f"/attached_assets/avatars/{expert_id}{ext}"
        updated_expert = await storage.update_expert_avatar(expert_id, avatar_url)
        
        if not updated_expert:
            raise HTTPException(status_code=500, detail="Failed to update expert avatar")
        
        return updated_expert
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error uploading avatar: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to upload avatar: {str(e)}")
    finally:
        # Ensure file is closed
        await file.close()

# Conversation endpoints
@app.get("/api/conversations", response_model=List[Conversation])
async def get_conversations(expertId: Optional[str] = None):
    """Get conversations, optionally filtered by expert"""
    return await storage.get_conversations(expertId)

@app.get("/api/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: str):
    """Get a specific conversation"""
    conversation = await storage.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@app.post("/api/conversations", response_model=Conversation, status_code=201)
async def create_conversation(data: ConversationCreate):
    """Create a new conversation with an expert"""
    try:
        # Verify expert exists
        expert = await storage.get_expert(data.expertId)
        if not expert:
            raise HTTPException(status_code=404, detail="Expert not found")
        
        conversation = await storage.create_conversation(data)
        return conversation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create conversation: {str(e)}")

# Message endpoints
@app.get("/api/conversations/{conversation_id}/messages", response_model=List[Message])
async def get_messages(conversation_id: str):
    """Get all messages in a conversation"""
    messages = await storage.get_messages(conversation_id)
    return messages

@app.post("/api/conversations/{conversation_id}/messages", response_model=MessageResponse, status_code=201)
async def send_message(conversation_id: str, data: MessageSend):
    """Send a message and get AI response from the marketing legend"""
    try:
        # Validate conversation exists
        conversation = await storage.get_conversation(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Get expert
        expert = await storage.get_expert(conversation.expertId)
        if not expert:
            raise HTTPException(status_code=404, detail="Expert not found")
        
        # Get conversation history BEFORE saving the new user message
        # This way we pass all previous messages to the agent
        all_messages = await storage.get_messages(conversation_id)
        history = [
            {"role": msg.role, "content": msg.content}
            for msg in all_messages
        ]
        
        # Create agent for this expert
        agent = LegendAgentFactory.create_agent(
            expert_name=expert.name,
            system_prompt=expert.systemPrompt
        )
        
        # Get AI response (agent.chat will add the new user message to history)
        ai_response = await agent.chat(history, data.content)
        
        # Now save user message AFTER getting AI response
        user_message = await storage.create_message(MessageCreate(
            conversationId=conversation_id,
            role="user",
            content=data.content
        ))
        
        # Save assistant message
        assistant_message = await storage.create_message(MessageCreate(
            conversationId=conversation_id,
            role="assistant",
            content=ai_response
        ))
        
        return MessageResponse(
            userMessage=user_message,
            assistantMessage=assistant_message
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")

# Business Profile endpoints
@app.post("/api/profile", response_model=BusinessProfile)
async def save_profile(data: BusinessProfileCreate):
    """Create or update business profile"""
    # For now, use a default user_id until we add authentication
    user_id = "default_user"
    try:
        profile = await storage.save_business_profile(user_id, data)
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save profile: {str(e)}")

@app.get("/api/profile", response_model=Optional[BusinessProfile])
async def get_profile():
    """Get current user's business profile"""
    # For now, use a default user_id until we add authentication
    user_id = "default_user"
    profile = await storage.get_business_profile(user_id)
    return profile

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
