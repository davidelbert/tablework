CREATE TABLE IF NOT EXISTS entries (
    id SERIAL PRIMARY KEY,
    index_id INTEGER UNIQUE,
    abstract TEXT,
    pro TEXT[],
    mat TEXT[],
    smt TEXT[],
    dsc TEXT[],
    spl TEXT[],
    cmt TEXT[],
    apl TEXT[],
    title TEXT,
    doi TEXT,
    pii TEXT,
    journal TEXT
);


CREATE INDEX IF NOT EXISTS idx_pro ON entries USING GIN (pro);
CREATE INDEX IF NOT EXISTS idx_mat ON entries USING GIN (mat);
CREATE INDEX IF NOT EXISTS idx_smt ON entries USING GIN (smt);
CREATE INDEX IF NOT EXISTS idx_dsc ON entries USING GIN (dsc);
CREATE INDEX IF NOT EXISTS idx_spl ON entries USING GIN (spl);
CREATE INDEX IF NOT EXISTS idx_cmt ON entries USING GIN (cmt);
CREATE INDEX IF NOT EXISTS idx_apl ON entries USING GIN (apl);

