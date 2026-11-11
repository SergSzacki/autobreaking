-- Add the photo URL list to the existing parts table.
-- PostgreSQL migration; the JSON array default keeps existing rows valid.
ALTER TABLE part
    ADD COLUMN IF NOT EXISTS photos JSON NOT NULL DEFAULT '[]'::json;

-- Rollback:
-- ALTER TABLE part DROP COLUMN IF EXISTS photos;
