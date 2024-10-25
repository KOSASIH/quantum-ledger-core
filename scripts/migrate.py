import os
import logging
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Migrator:
    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = create_engine(self.db_url)
        self.alembic_cfg = Config("alembic.ini")

    def run_migrations(self):
        """Run database migrations."""
        logger.info("Running database migrations...")
        command.upgrade(self.alembic_cfg, "head")
        logger.info("Database migrations completed successfully.")

if __name__ == "__main__":
    DB_URL = os.getenv("DATABASE_URL", "sqlite:///example.db")
    
    migrator = Migrator(DB_URL)
    migrator.run_migrations()
