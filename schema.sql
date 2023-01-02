DROP TABLE IF EXISTS drone;

CREATE TABLE drone (
    drone_id CHAR(13) PRIMARY KEY,
    closest_approach FLOAT,
    last_seen TIMESTAMP,
    first_name TEXT,
    last_name TEXT,
    phone TEXT,
    email TEXT
);