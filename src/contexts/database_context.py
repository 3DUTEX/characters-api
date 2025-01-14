import psycopg2
import os

conn = psycopg2.connect(
    database= os.getenv('DB_NAME'),
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    port=os.getenv('DB_PORT')
)

cursor = conn.cursor()
