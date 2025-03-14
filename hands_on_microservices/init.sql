-- -- Création de la table
-- CREATE TABLE IF NOT EXISTS users (
--     id SERIAL PRIMARY KEY,
--     name VARCHAR(100),
--     age INT
-- );

-- -- Importation des données depuis le fichier CSV
-- COPY users(name, age)
-- FROM '/docker-entrypoint-initdb.d/data.csv'
-- DELIMITER ','
-- CSV HEADER;

-- CREATE TABLE IF NOT EXISTS images (
--     id SERIAL PRIMARY KEY,
--     nom VARCHAR(100) NOT NULL,
--     email VARCHAR(255) UNIQUE NOT NULL,
--     age INTEGER NOT NULL
-- );


CREATE TABLE IF NOT EXISTS images (
    id SERIAL PRIMARY KEY,
    description TEXT,
    image BYTEA
)