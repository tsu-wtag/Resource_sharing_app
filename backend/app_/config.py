import psycopg2
import os

conn = psycopg2.connect(
    dbname = os.environ.get('DB_NAME'),
    user = os.environ.get('DB_USER'),
    password = os.environ.get('DB_PASSWORD'),
    host = os.environ.get('DB_HOST'),
    port = os.environ.get('DB_PORT'),
)


# conn = psycopg2.connect(
#     dbname=os.environ.get('POSTGRES_DB'),
#     user=os.environ.get('POSTGRES_USER'),
#     password=os.environ.get('POSTGRES_PASSWORD'),
#     host=os.environ.get('POSTGRES_HOST'),
#     port=os.environ.get('POSTGRES_PORT')
# )
