
-- Tabla principal con las respuestas por keyword
CREATE TABLE IF NOT EXISTS keyword_responses (
    keyword TEXT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    response_type TEXT NOT NULL,
    content TEXT,
    emoji TEXT,
    gif_url TEXT,
    random BOOLEAN DEFAULT FALSE
);

-- Tabla con respuestas múltiples si random=True
CREATE TABLE IF NOT EXISTS keyword_response_variants (
    id SERIAL PRIMARY KEY,
    keyword TEXT REFERENCES keyword_responses(keyword) ON DELETE CASCADE,
    response TEXT NOT NULL
);
