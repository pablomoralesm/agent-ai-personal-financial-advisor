"""Database initialization script for the Financial Advisor app."""

import os
import mysql.connector
from mysql.connector import Error
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.utils.config import DB_CONFIG

def init_database():
    """Initialize the database with the schema."""
    connection = None
    try:
        # Create connection without database (to create it if needed)
        config_without_db = DB_CONFIG.copy()
        database_name = config_without_db.pop('database')
        
        connection = mysql.connector.connect(**config_without_db)
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        cursor.execute(f"USE {database_name}")
        
        # Read schema file
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        # Execute schema commands
        for statement in schema_sql.split(';'):
            if statement.strip():
                cursor.execute(statement)
        
        connection.commit()
        print(f"Database '{database_name}' initialized successfully.")
        
    except Error as e:
        print(f"Error initializing database: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def main():
    """Main function to initialize the database."""
    print("Initializing Financial Advisor database...")
    init_database()
    print("Database initialization complete.")

if __name__ == "__main__":
    main()
