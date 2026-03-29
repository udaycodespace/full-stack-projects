CREATE TABLE IF NOT EXISTS api_sources (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    base_url TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    api_source_id INTEGER NOT NULL REFERENCES api_sources(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    city TEXT,
    company_name TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (user_id > 0)
);

CREATE TABLE IF NOT EXISTS records (
    record_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    api_source_id INTEGER NOT NULL REFERENCES api_sources(id) ON DELETE CASCADE,
    external_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    consumed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (external_id > 0),
    UNIQUE (external_id, api_source_id)
);
