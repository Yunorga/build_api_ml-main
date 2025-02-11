CREATE DATABASE your_database_name;

\c your_database_name

CREATE TABLE your_table_name (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age INT
);

COPY your_table_name (id, name, age)
FROM '../data/data.csv'
DELIMITER ','
CSV HEADER;