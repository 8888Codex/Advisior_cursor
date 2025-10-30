import os
import asyncpg
import asyncio
from dotenv import load_dotenv

async def create_tables():
    """Connects to the database and creates the necessary tables."""
    
    # Load environment variables from .env file
    load_dotenv()
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL not found in .env file. Please ensure it is set.")
        return

    print(f"Connecting to the database...")
    conn = None
    try:
        conn = await asyncpg.connect(database_url)
        print("✅ Successfully connected to the database.")

        # Drop table to ensure clean seeding
        print("Dropping 'experts' table for a clean seed...")
        await conn.execute("DROP TABLE IF EXISTS experts;")
        print("✅ 'experts' table dropped.")

        # SQL commands to create tables based on shared/schema.ts
        # Note: This is a manual representation of the Drizzle schema.
        
        await conn.execute("""
            CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        """)

        print("Creating 'experts' table...")
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS experts (
                id VARCHAR PRIMARY KEY DEFAULT uuid_generate_v4(),
                name TEXT NOT NULL,
                title TEXT NOT NULL,
                expertise TEXT[] NOT NULL,
                bio TEXT NOT NULL,
                "systemPrompt" TEXT NOT NULL,
                avatar TEXT,
                "expertType" TEXT NOT NULL,
                category TEXT NOT NULL DEFAULT 'marketing',
                "createdAt" TIMESTAMP NOT NULL DEFAULT NOW(),
                "updatedAt" TIMESTAMP NOT NULL DEFAULT NOW()
            );
        """)
        print("✅ 'experts' table created or already exists.")

        print("Creating 'conversations' table...")
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id VARCHAR PRIMARY KEY DEFAULT uuid_generate_v4(),
                "expertId" VARCHAR NOT NULL,
                title TEXT NOT NULL,
                "createdAt" TIMESTAMP NOT NULL DEFAULT NOW(),
                "updatedAt" TIMESTAMP NOT NULL DEFAULT NOW()
            );
        """)
        print("✅ 'conversations' table created or already exists.")

        print("Creating 'messages' table...")
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id VARCHAR PRIMARY KEY DEFAULT uuid_generate_v4(),
                "conversationId" VARCHAR NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                "createdAt" TIMESTAMP NOT NULL DEFAULT NOW()
            );
        """)
        print("✅ 'messages' table created or already exists.")
        
        print("\nAll necessary tables have been created successfully!")

    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        if conn:
            await conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    asyncio.run(create_tables())
