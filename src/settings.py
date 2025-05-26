# ============================ Imports and Environment Setup =============================
import os
from dotenv import load_dotenv
from sqlalchemy import inspect

# Llama Index imports
from llama_index.llms.groq import Groq
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings, SQLDatabase, VectorStoreIndex
from llama_index.core.objects import SQLTableNodeMapping, ObjectIndex, SQLTableSchema
from llama_index.core.retrievers import SQLRetriever

# Project-specific imports
from src.utility import load_config, create_sqldb_and_tables
from src.prompt import CONTEXT

# ============================ Load Environment Variables ================================
load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")


# ============================ Load Configuration ========================================
config = load_config()


# ============================ Initialize LLM and Embedding Models =======================
# Initialize the Groq LLM
llm_model = config["groq"]["model"]
llm = Groq(model=llm_model, api_key=api_key)

# Access the Ollama settings from the config.yaml
ollama_config = config['ollama']
base_url = f"http://{ollama_config['host']}:{ollama_config['port']}"

# Initialize the embedding model
embedding_model = OllamaEmbedding(
    model_name=ollama_config['embedding_model'],  # Model for generating embeddings
    base_url=base_url,                            # Base URL for the embedding model
)

# Set the LLM and embedding model in the global settings
Settings.llm = llm
Settings.embed_model = embedding_model


# ============================ Database Initialization ==================================
# Define paths for data and database
data_dir_path = f"{os.getcwd()}/resources/data"
sqldb_path = f"{os.getcwd()}/resources/Database.db"

# Create the database and tables
engine = create_sqldb_and_tables(dir_path=data_dir_path, db_path=sqldb_path)

# Inspect the database to get table names
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"Tables Present in db: {tables}")


# ============================ SQL Database and Index Setup =============================
# Create an SQLDatabase instance
sql_database = SQLDatabase(engine, include_tables=tables)

# Create a mapping between SQL tables and nodes in the index
table_node_mapping = SQLTableNodeMapping(sql_database)

# Create a list of SQLTableSchema objects with context descriptions
table_schema_objs = [
    SQLTableSchema(table_name=t, context_str=c)
    for t, c in zip(tables, CONTEXT)
]

# Create an ObjectIndex for efficient retrieval
obj_index = ObjectIndex.from_objects(
    table_schema_objs,    # List of table schemas with context descriptions
    table_node_mapping,   # Mapping between SQL tables and index nodes
    VectorStoreIndex,     # Index type used for storing and retrieving vectors
)

# Create a retriever for fetching similar objects (tables) based on queries
table_retriever = obj_index.as_retriever(similarity_top_k=3)


# ============================ SQL Query Executor ============================
# Initialize the SQLRetriever with the SQLDatabase instance
SQL_QUERY_EXECUTOR = SQLRetriever(sql_database)

