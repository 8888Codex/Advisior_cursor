-- Migration: Create user_preferences table
-- Description: Stores user preferences for conversation style and content
-- Created: 2024

CREATE TABLE IF NOT EXISTS user_preferences (
    user_id VARCHAR(255) PRIMARY KEY,
    style_preference VARCHAR(20) CHECK (style_preference IN ('objetivo', 'detalhado')),
    focus_preference VARCHAR(20) CHECK (focus_preference IN ('ROI-first', 'brand-first')),
    tone_preference VARCHAR(20) CHECK (tone_preference IN ('prático', 'estratégico')),
    communication_preference VARCHAR(20) CHECK (communication_preference IN ('bullets', 'blocos')),
    conversation_style VARCHAR(20) CHECK (conversation_style IN ('coach', 'consultor', 'direto')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Foreign key constraint (optional, if users table exists)
    -- CONSTRAINT fk_user_preferences_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_user_preferences_user_id ON user_preferences(user_id);

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_user_preferences_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_user_preferences_updated_at
    BEFORE UPDATE ON user_preferences
    FOR EACH ROW
    EXECUTE FUNCTION update_user_preferences_updated_at();

-- Comments for documentation
COMMENT ON TABLE user_preferences IS 'Stores user preferences for conversation style and content formatting';
COMMENT ON COLUMN user_preferences.user_id IS 'Foreign key to users table';
COMMENT ON COLUMN user_preferences.style_preference IS 'Preferred response style: objetivo (concise) or detalhado (detailed)';
COMMENT ON COLUMN user_preferences.focus_preference IS 'Preferred focus: ROI-first or brand-first';
COMMENT ON COLUMN user_preferences.tone_preference IS 'Preferred tone: prático (practical) or estratégico (strategic)';
COMMENT ON COLUMN user_preferences.communication_preference IS 'Preferred communication format: bullets or blocos (paragraphs)';
COMMENT ON COLUMN user_preferences.conversation_style IS 'Preferred conversation style: coach, consultor, or direto (direct)';

