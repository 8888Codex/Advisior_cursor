-- Tabela para armazenar personas profundas (Framework de 20 pontos)
CREATE TABLE IF NOT EXISTS personas_deep (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    name VARCHAR(500) NOT NULL,
    research_mode VARCHAR(50) DEFAULT 'deep',
    target_description TEXT NOT NULL,
    industry VARCHAR(255),
    data JSONB NOT NULL,  -- Armazena toda a estrutura de 20 pontos
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_personas_deep_user_id ON personas_deep(user_id);
CREATE INDEX IF NOT EXISTS idx_personas_deep_created_at ON personas_deep(created_at DESC);
