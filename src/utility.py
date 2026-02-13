import os
import yaml
import logging
import pandas as pd
from sqlalchemy import create_engine, inspect

# ============================ Logging Configuration ============================
def get_logger(name=__name__):
    """
    Configure and return a standard logger.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

logger = get_logger("Text2SQL")


# ============================ Configuration Loader ============================
def load_config():
    """
    Load the configuration from a YAML file.

    Returns:
        dict: Configuration dictionary loaded from the YAML file.
    """
    config_path = f"{os.getcwd()}/config/config.yml"
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config

# ============================ Database Utility Functions ============================
def create_sqldb_and_tables(dir_path: str, db_path: str):
    """
    Create a SQLite database and populate it with tables from CSV files in the specified directory.

    Args:
        dir_path (str): Path to the directory containing CSV files.
        db_path (str): Path to the SQLite database file.

    Returns:
        sqlalchemy.engine.Engine: SQLAlchemy engine connected to the database.
    """
    # List all CSV files in the directory
    csv_files = [file for file in os.listdir(dir_path) if file.endswith('.csv')]

    # Create a SQLAlchemy engine
    engine = create_engine(f"sqlite:///{db_path}")
    logger.info(f"Successfully connected to the SQL database: {engine}")

    # Inspect existing tables in the database
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    logger.info(f"Tables present in database: {existing_tables}")

    # Iterate through CSV files and create tables
    for file in csv_files:
        table_name = os.path.splitext(file)[0]  # Extract table name from the file name
        csv_path = os.path.join(dir_path, file)
        df = pd.read_csv(csv_path)

        if table_name not in existing_tables:
            # Create a new table and populate it with data
            df.to_sql(table_name, engine, index=False)
            logger.info(f"Table '{table_name}' has been created and data has been added.")
        else:
            logger.info(f"Table '{table_name}' already exists in the database.")

    return engine
