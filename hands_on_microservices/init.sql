-- Création de la table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age INT
);

-- Importation des données depuis le fichier CSV
COPY users(name, age)
FROM '/docker-entrypoint-initdb.d/data.csv'
DELIMITER ','
CSV HEADER;