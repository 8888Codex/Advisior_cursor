from typing import Dict, List, Optional
from datetime import datetime
import uuid
import asyncpg
import os
import json

from python_backend.models import (
    Expert, ExpertCreate, Conversation, ConversationCreate, 
    Message, MessageCreate, BusinessProfile, BusinessProfileCreate,
    CouncilAnalysis, Persona, User, UserPreferences, UserPreferencesUpdate
)
from python_backend.models_persona import PersonaModern

class PostgresStorage:
    """PostgreSQL storage implementation."""
    
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool = None

    async def connect(self):
        """Creates a connection pool."""
        if not self.pool:
            self.pool = await asyncpg.create_pool(self.dsn)
            print("Successfully connected to PostgreSQL.")
            # Initialize schema (create tables if they don't exist)
            await self._ensure_user_preferences_table()

    async def _ensure_user_preferences_table(self):
        """Ensure user_preferences table exists, create if not."""
        try:
            # Check if table exists
            check_query = """
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'user_preferences'
                );
            """
            exists_record = await self._fetchrow(check_query)
            exists = exists_record[0] if exists_record else False
            
            if not exists:
                # Create table
                create_table_query = """
                    CREATE TABLE IF NOT EXISTS user_preferences (
                        user_id VARCHAR(255) PRIMARY KEY,
                        style_preference VARCHAR(20) CHECK (style_preference IN ('objetivo', 'detalhado')),
                        focus_preference VARCHAR(20) CHECK (focus_preference IN ('ROI-first', 'brand-first')),
                        tone_preference VARCHAR(20) CHECK (tone_preference IN ('prático', 'estratégico')),
                        communication_preference VARCHAR(20) CHECK (communication_preference IN ('bullets', 'blocos')),
                        conversation_style VARCHAR(20) CHECK (conversation_style IN ('coach', 'consultor', 'direto')),
                        created_at TIMESTAMP DEFAULT NOW(),
                        updated_at TIMESTAMP DEFAULT NOW()
                    );
                    
                    CREATE INDEX IF NOT EXISTS idx_user_preferences_user_id ON user_preferences(user_id);
                    
                    CREATE OR REPLACE FUNCTION update_user_preferences_updated_at()
                    RETURNS TRIGGER AS $$
                    BEGIN
                        NEW.updated_at = NOW();
                        RETURN NEW;
                    END;
                    $$ LANGUAGE plpgsql;
                    
                    DROP TRIGGER IF EXISTS trigger_update_user_preferences_updated_at ON user_preferences;
                    CREATE TRIGGER trigger_update_user_preferences_updated_at
                        BEFORE UPDATE ON user_preferences
                        FOR EACH ROW
                        EXECUTE FUNCTION update_user_preferences_updated_at();
                """
                await self._execute(create_table_query)
                print("Created user_preferences table.")
            else:
                print("user_preferences table already exists.")
        except Exception as e:
            print(f"Warning: Could not ensure user_preferences table exists: {e}")
            # Don't raise, allow app to continue

    async def close(self):
        """Closes the connection pool."""
        if self.pool:
            await self.pool.close()
            print("PostgreSQL connection pool closed.")

    async def _execute(self, query: str, *args):
        """Helper to execute a query with connection management."""
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as connection:
            return await connection.execute(query, *args)

    async def _fetch(self, query: str, *args) -> List[asyncpg.Record]:
        """Helper to fetch multiple rows."""
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def _fetchrow(self, query: str, *args) -> Optional[asyncpg.Record]:
        """Helper to fetch a single row."""
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query, *args)

    # USER OPERATIONS (To be implemented)
    async def create_user(self, email: str, password_hash: str, name: Optional[str] = None) -> User:
        raise NotImplementedError

    async def get_user(self, user_id: str) -> Optional[User]:
        raise NotImplementedError

    async def get_user_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    # USER PREFERENCES OPERATIONS
    async def get_user_preferences(self, user_id: str) -> Optional[UserPreferences]:
        """Get user preferences by user ID."""
        record = await self._fetchrow(
            'SELECT * FROM user_preferences WHERE user_id = $1',
            user_id
        )
        if not record:
            return None
        
        return UserPreferences(
            user_id=record['user_id'],
            style_preference=record.get('style_preference'),
            focus_preference=record.get('focus_preference'),
            tone_preference=record.get('tone_preference'),
            communication_preference=record.get('communication_preference'),
            conversation_style=record.get('conversation_style'),
            created_at=record.get('created_at', datetime.utcnow()),
            updated_at=record.get('updated_at', datetime.utcnow())
        )
    
    async def save_user_preferences(self, user_id: str, preferences: UserPreferencesUpdate) -> UserPreferences:
        """Save or update user preferences."""
        # Check if preferences exist
        existing = await self.get_user_preferences(user_id)
        
        if existing:
            # Update existing preferences
            set_clauses = []
            values = []
            param_count = 1
            
            update_data = preferences.dict(exclude_unset=True)
            for key, value in update_data.items():
                if value is not None:
                    set_clauses.append(f'{key} = ${param_count}')
                    values.append(value)
                    param_count += 1
            
            if set_clauses:
                set_clauses.append('updated_at = NOW()')
                values.append(user_id)
                
                query = f"""
                    UPDATE user_preferences
                    SET {', '.join(set_clauses)}
                    WHERE user_id = ${param_count}
                    RETURNING *;
                """
                
                record = await self._fetchrow(query, *values)
            else:
                # No updates, just return existing
                record = await self._fetchrow(
                    'SELECT * FROM user_preferences WHERE user_id = $1',
                    user_id
                )
        else:
            # Create new preferences
            insert_data = preferences.dict(exclude_unset=True)
            columns = ['user_id'] + list(insert_data.keys())
            placeholders = ['$1'] + [f'${i+2}' for i in range(len(insert_data))]
            
            query = f"""
                INSERT INTO user_preferences ({', '.join(columns)}, created_at, updated_at)
                VALUES ({', '.join(placeholders)}, NOW(), NOW())
                RETURNING *;
            """
            
            values = [user_id] + list(insert_data.values())
            record = await self._fetchrow(query, *values)
        
        return UserPreferences(
            user_id=record['user_id'],
            style_preference=record.get('style_preference'),
            focus_preference=record.get('focus_preference'),
            tone_preference=record.get('tone_preference'),
            communication_preference=record.get('communication_preference'),
            conversation_style=record.get('conversation_style'),
            created_at=record.get('created_at', datetime.utcnow()),
            updated_at=record.get('updated_at', datetime.utcnow())
        )
    
    async def delete_user_preferences(self, user_id: str) -> bool:
        """Delete user preferences."""
        result = await self._execute(
            'DELETE FROM user_preferences WHERE user_id = $1',
            user_id
        )
        return result == "DELETE 1"

    # EXPERT OPERATIONS
    async def create_expert(self, data: ExpertCreate, expert_id: Optional[str] = None) -> Expert:
        """Creates an expert in the database."""
        if expert_id is None:
            expert_id = str(uuid.uuid4())
        
        query = """
            INSERT INTO experts (id, name, title, expertise, bio, "systemPrompt", avatar, "expertType", category)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            RETURNING *;
        """
        record = await self._fetchrow(
            query, expert_id, data.name, data.title, data.expertise, data.bio,
            data.systemPrompt, data.avatar, data.expertType.value, data.category.value
        )
        return Expert(**dict(record))

    async def get_expert(self, expert_id: str) -> Optional[Expert]:
        """Fetches a single expert by ID."""
        record = await self._fetchrow("SELECT * FROM experts WHERE id = $1", expert_id)
        return Expert(**dict(record)) if record else None

    async def get_experts(self) -> List[Expert]:
        """Fetches all experts from the database."""
        records = await self._fetch("SELECT * FROM experts ORDER BY name")
        return [Expert(**dict(record)) for record in records]
    
    async def update_expert_avatar(self, expert_id: str, avatar_path: str) -> Optional[Expert]:
        query = """
            UPDATE experts SET avatar = $2, "updatedAt" = NOW()
            WHERE id = $1 RETURNING *;
        """
        record = await self._fetchrow(query, expert_id, avatar_path)
        return Expert(**dict(record)) if record else None

    # CONVERSATION & MESSAGE OPERATIONS
    async def create_conversation(self, data: ConversationCreate) -> Conversation:
        """Creates a conversation in the database."""
        conversation_id = str(uuid.uuid4())
        query = """
            INSERT INTO conversations (id, "expertId", title, "createdAt", "updatedAt")
            VALUES ($1, $2, $3, NOW(), NOW())
            RETURNING *;
        """
        record = await self._fetchrow(query, conversation_id, data.expertId, data.title)
        return Conversation(**dict(record))

    async def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Fetches a single conversation by ID."""
        record = await self._fetchrow("SELECT * FROM conversations WHERE id = $1", conversation_id)
        return Conversation(**dict(record)) if record else None

    async def get_conversations(self, expert_id: Optional[str] = None) -> List[Conversation]:
        """Fetches conversations, optionally filtered by expert."""
        if expert_id:
            records = await self._fetch(
                'SELECT * FROM conversations WHERE "expertId" = $1 ORDER BY "updatedAt" DESC',
                expert_id
            )
        else:
            records = await self._fetch('SELECT * FROM conversations ORDER BY "updatedAt" DESC')
        return [Conversation(**dict(record)) for record in records]

    async def create_message(self, data: MessageCreate) -> Message:
        """Creates a message in the database."""
        message_id = str(uuid.uuid4())
        query = """
            INSERT INTO messages (id, "conversationId", role, content, "createdAt")
            VALUES ($1, $2, $3, $4, NOW())
            RETURNING *;
        """
        record = await self._fetchrow(query, message_id, data.conversationId, data.role, data.content)
        
        # Update conversation's updatedAt timestamp
        await self._execute(
            'UPDATE conversations SET "updatedAt" = NOW() WHERE id = $1',
            data.conversationId
        )
        
        return Message(**dict(record))

    async def get_messages(self, conversation_id: str) -> List[Message]:
        """Fetches all messages for a conversation."""
        records = await self._fetch(
            'SELECT * FROM messages WHERE "conversationId" = $1 ORDER BY "createdAt" ASC',
            conversation_id
        )
        return [Message(**dict(record)) for record in records]

    # BUSINESS PROFILE OPERATIONS
    async def save_business_profile(self, user_id: str, data: BusinessProfileCreate) -> BusinessProfile:
        """Saves or updates a business profile."""
        # For now, return None - to be implemented when we add business_profiles table
        raise NotImplementedError

    async def get_business_profile(self, user_id: str) -> Optional[BusinessProfile]:
        """Gets a business profile for a user."""
        # For now, return None - profiles will be implemented later
        # This allows the chat to work without profiles
        return None
        
    # COUNCIL ANALYSIS & PERSONA OPERATIONS
    async def save_council_analysis(self, analysis: CouncilAnalysis) -> CouncilAnalysis:
        # To be implemented when council analysis table is created
        raise NotImplementedError

    async def get_council_analysis(self, analysis_id: str) -> Optional[CouncilAnalysis]:
        raise NotImplementedError

    async def get_council_analyses(self, user_id: str) -> List[CouncilAnalysis]:
        raise NotImplementedError
        
    async def create_persona(self, user_id: str, persona_data: dict) -> Persona:
        """Creates a persona in the database."""
        persona_id = str(uuid.uuid4())
        
        query = """
            INSERT INTO personas (
                id, "userId", name, "researchMode", demographics, psychographics,
                "painPoints", goals, values, "contentPreferences", communities,
                "behavioralPatterns", "researchData", "createdAt", "updatedAt"
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, NOW(), NOW())
            RETURNING *;
        """
        
        # Prepare data with defaults
        record = await self._fetchrow(
            query,
            persona_id,
            user_id,
            persona_data.get("name", ""),
            persona_data.get("researchMode", "quick"),
            json.dumps(persona_data.get("demographics", {})),
            json.dumps(persona_data.get("psychographics", {})),
            persona_data.get("painPoints", []),
            persona_data.get("goals", []),
            persona_data.get("values", []),
            json.dumps(persona_data.get("contentPreferences", {})),
            persona_data.get("communities", []),
            json.dumps(persona_data.get("behavioralPatterns", {})),
            json.dumps(persona_data.get("researchData", {}))
        )
        
        # Convert record to Persona model
        persona_dict = dict(record)
        
        # Parse JSONB fields from string to dict
        for json_field in ['demographics', 'psychographics', 'contentPreferences', 'behavioralPatterns', 'researchData']:
            if json_field in persona_dict and isinstance(persona_dict[json_field], str):
                persona_dict[json_field] = json.loads(persona_dict[json_field])
        
        return Persona(**persona_dict)
        
    async def get_persona(self, persona_id: str) -> Optional[Persona]:
        """Fetches a single persona by ID."""
        record = await self._fetchrow("SELECT * FROM personas WHERE id = $1", persona_id)
        if not record:
            return None
        
        persona_dict = dict(record)
        # Parse JSONB fields from string to dict
        for json_field in ['demographics', 'psychographics', 'contentPreferences', 'behavioralPatterns', 'researchData']:
            if json_field in persona_dict and isinstance(persona_dict[json_field], str):
                persona_dict[json_field] = json.loads(persona_dict[json_field])
        
        return Persona(**persona_dict)
        
    async def get_personas(self, user_id: str) -> List[Persona]:
        """Fetches all personas for a user."""
        records = await self._fetch(
            'SELECT * FROM personas WHERE "userId" = $1 ORDER BY "createdAt" DESC',
            user_id
        )
        
        personas = []
        for record in records:
            persona_dict = dict(record)
            # Parse JSONB fields from string to dict
            for json_field in ['demographics', 'psychographics', 'contentPreferences', 'behavioralPatterns', 'researchData']:
                if json_field in persona_dict and isinstance(persona_dict[json_field], str):
                    persona_dict[json_field] = json.loads(persona_dict[json_field])
            personas.append(Persona(**persona_dict))
        
        return personas
        
    async def update_persona(self, persona_id: str, updates: dict) -> Optional[Persona]:
        """Updates a persona."""
        # Build dynamic update query
        set_clauses = []
        values = []
        param_count = 1
        
        for key, value in updates.items():
            if key in ["demographics", "psychographics", "contentPreferences", "behavioralPatterns", "researchData"]:
                set_clauses.append(f'"{key}" = ${param_count}')
                values.append(json.dumps(value))
            elif key in ["painPoints", "goals", "values", "communities"]:
                set_clauses.append(f'"{key}" = ${param_count}')
                values.append(value)
            else:
                set_clauses.append(f'"{key}" = ${param_count}')
                values.append(value)
            param_count += 1
        
        set_clauses.append(f'"updatedAt" = NOW()')
        values.append(persona_id)
        
        query = f"""
            UPDATE personas
            SET {', '.join(set_clauses)}
            WHERE id = ${param_count}
            RETURNING *;
        """
        
        record = await self._fetchrow(query, *values)
        if not record:
            return None
        
        persona_dict = dict(record)
        # Parse JSONB fields from string to dict
        for json_field in ['demographics', 'psychographics', 'contentPreferences', 'behavioralPatterns', 'researchData']:
            if json_field in persona_dict and isinstance(persona_dict[json_field], str):
                persona_dict[json_field] = json.loads(persona_dict[json_field])
        
        return Persona(**persona_dict)
        
    async def delete_persona(self, persona_id: str) -> bool:
        """Deletes a persona."""
        result = await self._execute("DELETE FROM personas WHERE id = $1", persona_id)
        return result == "DELETE 1"
    
    # PERSONA MODERN OPERATIONS (JTBD + BAG)
    async def create_persona_modern(self, user_id: str, persona: PersonaModern) -> PersonaModern:
        """Creates a modern persona using JTBD + BAG frameworks."""
        query = """
            INSERT INTO personas (
                id, "userId", name, "researchMode",
                "jobStatement", "situationalContexts", "functionalJobs", "emotionalJobs", "socialJobs",
                behaviors, aspirations, goals,
                "painPointsQuantified", "decisionCriteria",
                demographics, values,
                touchpoints, "contentPreferences", communities,
                "researchData", "createdAt", "updatedAt"
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, NOW(), NOW())
            RETURNING *;
        """
        
        # Convert PersonaModern to database format
        record = await self._fetchrow(
            query,
            persona.id,
            persona.userId,
            persona.name,
            persona.researchMode,
            persona.job_statement,
            persona.situational_contexts,
            persona.functional_jobs,
            persona.emotional_jobs,
            persona.social_jobs,
            json.dumps(persona.behaviors),
            persona.aspirations,
            persona.goals,
            json.dumps([p.dict() for p in persona.pain_points_quantified]),
            json.dumps(persona.decision_criteria),
            json.dumps(persona.demographics.dict()),
            persona.values,
            json.dumps([t.dict() for t in persona.touchpoints]),
            json.dumps(persona.content_preferences.dict()),
            json.dumps([c.dict() for c in persona.communities]),
            json.dumps(persona.research_data.dict())
        )
        
        return self._parse_persona_modern_record(record)
    
    async def get_persona_modern(self, persona_id: str) -> Optional[PersonaModern]:
        """Fetches a modern persona by ID."""
        record = await self._fetchrow("SELECT * FROM personas WHERE id = $1", persona_id)
        if not record:
            return None
        return self._parse_persona_modern_record(record)
    
    async def get_personas_modern(self, user_id: str) -> List[PersonaModern]:
        """Fetches all modern personas for a user."""
        records = await self._fetch(
            'SELECT * FROM personas WHERE "userId" = $1 ORDER BY "createdAt" DESC',
            user_id
        )
        return [self._parse_persona_modern_record(record) for record in records]
    
    async def update_persona_modern(self, persona_id: str, updates: dict) -> Optional[PersonaModern]:
        """Updates a modern persona."""
        # Similar logic to update_persona but for PersonaModern
        set_clauses = []
        values = []
        param_count = 1
        
        for key, value in updates.items():
            if key in ["behaviors", "painPointsQuantified", "decisionCriteria", "demographics", 
                      "touchpoints", "contentPreferences", "communities", "researchData"]:
                set_clauses.append(f'"{key}" = ${param_count}')
                values.append(json.dumps(value))
            elif key in ["situationalContexts", "functionalJobs", "emotionalJobs", "socialJobs",
                        "aspirations", "goals", "values"]:
                set_clauses.append(f'"{key}" = ${param_count}')
                values.append(value)
            else:
                set_clauses.append(f'"{key}" = ${param_count}')
                values.append(value)
            param_count += 1
        
        set_clauses.append(f'"updatedAt" = NOW()')
        values.append(persona_id)
        
        query = f"""
            UPDATE personas
            SET {', '.join(set_clauses)}
            WHERE id = ${param_count}
            RETURNING *;
        """
        
        record = await self._fetchrow(query, *values)
        if not record:
            return None
        return self._parse_persona_modern_record(record)
    
    async def delete_persona_modern(self, persona_id: str) -> bool:
        """Deletes a modern persona."""
        result = await self._execute("DELETE FROM personas WHERE id = $1", persona_id)
        return result == "DELETE 1"
    
    def _parse_persona_modern_record(self, record: asyncpg.Record) -> PersonaModern:
        """Helper to parse a database record into PersonaModern."""
        from python_backend.models_persona import (
            Demographics, QuantifiedPain, Touchpoint, 
            Community, ContentPreferences, ResearchData
        )
        
        persona_dict = dict(record)
        
        # Parse JSONB fields
        if isinstance(persona_dict.get('behaviors'), str):
            persona_dict['behaviors'] = json.loads(persona_dict['behaviors'])
        
        if isinstance(persona_dict.get('painPointsQuantified'), str):
            pains = json.loads(persona_dict['painPointsQuantified'])
            persona_dict['pain_points_quantified'] = [QuantifiedPain(**p) for p in pains]
        else:
            persona_dict['pain_points_quantified'] = []
        
        if isinstance(persona_dict.get('decisionCriteria'), str):
            persona_dict['decision_criteria'] = json.loads(persona_dict['decisionCriteria'])
        
        if isinstance(persona_dict.get('demographics'), str):
            persona_dict['demographics'] = Demographics(**json.loads(persona_dict['demographics']))
        
        if isinstance(persona_dict.get('touchpoints'), str):
            touchpoints = json.loads(persona_dict['touchpoints'])
            persona_dict['touchpoints'] = [Touchpoint(**t) for t in touchpoints]
        else:
            persona_dict['touchpoints'] = []
        
        if isinstance(persona_dict.get('contentPreferences'), str):
            persona_dict['content_preferences'] = ContentPreferences(**json.loads(persona_dict['contentPreferences']))
        
        if isinstance(persona_dict.get('communities'), str):
            communities = json.loads(persona_dict['communities'])
            persona_dict['communities'] = [Community(**c) for c in communities]
        else:
            persona_dict['communities'] = []
        
        if isinstance(persona_dict.get('researchData'), str):
            persona_dict['research_data'] = ResearchData(**json.loads(persona_dict['researchData']))
        
        # Map database snake_case to Python snake_case expected by Pydantic
        persona_dict['created_at'] = persona_dict.pop('createdAt', persona_dict.get('created_at'))
        persona_dict['updated_at'] = persona_dict.pop('updatedAt', persona_dict.get('updated_at'))
        persona_dict['userId'] = persona_dict.get('userId')
        persona_dict['researchMode'] = persona_dict.get('researchMode')
        persona_dict['job_statement'] = persona_dict.pop('jobStatement', '')
        persona_dict['situational_contexts'] = persona_dict.pop('situationalContexts', [])
        persona_dict['functional_jobs'] = persona_dict.pop('functionalJobs', [])
        persona_dict['emotional_jobs'] = persona_dict.pop('emotionalJobs', [])
        persona_dict['social_jobs'] = persona_dict.pop('socialJobs', [])
        
        return PersonaModern(**persona_dict)
