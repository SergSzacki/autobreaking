-- PostgreSQL migration: store the part's photo URLs as a JSON array.
-- Existing rows receive an empty array, and future rows use the same default.
ALTER TABLE part
    ADD COLUMN IF NOT EXISTS photos JSONB NOT NULL DEFAULT '[]'::jsonb;

-- Rollback:
-- ALTER TABLE part DROP COLUMN IF EXISTS photos;
