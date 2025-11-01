from typing import Dict, List, Optional
from datetime import datetime
import uuid
import asyncpg
import os
import json

from python_backend.models import (
    Expert, ExpertCreate, Conversation, ConversationCreate, 
    Message, MessageSend,
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
        from python_backend.models import ExpertType, CategoryType
        import asyncpg
        
        if expert_id is None:
            expert_id = str(uuid.uuid4())
        
        # Garantir que a tabela experts existe
        await self._ensure_experts_table()
        
        # Serializar expertise como JSON
        expertise_json = json.dumps(data.expertise) if isinstance(data.expertise, list) else data.expertise
        
        query = """
            INSERT INTO experts (id, name, title, expertise, bio, "systemPrompt", avatar, "expertType", category)
            VALUES ($1, $2, $3, $4::jsonb, $5, $6, $7, $8, $9)
            RETURNING *;
        """
        
        try:
            record = await self._fetchrow(
                query, expert_id, data.name, data.title, expertise_json, data.bio,
                data.systemPrompt, data.avatar, data.expertType.value, data.category.value
            )
        except asyncpg.exceptions.UndefinedTableError:
            # Tabela não existe, criar e tentar novamente
            await self._create_experts_table()
            record = await self._fetchrow(
                query, expert_id, data.name, data.title, expertise_json, data.bio,
                data.systemPrompt, data.avatar, data.expertType.value, data.category.value
            )
        
        # Convert record to dict and handle field name mapping
        expert_dict = dict(record)
        
        # Map database fields to Expert model fields
        mapped_dict = {
            "id": str(expert_dict.get("id", "")),
            "name": expert_dict.get("name", ""),
            "title": expert_dict.get("title", ""),
            "expertise": expert_dict.get("expertise", []),
            "bio": expert_dict.get("bio", ""),
            "systemPrompt": expert_dict.get("systemPrompt") or expert_dict.get("system_prompt", ""),
            "avatar": expert_dict.get("avatar"),
            "expertType": ExpertType(expert_dict.get("expertType") or expert_dict.get("expert_type", "high_fidelity")),
            "category": CategoryType(expert_dict.get("category", "marketing")),
            "createdAt": expert_dict.get("createdAt") or expert_dict.get("created_at") or datetime.utcnow()
        }
        
        return Expert(**mapped_dict)

    async def get_expert(self, expert_id: str) -> Optional[Expert]:
        """Fetches a single expert by ID."""
        from python_backend.models import ExpertType, CategoryType
        import asyncpg
        
        # Garantir que a tabela existe
        await self._ensure_experts_table()
        
        try:
            record = await self._fetchrow("SELECT * FROM experts WHERE id = $1", expert_id)
        except asyncpg.exceptions.UndefinedTableError:
            await self._create_experts_table()
            return None
            
        if not record:
            return None
        
        # Convert record to dict and handle field name mapping
        expert_dict = dict(record)
        
        # Parse expertise from JSON if needed
        expertise_data = expert_dict.get("expertise", [])
        if isinstance(expertise_data, str):
            try:
                expertise_data = json.loads(expertise_data)
            except:
                expertise_data = []
        elif expertise_data is None:
            expertise_data = []
        
        # Map database fields to Expert model fields
        # Handle both camelCase (quoted) and snake_case field names
        mapped_dict = {
            "id": str(expert_dict.get("id", "")),
            "name": expert_dict.get("name", ""),
            "title": expert_dict.get("title", ""),
            "expertise": expertise_data,
            "bio": expert_dict.get("bio", ""),
            "systemPrompt": expert_dict.get("systemPrompt") or expert_dict.get("system_prompt", ""),
            "avatar": expert_dict.get("avatar"),
            "expertType": ExpertType(expert_dict.get("expertType") or expert_dict.get("expert_type", "high_fidelity")),
            "category": CategoryType(expert_dict.get("category", "marketing")),
            "createdAt": expert_dict.get("createdAt") or expert_dict.get("created_at") or datetime.utcnow()
        }
        
        return Expert(**mapped_dict)

    async def _ensure_experts_table(self):
        """Ensure experts table exists, create if not."""
        try:
            check_query = """
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'experts'
                );
            """
            exists_record = await self._fetchrow(check_query)
            exists = exists_record[0] if exists_record else False
            
            if not exists:
                await self._create_experts_table()
        except Exception as e:
            print(f"[PostgresStorage] Warning checking experts table: {e}")
            # Try to create anyway
            try:
                await self._create_experts_table()
            except:
                pass
    
    async def _create_experts_table(self):
        """Create experts table if it doesn't exist"""
        query = """
            CREATE TABLE IF NOT EXISTS experts (
                id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                title VARCHAR(255) NOT NULL,
                expertise JSONB NOT NULL DEFAULT '[]'::jsonb,
                bio TEXT NOT NULL,
                "systemPrompt" TEXT NOT NULL,
                avatar VARCHAR(500),
                "expertType" VARCHAR(50) NOT NULL DEFAULT 'high_fidelity',
                category VARCHAR(50) NOT NULL DEFAULT 'marketing',
                "createdAt" TIMESTAMP NOT NULL DEFAULT NOW()
            );
        """
        await self._execute(query)
        print("[PostgresStorage] Created experts table.")

    async def get_experts(self) -> List[Expert]:
        """Fetches all experts from the database."""
        from python_backend.models import ExpertType, CategoryType
        import asyncpg
        
        # Garantir que a tabela existe
        await self._ensure_experts_table()
        
        try:
            records = await self._fetch("SELECT * FROM experts ORDER BY name")
        except asyncpg.exceptions.UndefinedTableError:
            # Tabela não existe, criar e retornar vazio
            await self._create_experts_table()
            return []
        
        experts = []
        for record in records:
            try:
                # Convert record to dict and handle field name mapping
                expert_dict = dict(record)
                
                # Parse expertise from JSON if needed
                expertise_data = expert_dict.get("expertise", [])
                if isinstance(expertise_data, str):
                    try:
                        expertise_data = json.loads(expertise_data)
                    except:
                        expertise_data = []
                elif expertise_data is None:
                    expertise_data = []
                
                # Map database fields to Expert model fields
                mapped_dict = {
                    "id": str(expert_dict.get("id", "")),
                    "name": expert_dict.get("name", ""),
                    "title": expert_dict.get("title", ""),
                    "expertise": expertise_data,
                    "bio": expert_dict.get("bio", ""),
                    "systemPrompt": expert_dict.get("systemPrompt") or expert_dict.get("system_prompt", ""),
                    "avatar": expert_dict.get("avatar"),
                    "expertType": ExpertType(expert_dict.get("expertType") or expert_dict.get("expert_type", "high_fidelity")),
                    "category": CategoryType(expert_dict.get("category", "marketing")),
                    "createdAt": expert_dict.get("createdAt") or expert_dict.get("created_at") or datetime.utcnow()
                }
                
                expert = Expert(**mapped_dict)
                experts.append(expert)
            except Exception as e:
                print(f"[PostgresStorage] Error converting expert record to Expert model: {e}")
                print(f"[PostgresStorage] Record data: {dict(record)}")
                import traceback
                traceback.print_exc()
                # Skip this expert and continue
                continue
        
        return experts
    
    async def update_expert_avatar(self, expert_id: str, avatar_path: str) -> Optional[Expert]:
        from python_backend.models import ExpertType, CategoryType
        query = """
            UPDATE experts SET avatar = $2, "updatedAt" = NOW()
            WHERE id = $1 RETURNING *;
        """
        record = await self._fetchrow(query, expert_id, avatar_path)
        if not record:
            return None
        
        # Convert record to dict and handle field name mapping
        expert_dict = dict(record)
        
        # Map database fields to Expert model fields
        mapped_dict = {
            "id": str(expert_dict.get("id", "")),
            "name": expert_dict.get("name", ""),
            "title": expert_dict.get("title", ""),
            "expertise": expert_dict.get("expertise", []),
            "bio": expert_dict.get("bio", ""),
            "systemPrompt": expert_dict.get("systemPrompt") or expert_dict.get("system_prompt", ""),
            "avatar": expert_dict.get("avatar"),
            "expertType": ExpertType(expert_dict.get("expertType") or expert_dict.get("expert_type", "high_fidelity")),
            "category": CategoryType(expert_dict.get("category", "marketing")),
            "createdAt": expert_dict.get("createdAt") or expert_dict.get("created_at") or datetime.utcnow()
        }
        
        return Expert(**mapped_dict)

    # CONVERSATION & MESSAGE OPERATIONS
    async def create_conversation(self, data: ConversationCreate) -> Conversation:
        """Creates a conversation in the database."""
        conversation_id = str(uuid.uuid4())
        # Ensure userId column exists (migration)
        try:
            await self._execute('ALTER TABLE conversations ADD COLUMN IF NOT EXISTS "userId" VARCHAR(255) DEFAULT \'default_user\'')
        except:
            pass  # Column may already exist
        
        query = """
            INSERT INTO conversations (id, "expertId", title, "userId", "createdAt", "updatedAt")
            VALUES ($1, $2, $3, 'default_user', NOW(), NOW())
            RETURNING *;
        """
        record = await self._fetchrow(query, conversation_id, data.expertId, data.title)
        
        # Map field names (PostgreSQL may return lowercase)
        record_dict = dict(record)
        if "userid" in record_dict and "userId" not in record_dict:
            record_dict["userId"] = record_dict.get("userid") or "default_user"
        if "expertid" in record_dict and "expertId" not in record_dict:
            record_dict["expertId"] = record_dict["expertid"]
        if "createdat" in record_dict and "createdAt" not in record_dict:
            record_dict["createdAt"] = record_dict["createdat"]
        if "updatedat" in record_dict and "updatedAt" not in record_dict:
            record_dict["updatedAt"] = record_dict["updatedat"]
        
        # Ensure userId exists (add default if missing)
        if "userId" not in record_dict:
            record_dict["userId"] = "default_user"
        
        return Conversation(**record_dict)

    async def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Fetches a single conversation by ID."""
        record = await self._fetchrow("SELECT * FROM conversations WHERE id = $1", conversation_id)
        if not record:
            return None
        
        # Map field names (PostgreSQL may return lowercase)
        record_dict = dict(record)
        if "userid" in record_dict and "userId" not in record_dict:
            record_dict["userId"] = record_dict.get("userid") or "default_user"
        if "expertid" in record_dict and "expertId" not in record_dict:
            record_dict["expertId"] = record_dict["expertid"]
        if "createdat" in record_dict and "createdAt" not in record_dict:
            record_dict["createdAt"] = record_dict["createdat"]
        if "updatedat" in record_dict and "updatedAt" not in record_dict:
            record_dict["updatedAt"] = record_dict["updatedat"]
        
        # Ensure userId exists
        if "userId" not in record_dict:
            record_dict["userId"] = "default_user"
        
        return Conversation(**record_dict)

    async def get_conversations(self, expert_id: Optional[str] = None) -> List[Conversation]:
        """Fetches conversations, optionally filtered by expert."""
        if expert_id:
            records = await self._fetch(
                'SELECT * FROM conversations WHERE "expertId" = $1 ORDER BY "updatedAt" DESC',
                expert_id
            )
        else:
            records = await self._fetch('SELECT * FROM conversations ORDER BY "updatedAt" DESC')
        
        # Map field names for each record
        conversations = []
        for record in records:
            record_dict = dict(record)
            if "userid" in record_dict and "userId" not in record_dict:
                record_dict["userId"] = record_dict.get("userid") or "default_user"
            if "expertid" in record_dict and "expertId" not in record_dict:
                record_dict["expertId"] = record_dict["expertid"]
            if "createdat" in record_dict and "createdAt" not in record_dict:
                record_dict["createdAt"] = record_dict["createdat"]
            if "updatedat" in record_dict and "updatedAt" not in record_dict:
                record_dict["updatedAt"] = record_dict["updatedat"]
            
            # Ensure userId exists
            if "userId" not in record_dict:
                record_dict["userId"] = "default_user"
            
            conversations.append(Conversation(**record_dict))
        
        return conversations

    async def create_message(self, data: MessageSend) -> Message:
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
    async def save_business_profile(self, user_id: str, data: dict) -> dict:
        """Saves or updates a business profile."""
        # For now, return None - to be implemented when we add business_profiles table
        raise NotImplementedError

    async def get_business_profile(self, user_id: str) -> Optional[dict]:
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
                try:
                    persona_dict[json_field] = json.loads(persona_dict[json_field])
                except (json.JSONDecodeError, TypeError):
                    persona_dict[json_field] = {}
        
        # Parse list fields that might come as strings
        for list_field in ['painPoints', 'goals', 'values', 'communities']:
            if list_field in persona_dict:
                if isinstance(persona_dict[list_field], str):
                    try:
                        # Try to parse as JSON array
                        parsed = json.loads(persona_dict[list_field])
                        if isinstance(parsed, list):
                            persona_dict[list_field] = parsed
                        else:
                            persona_dict[list_field] = []
                    except (json.JSONDecodeError, TypeError):
                        # If it's a string like '[]', convert to empty list
                        if persona_dict[list_field] == '[]' or persona_dict[list_field] == '':
                            persona_dict[list_field] = []
                        else:
                            # Single value or comma-separated, convert to list
                            persona_dict[list_field] = [item.strip() for item in persona_dict[list_field].split(',') if item.strip()]
                elif persona_dict[list_field] is None:
                    persona_dict[list_field] = []
        
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
                    try:
                        persona_dict[json_field] = json.loads(persona_dict[json_field])
                    except (json.JSONDecodeError, TypeError):
                        persona_dict[json_field] = {}
            
            # Parse list fields that might come as strings
            for list_field in ['painPoints', 'goals', 'values', 'communities']:
                if list_field in persona_dict:
                    if isinstance(persona_dict[list_field], str):
                        try:
                            # Try to parse as JSON array
                            parsed = json.loads(persona_dict[list_field])
                            if isinstance(parsed, list):
                                persona_dict[list_field] = parsed
                            else:
                                persona_dict[list_field] = []
                        except (json.JSONDecodeError, TypeError):
                            # If it's a string like '[]', convert to empty list
                            if persona_dict[list_field] == '[]' or persona_dict[list_field] == '':
                                persona_dict[list_field] = []
                            else:
                                # Single value or comma-separated, convert to list
                                persona_dict[list_field] = [item.strip() for item in persona_dict[list_field].split(',') if item.strip()]
                    elif persona_dict[list_field] is None:
                        persona_dict[list_field] = []
            
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
    
    # =============================================================================
    # COUNCIL CONVERSATION OPERATIONS
    # =============================================================================
    
    async def create_council_conversation(self, user_id: str, persona_id: str, problem: str, expert_ids: List[str], analysis_id: Optional[str] = None) -> 'CouncilConversation':
        """Create a new council conversation"""
        from python_backend.models import CouncilConversation
        import uuid
        
        conversation_id = str(uuid.uuid4())
        
        # Insert into database (create table if needed)
        # For now, we'll use a simple approach: store in JSON format
        # TODO: Create proper table schema for council_conversations
        query = """
            INSERT INTO council_conversations (id, "userId", "personaId", problem, "expertIds", "analysisId", "createdAt", "updatedAt")
            VALUES ($1, $2, $3, $4, $5::jsonb, $6, NOW(), NOW())
            RETURNING *;
        """
        
        try:
            record = await self._fetchrow(
                query,
                conversation_id,
                user_id,
                persona_id,
                problem,
                json.dumps(expert_ids),
                analysis_id  # Adicionar analysis_id no primeiro INSERT também
            )
            
            # Parse expertIds from JSON
            expert_ids_list = json.loads(record["expertIds"]) if isinstance(record["expertIds"], str) else record["expertIds"]
            
            # Try both case variations for field names
            user_id_field = record.get("userId") or record.get("userid")
            persona_id_field = record.get("personaId") or record.get("personaid")
            expert_ids_field = record.get("expertIds") or record.get("expertids")
            analysis_id_field = record.get("analysisId") or record.get("analysisid")
            created_at_field = record.get("createdAt") or record.get("createdat")
            updated_at_field = record.get("updatedAt") or record.get("updatedat")
            
            return CouncilConversation(
                id=str(record["id"]),
                userId=user_id_field,
                personaId=persona_id_field,
                problem=record["problem"],
                expertIds=expert_ids_list,
                analysisId=analysis_id_field if analysis_id_field else None,
                createdAt=created_at_field,
                updatedAt=updated_at_field
            )
        except asyncpg.exceptions.UndefinedTableError:
            # Table doesn't exist, create it
            await self._create_council_conversations_table()
            # Retry the insert
            record = await self._fetchrow(
                query,
                conversation_id,
                user_id,
                persona_id,
                problem,
                json.dumps(expert_ids),
                analysis_id
            )
            expert_ids_list = json.loads(record["expertIds"]) if isinstance(record["expertIds"], str) else record["expertIds"]
            
            # Try both case variations for field names
            user_id_field = record.get("userId") or record.get("userid")
            persona_id_field = record.get("personaId") or record.get("personaid")
            expert_ids_field = record.get("expertIds") or record.get("expertids")
            analysis_id_field = record.get("analysisId") or record.get("analysisid")
            created_at_field = record.get("createdAt") or record.get("createdat")
            updated_at_field = record.get("updatedAt") or record.get("updatedat")
            
            return CouncilConversation(
                id=str(record["id"]),
                userId=user_id_field,
                personaId=persona_id_field,
                problem=record["problem"],
                expertIds=expert_ids_list,
                analysisId=analysis_id_field if analysis_id_field else None,
                createdAt=created_at_field,
                updatedAt=updated_at_field
            )
    
    async def _create_council_conversations_table(self):
        """Create council_conversations table if it doesn't exist"""
        query = """
            CREATE TABLE IF NOT EXISTS council_conversations (
                id UUID PRIMARY KEY,
                "userId" VARCHAR(255) NOT NULL,
                "personaId" VARCHAR(255) NOT NULL,
                problem TEXT NOT NULL,
                "expertIds" JSONB NOT NULL,
                "analysisId" VARCHAR(255),
                "createdAt" TIMESTAMP NOT NULL DEFAULT NOW(),
                "updatedAt" TIMESTAMP NOT NULL DEFAULT NOW()
            );
        """
        await self._execute(query)
    
    async def get_council_conversation(self, conversation_id: str) -> Optional['CouncilConversation']:
        """Get a council conversation by ID"""
        from python_backend.models import CouncilConversation
        
        query = 'SELECT * FROM council_conversations WHERE id = $1'
        try:
            record = await self._fetchrow(query, conversation_id)
            if not record:
                return None
            
            # Parse expertIds from JSON
            expert_ids_list = json.loads(record["expertIds"]) if isinstance(record["expertIds"], str) else record["expertIds"]
            
            # Try both case variations for field names
            user_id_field = record.get("userId") or record.get("userid")
            persona_id_field = record.get("personaId") or record.get("personaid")
            analysis_id_field = record.get("analysisId") or record.get("analysisid")
            created_at_field = record.get("createdAt") or record.get("createdat")
            updated_at_field = record.get("updatedAt") or record.get("updatedat")
            
            return CouncilConversation(
                id=str(record["id"]),
                userId=user_id_field,
                personaId=persona_id_field,
                problem=record["problem"],
                expertIds=expert_ids_list,
                analysisId=analysis_id_field if analysis_id_field else None,
                createdAt=created_at_field,
                updatedAt=updated_at_field
            )
        except asyncpg.exceptions.UndefinedTableError:
            return None
    
    async def get_council_conversations(self, user_id: Optional[str] = None) -> List['CouncilConversation']:
        """Get all council conversations, optionally filtered by user"""
        from python_backend.models import CouncilConversation
        
        if user_id:
            query = 'SELECT * FROM council_conversations WHERE "userId" = $1 ORDER BY "updatedAt" DESC'
            records = await self._fetch(query, user_id)
        else:
            query = 'SELECT * FROM council_conversations ORDER BY "updatedAt" DESC'
            records = await self._fetch(query)
        
        conversations = []
        for record in records:
            expert_ids_list = json.loads(record["expertIds"]) if isinstance(record["expertIds"], str) else record["expertIds"]
            conversations.append(CouncilConversation(
                id=str(record["id"]),
                userId=record["userId"],
                personaId=record["personaId"],
                problem=record["problem"],
                expertIds=expert_ids_list,
                analysisId=record.get("analysisId"),
                createdAt=record["createdAt"],
                updatedAt=record["updatedAt"]
            ))
        
        return conversations
    
    async def create_council_message(self, conversation_id: str, role: str, content: str, expert_id: Optional[str] = None, expert_name: Optional[str] = None) -> 'CouncilMessage':
        """Create a message in a council conversation"""
        from python_backend.models import CouncilMessage
        import uuid
        
        message_id = str(uuid.uuid4())
        
        query = """
            INSERT INTO council_messages (id, "conversationId", "expertId", "expertName", content, role, timestamp)
            VALUES ($1, $2, $3, $4, $5, $6, NOW())
            RETURNING *;
        """
        
        try:
            record = await self._fetchrow(
                query,
                message_id,
                conversation_id,
                expert_id,
                expert_name,
                content,
                role
            )
            
            # Update conversation timestamp
            await self._execute(
                'UPDATE council_conversations SET "updatedAt" = NOW() WHERE id = $1',
                conversation_id
            )
            
            # Parse reactions (default empty list)
            reactions = []
            if record.get("reactions"):
                reactions = json.loads(record["reactions"]) if isinstance(record["reactions"], str) else record["reactions"]
            
            return CouncilMessage(
                id=str(record["id"]),
                conversationId=str(record["conversationId"]),
                expertId=record["expertId"],
                expertName=record["expertName"],
                content=record["content"],
                role=record["role"],
                timestamp=record["timestamp"],
                reactions=reactions
            )
        except asyncpg.exceptions.UndefinedTableError:
            # Table doesn't exist, create it
            await self._create_council_messages_table()
            # Retry the insert
            record = await self._fetchrow(
                query,
                message_id,
                conversation_id,
                expert_id,
                expert_name,
                content,
                role
            )
            await self._execute(
                'UPDATE council_conversations SET "updatedAt" = NOW() WHERE id = $1',
                conversation_id
            )
            reactions = []
            if record.get("reactions"):
                reactions = json.loads(record["reactions"]) if isinstance(record["reactions"], str) else record["reactions"]
            return CouncilMessage(
                id=str(record["id"]),
                conversationId=str(record["conversationId"]),
                expertId=record["expertId"],
                expertName=record["expertName"],
                content=record["content"],
                role=record["role"],
                timestamp=record["timestamp"],
                reactions=reactions
            )
    
    async def _create_council_messages_table(self):
        """Create council_messages table if it doesn't exist"""
        query = """
            CREATE TABLE IF NOT EXISTS council_messages (
                id UUID PRIMARY KEY,
                "conversationId" UUID NOT NULL REFERENCES council_conversations(id) ON DELETE CASCADE,
                "expertId" VARCHAR(255),
                "expertName" VARCHAR(255),
                content TEXT NOT NULL,
                role VARCHAR(50) NOT NULL,
                timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
                reactions JSONB DEFAULT '[]'::jsonb
            );
            
            CREATE INDEX IF NOT EXISTS idx_council_messages_conversation ON council_messages("conversationId");
        """
        await self._execute(query)
    
    async def get_council_messages(self, conversation_id: str) -> List['CouncilMessage']:
        """Get all messages for a council conversation"""
        from python_backend.models import CouncilMessage
        
        query = 'SELECT * FROM council_messages WHERE "conversationId" = $1 ORDER BY timestamp ASC'
        try:
            records = await self._fetch(query, conversation_id)
        except asyncpg.exceptions.UndefinedTableError:
            return []
        
        messages = []
        for record in records:
            reactions = []
            if record.get("reactions"):
                reactions = json.loads(record["reactions"]) if isinstance(record["reactions"], str) else record["reactions"]
            
            messages.append(CouncilMessage(
                id=str(record["id"]),
                conversationId=str(record["conversationId"]),
                expertId=record["expertId"],
                expertName=record["expertName"],
                content=record["content"],
                role=record["role"],
                timestamp=record["timestamp"],
                reactions=reactions
            ))
        
        return messages
    
    async def add_council_message_reaction(self, message_id: str, reaction: 'MessageReaction') -> bool:
        """Add a reaction to a council message"""
        from python_backend.models import MessageReaction
        
        # Get current message
        message = await self._fetchrow('SELECT reactions FROM council_messages WHERE id = $1', message_id)
        if not message:
            return False
        
        # Get current reactions
        reactions = []
        if message.get("reactions"):
            reactions = json.loads(message["reactions"]) if isinstance(message["reactions"], str) else message["reactions"]
        
        # Add new reaction
        reactions.append(reaction.model_dump() if hasattr(reaction, 'model_dump') else reaction.dict() if hasattr(reaction, 'dict') else reaction)
        
        # Update message
        await self._execute(
            'UPDATE council_messages SET reactions = $1::jsonb WHERE id = $2',
            json.dumps(reactions),
            message_id
        )
        
        return True
    
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
