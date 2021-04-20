DROP TABLE IF EXISTS headwords CASCADE;
DROP TABLE IF EXISTS meanings CASCADE;

-- includes language code
-- example: es_gato
CREATE TABLE headwords (
    headword TEXT PRIMARY KEY
);

CREATE TABLE meanings (
    id SERIAL PRIMARY KEY
    ,meaning TEXT NOT NULL
    ,headword TEXT REFERENCES headwords(headword)
);