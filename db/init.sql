CREATE TABLE IF NOT EXISTS entries (
    id SERIAL PRIMARY KEY,
    col1 TEXT,
    col2 TEXT[],
    col3 TEXT[]
);

CREATE INDEX IF NOT EXISTS col2_gin ON entries USING GIN (col2);
CREATE INDEX IF NOT EXISTS col3_gin ON entries USING GIN (col3);
