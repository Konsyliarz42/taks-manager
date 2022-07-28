-- Upgrade --
CREATE TABLE User(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(256) NOT NULL,
    last_name VARCHAR(256) NOT NULL,
    email VARCHAR(256) UNIQUE NOT NULL,
    password VARCHAR(512) UNIQUE NOT NULL,
    is_admin BOOLEAN DEFAULT False,
    register_at TIMESTAMP NOT NULL
); 

-- Downgrade --
DROP TABLE User;
