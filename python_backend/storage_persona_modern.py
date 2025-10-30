"""
Storage functions for modern personas with cache and database support
"""
from typing import Dict, List, Optional, Any
import uuid
import json
import os
import time
from datetime import datetime
import asyncio
import asyncpg

from models_persona import PersonaModern

class PersonaModernStorage:
    """
    Storage methods for modern personas
    
    Features:
    - In-memory storage with TTL cache
    - Optional PostgreSQL support (when DATABASE_URL is set)
    - Automatic serialization/deserialization
    """
    
    def __init__(self):
        self.personas_modern = {}  # In-memory storage
        self.cache = {}  # Cache with TTL
        self.cache_ttl = 3600  # 1 hour in seconds
        
        # Check if PostgreSQL is configured
        self.use_postgres = os.getenv("DATABASE_URL") is not None
        self.db_connection_pool = None
        
        # Create DB schema if PostgreSQL is enabled
        if self.use_postgres:
            asyncio.create_task(self._init_postgres())
    
    async def _init_postgres(self):
        """Initialize PostgreSQL connection pool and schema"""
        try:
            # Create connection pool
            self.db_connection_pool = await asyncpg.create_pool(
                os.getenv("DATABASE_URL"),
                min_size=1,
                max_size=10
            )
            
            # Create schema if not exists
            async with self.db_connection_pool.acquire() as conn:
                await conn.execute("""
                CREATE TABLE IF NOT EXISTS personas_modern (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    data JSONB NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
                    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
                );
                CREATE INDEX IF NOT EXISTS personas_modern_user_id_idx ON personas_modern(user_id);
                """)
                
            print("[INFO] PostgreSQL initialized for modern personas")
        except Exception as e:
            print(f"[ERROR] Failed to initialize PostgreSQL: {str(e)}")
            self.use_postgres = False
    
    def _get_cache_key(self, method: str, **kwargs) -> str:
        """Generate a cache key from method name and arguments"""
        # Sort kwargs to ensure consistent keys
        sorted_kwargs = {k: kwargs[k] for k in sorted(kwargs.keys()) if kwargs[k] is not None}
        return f"{method}:{json.dumps(sorted_kwargs)}"
    
    def _get_cached_result(self, cache_key: str) -> Optional[Any]:
        """Get result from cache if it exists and is not expired"""
        if cache_key in self.cache:
            timestamp, data = self.cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return data
            else:
                # Remove expired cache entry
                del self.cache[cache_key]
        return None
    
    def _set_cache_result(self, cache_key: str, data: Any):
        """Store result in cache with current timestamp"""
        self.cache[cache_key] = (time.time(), data)
    
    def _clear_cache(self, method: Optional[str] = None):
        """Clear cache entries, optionally filtered by method"""
        if method:
            # Clear only cache entries for the specified method
            keys_to_remove = [k for k in self.cache.keys() if k.startswith(f"{method}:")]
            for key in keys_to_remove:
                del self.cache[key]
        else:
            # Clear all cache
            self.cache = {}
    
    async def create_persona_modern(self, user_id: str, persona: PersonaModern) -> PersonaModern:
        """Create a new modern persona"""
        try:
            # Store in memory
            self.personas_modern[persona.id] = persona
            
            # Store in PostgreSQL if enabled
            if self.use_postgres and self.db_connection_pool:
                try:
                    async with self.db_connection_pool.acquire() as conn:
                        # Convert persona to JSON
                        persona_json = persona.model_dump_json()
                        
                        # Insert into database
                        await conn.execute(
                            """
                            INSERT INTO personas_modern (id, user_id, data, created_at, updated_at)
                            VALUES ($1, $2, $3, $4, $5)
                            """,
                            persona.id,
                            user_id,
                            persona_json,
                            persona.created_at,
                            persona.updated_at
                        )
                except Exception as e:
                    print(f"[ERROR] Failed to store persona in PostgreSQL: {str(e)}")
            
            # Clear cache for list operations
            self._clear_cache("get_personas_modern")
            
            print(f"[INFO] Modern persona created: {persona.id}")
            return persona
        except Exception as e:
            print(f"[ERROR] Error creating modern persona: {str(e)}")
            raise
    
    async def get_persona_modern(self, persona_id: str) -> Optional[PersonaModern]:
        """Get a specific modern persona by ID"""
        # Check cache first
        cache_key = self._get_cache_key("get_persona_modern", persona_id=persona_id)
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            return cached_result
        
        # Check in-memory storage
        if persona_id in self.personas_modern:
            persona = self.personas_modern[persona_id]
            self._set_cache_result(cache_key, persona)
            return persona
        
        # Check PostgreSQL if enabled
        if self.use_postgres and self.db_connection_pool:
            try:
                async with self.db_connection_pool.acquire() as conn:
                    row = await conn.fetchrow(
                        "SELECT data FROM personas_modern WHERE id = $1",
                        persona_id
                    )
                    
                    if row:
                        # Convert JSON to PersonaModern
                        persona_data = json.loads(row["data"])
                        persona = PersonaModern(**persona_data)
                        
                        # Update in-memory storage
                        self.personas_modern[persona_id] = persona
                        
                        # Update cache
                        self._set_cache_result(cache_key, persona)
                        
                        return persona
            except Exception as e:
                print(f"[ERROR] Failed to get persona from PostgreSQL: {str(e)}")
        
        return None
    
    async def get_personas_modern(self, user_id: str) -> List[PersonaModern]:
        """Get all modern personas for a user"""
        # Check cache first
        cache_key = self._get_cache_key("get_personas_modern", user_id=user_id)
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            return cached_result
        
        personas = []
        
        # Check in-memory storage
        memory_personas = [
            persona for persona in self.personas_modern.values()
            if persona.userId == user_id
        ]
        
        # Check PostgreSQL if enabled
        if self.use_postgres and self.db_connection_pool:
            try:
                async with self.db_connection_pool.acquire() as conn:
                    rows = await conn.fetch(
                        "SELECT data FROM personas_modern WHERE user_id = $1 ORDER BY created_at DESC",
                        user_id
                    )
                    
                    if rows:
                        # Convert JSON to PersonaModern objects
                        for row in rows:
                            persona_data = json.loads(row["data"])
                            persona = PersonaModern(**persona_data)
                            personas.append(persona)
                            
                            # Update in-memory storage
                            self.personas_modern[persona.id] = persona
            except Exception as e:
                print(f"[ERROR] Failed to get personas from PostgreSQL: {str(e)}")
        
        # If no PostgreSQL or it failed, use in-memory personas
        if not personas:
            personas = memory_personas
        
        # Sort by created_at descending
        personas.sort(key=lambda p: p.created_at, reverse=True)
        
        # Update cache
        self._set_cache_result(cache_key, personas)
        
        return personas
    
    async def update_persona_modern(self, persona_id: str, updates: dict) -> Optional[PersonaModern]:
        """Update a modern persona"""
        persona = None
        
        # Check in-memory storage
        if persona_id in self.personas_modern:
            persona = self.personas_modern[persona_id]
            
            # Update fields
            for key, value in updates.items():
                if hasattr(persona, key):
                    setattr(persona, key, value)
            
            # Update timestamp
            persona.updated_at = datetime.utcnow()
            
            # Update in-memory storage
            self.personas_modern[persona_id] = persona
        
        # Update in PostgreSQL if enabled
        if self.use_postgres and self.db_connection_pool and persona:
            try:
                async with self.db_connection_pool.acquire() as conn:
                    # Convert persona to JSON
                    persona_json = persona.model_dump_json()
                    
                    # Update in database
                    await conn.execute(
                        """
                        UPDATE personas_modern
                        SET data = $1, updated_at = $2
                        WHERE id = $3
                        """,
                        persona_json,
                        persona.updated_at,
                        persona_id
                    )
            except Exception as e:
                print(f"[ERROR] Failed to update persona in PostgreSQL: {str(e)}")
        
        # Clear cache
        self._clear_cache("get_persona_modern")
        self._clear_cache("get_personas_modern")
        
        return persona
    
    async def delete_persona_modern(self, persona_id: str) -> bool:
        """Delete a modern persona"""
        success = False
        
        # Delete from in-memory storage
        if persona_id in self.personas_modern:
            del self.personas_modern[persona_id]
            success = True
        
        # Delete from PostgreSQL if enabled
        if self.use_postgres and self.db_connection_pool:
            try:
                async with self.db_connection_pool.acquire() as conn:
                    result = await conn.execute(
                        "DELETE FROM personas_modern WHERE id = $1",
                        persona_id
                    )
                    
                    # Check if any rows were deleted
                    if result and "DELETE" in result:
                        success = True
            except Exception as e:
                print(f"[ERROR] Failed to delete persona from PostgreSQL: {str(e)}")
        
        # Clear cache
        self._clear_cache("get_persona_modern")
        self._clear_cache("get_personas_modern")
        
        return success