import sys
import os

# this is needed to import classes from other modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from services.database.database import Base, engine
import models.batch 
import models.job
import models.vector_db_metadata
import models.embeddings_metadata
from sqlalchemy import create_engine, text
import psycopg2

def create_admin_engine(username, password, host):
    admin_url = f"postgresql://{username}:{password}@{host}:5432/postgres"
    return create_engine(admin_url)

def database_exists(username, password, host, db_name):
    engine = create_admin_engine(username, password, host)
    connection = engine.connect()
    query = text(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")
    result = connection.execute(query).fetchone()
    connection.close()
    engine.dispose()
    return result is not None


def create_database(username, password, host, db_name):
    engine = create_admin_engine(username, password, host)
    connection = engine.raw_connection()
    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE {db_name}")
    cursor.close()
    connection.close()
    engine.dispose()

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    username = os.getenv('POSTGRES_USERNAME')
    password = os.getenv('POSTGRES_PASSWORD')
    database_name = os.getenv('POSTGRES_DB')
    host = os.getenv('POSTGRES_HOST')
    
    if not database_exists(username, password, host, database_name):
        print(f"Database {database_name} does not exist. Creating...")
        create_database(username, password, host, database_name)
        print(f"Database {database_name} created successfully.")

    create_tables()
