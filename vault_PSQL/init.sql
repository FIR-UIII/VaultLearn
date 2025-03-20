-- Create tables in the database
CREATE TABLE vault_kv_store (
parent_path TEXT COLLATE "C" NOT NULL,
path TEXT COLLATE "C",
key TEXT COLLATE "C",
value BYTEA,
CONSTRAINT pkey PRIMARY KEY (path, key)
);
CREATE INDEX parent_path_idx ON vault_kv_store (parent_path);

-- Create tables for HAEnabled backend
CREATE TABLE vault_ha_locks (
  ha_key                                      TEXT COLLATE "C" NOT NULL,
  ha_identity                                 TEXT COLLATE "C" NOT NULL,
  ha_value                                    TEXT COLLATE "C",
  valid_until                                 TIMESTAMP WITH TIME ZONE NOT NULL,
  CONSTRAINT ha_key PRIMARY KEY (ha_key)
);