from typing import Dict, List, Optional
from datetime import datetime
import uuid
from models import (
    Expert, ExpertCreate, Conversation, ConversationCreate, 
    Message, MessageCreate, ExpertType, BusinessProfile, BusinessProfileCreate
)

class MemStorage:
    """In-memory storage compatible with frontend API expectations"""
    
    def __init__(self):
        self.experts: Dict[str, Expert] = {}
        self.conversations: Dict[str, Conversation] = {}
        self.messages: Dict[str, Message] = {}
        self.profiles: Dict[str, BusinessProfile] = {}  # userId -> BusinessProfile
    
    # Expert operations
    async def create_expert(self, data: ExpertCreate) -> Expert:
        expert_id = str(uuid.uuid4())
        expert = Expert(
            id=expert_id,
            name=data.name,
            title=data.title,
            bio=data.bio,
            expertise=data.expertise,
            systemPrompt=data.systemPrompt,
            avatar=data.avatar,
            expertType=data.expertType,
        )
        self.experts[expert_id] = expert
        return expert
    
    async def get_expert(self, expert_id: str) -> Optional[Expert]:
        return self.experts.get(expert_id)
    
    async def get_experts(self) -> List[Expert]:
        return list(self.experts.values())
    
    async def update_expert_avatar(self, expert_id: str, avatar_path: str) -> Optional[Expert]:
        """Update expert's avatar path"""
        expert = self.experts.get(expert_id)
        if expert:
            expert.avatar = avatar_path
            return expert
        return None
    
    # Conversation operations
    async def create_conversation(self, data: ConversationCreate) -> Conversation:
        conversation_id = str(uuid.uuid4())
        conversation = Conversation(
            id=conversation_id,
            expertId=data.expertId,
            title=data.title,
        )
        self.conversations[conversation_id] = conversation
        return conversation
    
    async def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        return self.conversations.get(conversation_id)
    
    async def get_conversations(self, expert_id: Optional[str] = None) -> List[Conversation]:
        conversations = list(self.conversations.values())
        if expert_id:
            conversations = [c for c in conversations if c.expertId == expert_id]
        # Sort by updatedAt descending
        conversations.sort(key=lambda x: x.updatedAt, reverse=True)
        return conversations
    
    async def update_conversation_timestamp(self, conversation_id: str):
        if conversation_id in self.conversations:
            self.conversations[conversation_id].updatedAt = datetime.utcnow()
    
    # Message operations
    async def create_message(self, data: MessageCreate) -> Message:
        message_id = str(uuid.uuid4())
        message = Message(
            id=message_id,
            conversationId=data.conversationId,
            role=data.role,
            content=data.content,
        )
        self.messages[message_id] = message
        
        # Update conversation timestamp
        await self.update_conversation_timestamp(data.conversationId)
        
        return message
    
    async def get_messages(self, conversation_id: str) -> List[Message]:
        messages = [m for m in self.messages.values() if m.conversationId == conversation_id]
        # Sort by createdAt ascending (chronological order)
        messages.sort(key=lambda x: x.createdAt)
        return messages
    
    # Business Profile operations
    async def save_business_profile(self, user_id: str, data: BusinessProfileCreate) -> BusinessProfile:
        """Create or update business profile for a user"""
        existing_profile = self.profiles.get(user_id)
        
        if existing_profile:
            # Update existing profile
            profile = BusinessProfile(
                id=existing_profile.id,
                userId=user_id,
                companyName=data.companyName,
                industry=data.industry,
                companySize=data.companySize,
                targetAudience=data.targetAudience,
                mainProducts=data.mainProducts,
                channels=data.channels,
                budgetRange=data.budgetRange,
                primaryGoal=data.primaryGoal,
                mainChallenge=data.mainChallenge,
                timeline=data.timeline,
                createdAt=existing_profile.createdAt,
                updatedAt=datetime.utcnow()
            )
        else:
            # Create new profile
            profile_id = str(uuid.uuid4())
            profile = BusinessProfile(
                id=profile_id,
                userId=user_id,
                companyName=data.companyName,
                industry=data.industry,
                companySize=data.companySize,
                targetAudience=data.targetAudience,
                mainProducts=data.mainProducts,
                channels=data.channels,
                budgetRange=data.budgetRange,
                primaryGoal=data.primaryGoal,
                mainChallenge=data.mainChallenge,
                timeline=data.timeline
            )
        
        self.profiles[user_id] = profile
        return profile
    
    async def get_business_profile(self, user_id: str) -> Optional[BusinessProfile]:
        """Get business profile for a user"""
        return self.profiles.get(user_id)

# Global storage instance
storage = MemStorage()
