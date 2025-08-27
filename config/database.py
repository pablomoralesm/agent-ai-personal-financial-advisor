"""
Database configuration for MySQL connection.
"""

import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class DatabaseConfig:
    """Configuration class for database connection parameters."""
    
    host: str
    port: int
    database: str
    username: str
    password: str
    
    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        """Create DatabaseConfig from environment variables."""
        return cls(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '3306')),
            database=os.getenv('DB_NAME', 'financial_advisor'),
            username=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
    
    def get_connection_string(self) -> str:
        """Generate MySQL connection string."""
        return f"mysql+mysqlconnector://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
    
    def __repr__(self) -> str:
        """String representation hiding password."""
        return (f"DatabaseConfig(host='{self.host}', port={self.port}, "
                f"database='{self.database}', username='{self.username}', "
                f"password='***')")


# Global database configuration instance
db_config = DatabaseConfig.from_env()
