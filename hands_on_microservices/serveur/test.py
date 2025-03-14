import psycopg2
import os

def create_database(db_params):
    """Creates a PostgreSQL table."""
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id SERIAL PRIMARY KEY,
                description TEXT,
                image BYTEA
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        print("Table 'images' created successfully.")
    except psycopg2.Error as e:
        print(f"Error creating table: {e}")

def insert_image(db_params, description, image_path):
    """Inserts an image and description into the PostgreSQL database."""
    try:
        with open(image_path, 'rb') as f:
            image_blob = f.read()

        # conn = psycopg2.connect(**db_params)
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO images (description, image) VALUES (%s, %s)', (description, psycopg2.Binary(image_blob)))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Image '{image_path}' inserted successfully.")

    except FileNotFoundError:
        print(f"Error: Image file '{image_path}' not found.")
    except psycopg2.Error as e:
        print(f"An PostgreSQL error occurred: {e}")

def retrieve_image(db_params, image_id, output_path):
    """Retrieves an image from the PostgreSQL database and saves it to a file."""
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        cursor.execute('SELECT image FROM images WHERE id = %s', (image_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            image_blob = result[0]
            with open(output_path, 'wb') as f:
                f.write(image_blob)
            print(f"Image retrieved and saved to '{output_path}'.")
        else:
            print(f"Image with ID {image_id} not found.")

    except psycopg2.Error as e:
        print(f"An PostgreSQL error occurred: {e}")

# Example usage:
# db_params = {
#     'host': 'postgres',  # Replace with your PostgreSQL host
#     'database': 'my_database',  # Replace with your database name
#     'user': 'postgres',  # Replace with your username
#     'password': '12345678'  # Replace with your password
# }

db_params = {
    "dbname": "my_database",
    "user": "postgres",
    "password": "12345678",
    "host": "postgres",
    "port": "5432"
}

image_file = 'image.png'  # Replace with your image file
description_text = 'A beautiful landscape.'
retrieved_image_file = 'retrieved_image.jpg'

if not os.path.exists(image_file):
    print(f"Error: {image_file} does not exist. Please place a jpg image in the same directory as the python script.")
else:
    create_database(db_params)
    insert_image(db_params, description_text, image_file)
    retrieve_image(db_params, 1, retrieved_image_file)
    print("Done.")