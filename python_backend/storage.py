from typing import Dict, List, Optional
from datetime import datetime
import uuid
from python_backend.models import (
    Expert, ExpertCreate, Conversation, ConversationCreate, 
    Message, MessageSend, ExpertType, CategoryType,
    CouncilAnalysis, Persona, User, UserPreferences, UserPreferencesUpdate
)

# Import modern persona storage
# from storage_persona_modern import PersonaModernStorage
from python_backend.models_persona import PersonaModern
import os
import json
from datetime import datetime as dt
import asyncpg

from python_backend.postgres_storage import PostgresStorage

class MemStorage:
    """In-memory storage for development and testing."""
    
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MemStorage, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.users: Dict[str, User] = {}
            self.user_emails: Dict[str, str] = {}
            self.experts: Dict[str, Expert] = {}
            self.conversations: Dict[str, Conversation] = {}
            self.messages: Dict[str, Message] = {}
            self.profiles: Dict[str, dict] = {}
            self.council_analyses: Dict[str, CouncilAnalysis] = {}
            self.personas: Dict[str, Persona] = {}
            self.user_preferences: Dict[str, UserPreferences] = {}  # user_id -> preferences
            # self._persona_modern_storage = PersonaModernStorage()
            self._initialized = True
            # Reset flag on initialization - seed will check actual data
            self._legends_seeded = False
            print("Initialized in-memory storage (MemStorage).")
    
    # =============================================================================
    # USER OPERATIONS
    # =============================================================================
    
    async def create_user(self, email: str, password_hash: str, name: Optional[str] = None) -> User:
        """Create a new user"""
        user_id = str(uuid.uuid4())
        user = User(
            id=user_id,
            email=email,
            password=password_hash,  # Already hashed
            name=name
        )
        self.users[user_id] = user
        self.user_emails[email.lower()] = user_id
        return user
    
    async def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self.users.get(user_id)
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        user_id = self.user_emails.get(email.lower())
        if user_id:
            return self.users.get(user_id)
        return None
    
    async def update_user(self, user_id: str, **updates) -> Optional[User]:
        """Update user fields"""
        user = self.users.get(user_id)
        if not user:
            return None
        
        for key, value in updates.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        
        user.updated_at = datetime.utcnow()
        return user
    
    # =============================================================================
    # USER PREFERENCES OPERATIONS
    # =============================================================================
    
    async def get_user_preferences(self, user_id: str) -> Optional[UserPreferences]:
        """Get user preferences by user ID"""
        return self.user_preferences.get(user_id)
    
    async def save_user_preferences(self, user_id: str, preferences: UserPreferencesUpdate) -> UserPreferences:
        """Save or update user preferences"""
        existing = self.user_preferences.get(user_id)
        
        if existing:
            # Update existing preferences
            update_data = preferences.dict(exclude_unset=True)
            for key, value in update_data.items():
                if value is not None:
                    setattr(existing, key, value)
            existing.updated_at = datetime.utcnow()
            return existing
        else:
            # Create new preferences
            new_prefs = UserPreferences(
                user_id=user_id,
                **preferences.dict(exclude_unset=True)
            )
            self.user_preferences[user_id] = new_prefs
            return new_prefs
    
    async def delete_user_preferences(self, user_id: str) -> bool:
        """Delete user preferences"""
        if user_id in self.user_preferences:
            del self.user_preferences[user_id]
            return True
        return False
    
    # =============================================================================
    # EXPERT OPERATIONS
    # =============================================================================
    
    async def create_expert(self, data: ExpertCreate, expert_id: Optional[str] = None) -> Expert:
        if expert_id is None:
            expert_id = str(uuid.uuid4())
            
        expert = Expert(
            id=expert_id, name=data.name, title=data.title, bio=data.bio,
            expertise=data.expertise, systemPrompt=data.systemPrompt, avatar=data.avatar,
            expertType=data.expertType, category=data.category
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
    async def create_message(self, data: MessageSend) -> Message:
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
    
    # Council Conversation operations
    async def create_council_conversation(self, user_id: str, persona_id: str, problem: str, expert_ids: List[str], analysis_id: Optional[str] = None) -> 'CouncilConversation':
        """Create a new council conversation"""
        from python_backend.models import CouncilConversation
        import uuid
        
        conversation_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        if not hasattr(self, 'council_conversations'):
            self.council_conversations = {}
        
        conversation = CouncilConversation(
            id=conversation_id,
            userId=user_id,
            personaId=persona_id,
            problem=problem,
            expertIds=expert_ids,
            analysisId=analysis_id,
            createdAt=now,
            updatedAt=now
        )
        self.council_conversations[conversation_id] = conversation
        return conversation
    
    async def get_council_conversation(self, conversation_id: str) -> Optional['CouncilConversation']:
        """Get a council conversation by ID"""
        if not hasattr(self, 'council_conversations'):
            return None
        return self.council_conversations.get(conversation_id)
    
    async def get_council_conversations(self, user_id: Optional[str] = None) -> List['CouncilConversation']:
        """Get all council conversations, optionally filtered by user"""
        from python_backend.models import CouncilConversation
        
        if not hasattr(self, 'council_conversations'):
            return []
        
        conversations = list(self.council_conversations.values())
        if user_id:
            conversations = [c for c in conversations if c.userId == user_id]
        conversations.sort(key=lambda x: x.updatedAt, reverse=True)
        return conversations
    
    async def create_council_message(self, conversation_id: str, role: str, content: str, expert_id: Optional[str] = None, expert_name: Optional[str] = None) -> 'CouncilMessage':
        """Create a message in a council conversation"""
        from python_backend.models import CouncilMessage
        import uuid
        
        message_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        if not hasattr(self, 'council_messages'):
            self.council_messages = {}
        
        message = CouncilMessage(
            id=message_id,
            conversationId=conversation_id,
            expertId=expert_id,
            expertName=expert_name,
            content=content,
            role=role,
            timestamp=now,
            reactions=[]
        )
        self.council_messages[message_id] = message
        
        # Update conversation timestamp
        if hasattr(self, 'council_conversations'):
            if conversation_id in self.council_conversations:
                self.council_conversations[conversation_id].updatedAt = now
        
        return message
    
    async def get_council_messages(self, conversation_id: str) -> List['CouncilMessage']:
        """Get all messages for a council conversation"""
        from python_backend.models import CouncilMessage
        
        if not hasattr(self, 'council_messages'):
            return []
        
        messages = [m for m in self.council_messages.values() if m.conversationId == conversation_id]
        messages.sort(key=lambda x: x.timestamp)
        return messages
    
    async def add_council_message_reaction(self, message_id: str, reaction: 'MessageReaction') -> bool:
        """Add a reaction to a council message"""
        from python_backend.models import MessageReaction
        
        if not hasattr(self, 'council_messages'):
            return False
        
        if message_id not in self.council_messages:
            return False
        
        message = self.council_messages[message_id]
        message.reactions.append(reaction)
        return True
    
    # Business Profile operations - TEMPORARILY DISABLED
    async def save_business_profile(self, user_id: str, data: dict) -> dict:
        """Create or update business profile for a user"""
        # Temporarily return empty dict - profiles not implemented yet
        return {}
    
    async def get_business_profile(self, user_id: str) -> Optional[dict]:
        """Get business profile for a user"""
        # Temporarily return None - profiles not implemented yet
        return None
    
    # Council Analysis operations
    async def save_council_analysis(self, analysis: CouncilAnalysis) -> CouncilAnalysis:
        """Save a completed council analysis"""
        self.council_analyses[analysis.id] = analysis
        return analysis
    
    async def get_council_analysis(self, analysis_id: str) -> Optional[CouncilAnalysis]:
        """Get a specific council analysis"""
        return self.council_analyses.get(analysis_id)
    
    async def get_council_analyses(self, user_id: str) -> List[CouncilAnalysis]:
        """Get all council analyses for a user"""
        analyses = [a for a in self.council_analyses.values() if a.userId == user_id]
        # Sort by createdAt descending (most recent first)
        analyses.sort(key=lambda x: x.createdAt, reverse=True)
        return analyses
    
    # Persona operations (PostgreSQL)
    async def _get_db_connection(self):
        """Get PostgreSQL connection from DATABASE_URL"""
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable not set")
        return await asyncpg.connect(database_url)
    
    async def create_persona(self, user_id: str, persona_data: dict) -> Persona:
        """Create a new persona (temporary in-memory version)"""
        try:
            # Inicializar dicionário de personas se não existir
            if not hasattr(self, 'personas'):
                self.personas = {}
            
            # Gerar ID único
            persona_id = str(uuid.uuid4())
            now = datetime.utcnow()
            
            # Criar objeto Persona
            persona = Persona(
                id=persona_id,
                userId=user_id,
                name=persona_data.get('name', 'Unnamed Persona'),
                researchMode=persona_data.get('researchMode', 'quick'),
                
                # Research data
                demographics=persona_data.get('demographics', {}),
                psychographics=persona_data.get('psychographics', {}),
                painPoints=persona_data.get('painPoints', []),
                goals=persona_data.get('goals', []),
                values=persona_data.get('values', []),
                contentPreferences=persona_data.get('contentPreferences', {}),
                communities=persona_data.get('communities', []),
                behavioralPatterns=persona_data.get('behavioralPatterns', {}),
                
                # Full research data
                researchData=persona_data.get('researchData', {}),
                
                # Timestamps
                createdAt=now.isoformat(),
                updatedAt=now.isoformat()
            )
            
            # Armazenar em memória (temporário até migração para PostgreSQL)
            self.personas[persona_id] = persona
            
            print(f"[INFO] Persona criada em memória: {persona_id}")
            return persona
            
        except Exception as e:
            print(f"[ERROR] Erro ao criar persona: {str(e)}")
            raise
    
    async def get_persona(self, persona_id: str) -> Optional[Persona]:
        """Get a specific persona by ID (temporary in-memory version)"""
        try:
            # Verificar se o dicionário de personas existe
            if not hasattr(self, 'personas'):
                self.personas = {}
            
            # Retornar persona do dicionário se existir
            return self.personas.get(persona_id)
        except Exception as e:
            print(f"[ERROR] Erro ao buscar persona: {str(e)}")
            return None
    
    async def get_personas(self, user_id: str) -> List[Persona]:
        """Get all personas for a user (temporary in-memory version)"""
        try:
            # Verificar se o dicionário de personas existe
            if not hasattr(self, 'personas'):
                self.personas = {}
            
            # Filtrar personas pelo user_id
            personas = [
                persona for persona in self.personas.values()
                if persona.userId == user_id
            ]
            
            # Ordenar por data de criação (mais recentes primeiro)
            personas.sort(key=lambda p: p.createdAt, reverse=True)
            
            return personas
        except Exception as e:
            print(f"[ERROR] Erro ao listar personas: {str(e)}")
            return []
    
    # =============================================================================
    # MODERN PERSONA OPERATIONS - Delegate to PersonaModernStorage
    # =============================================================================
    
    async def create_persona_modern(self, user_id: str, persona: PersonaModern) -> PersonaModern:
        """Create a new modern persona"""
        return await self._persona_modern_storage.create_persona_modern(user_id, persona)
    
    async def get_persona_modern(self, persona_id: str) -> Optional[PersonaModern]:
        """Get a specific modern persona by ID"""
        return await self._persona_modern_storage.get_persona_modern(persona_id)
    
    async def get_personas_modern(self, user_id: str) -> List[PersonaModern]:
        """Get all modern personas for a user"""
        return await self._persona_modern_storage.get_personas_modern(user_id)
    
    async def update_persona_modern(self, persona_id: str, updates: dict) -> Optional[PersonaModern]:
        """Update a modern persona"""
        return await self._persona_modern_storage.update_persona_modern(persona_id, updates)
    
    async def delete_persona_modern(self, persona_id: str) -> bool:
        """Delete a modern persona"""
        return await self._persona_modern_storage.delete_persona_modern(persona_id)
    
    async def update_persona(self, persona_id: str, updates: dict) -> Optional[Persona]:
        """Update a persona"""
        conn = await self._get_db_connection()
        try:
            now = datetime.utcnow()
            
            # Build dynamic UPDATE query based on provided fields
            set_clauses = ["updated_at = $1"]
            params = [now]
            param_num = 2
            
            field_mapping = {
                "name": "name",
                "demographics": "demographics",
                "psychographics": "psychographics",
                "painPoints": "pain_points",
                "goals": "goals",
                "values": "values",
                "contentPreferences": "content_preferences",
                "communities": "communities",
                "behavioralPatterns": "behavioral_patterns",
                "researchData": "research_data"
            }
            
            for field_camel, field_snake in field_mapping.items():
                if field_camel in updates:
                    value = updates[field_camel]
                    # JSON fields need to be stringified
                    if field_snake in ["demographics", "psychographics", "content_preferences", "behavioral_patterns", "research_data"]:
                        value = json.dumps(value)
                    
                    set_clauses.append(f"{field_snake} = ${param_num}")
                    params.append(value)
                    param_num += 1
            
            params.append(persona_id)
            query = f"UPDATE personas SET {', '.join(set_clauses)} WHERE id = ${param_num} RETURNING *"
            
            row = await conn.fetchrow(query, *params)
            if not row:
                return None
            
            return Persona(
                id=str(row["id"]),  # Convert UUID to string
                userId=row["user_id"],
                name=row["name"],
                researchMode=row["research_mode"],
                demographics=json.loads(row["demographics"]) if row["demographics"] else {},
                psychographics=json.loads(row["psychographics"]) if row["psychographics"] else {},
                painPoints=list(row["pain_points"]) if row["pain_points"] else [],
                goals=list(row["goals"]) if row["goals"] else [],
                values=list(row["values"]) if row["values"] else [],
                contentPreferences=json.loads(row["content_preferences"]) if row["content_preferences"] else {},
                communities=list(row["communities"]) if row["communities"] else [],
                behavioralPatterns=json.loads(row["behavioral_patterns"]) if row["behavioral_patterns"] else {},
                researchData=json.loads(row["research_data"]) if row["research_data"] else {},
                createdAt=row["created_at"].isoformat() if hasattr(row["created_at"], 'isoformat') else str(row["created_at"]),
                updatedAt=row["updated_at"].isoformat() if hasattr(row["updated_at"], 'isoformat') else str(row["updated_at"])
            )
        finally:
            await conn.close()
    
    async def delete_persona(self, persona_id: str) -> bool:
        """Delete a persona"""
        conn = await self._get_db_connection()
        try:
            result = await conn.execute("DELETE FROM personas WHERE id = $1", persona_id)
            return result == "DELETE 1"
        finally:
            await conn.close()


def get_storage_instance():
    """
    Factory function to get the appropriate storage instance.
    - If DATABASE_URL is set, it returns a PostgresStorage instance.
    - Otherwise, it returns a singleton MemStorage instance.
    """
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        print("DATABASE_URL found. Initializing PostgresStorage.")
        return PostgresStorage(dsn=database_url)
    else:
        print("DATABASE_URL not found. Using in-memory storage (MemStorage).")
        return MemStorage()

# Global storage instance, determined at startup.
storage = get_storage_instance()
