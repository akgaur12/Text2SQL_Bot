import os
import pandas as pd
from typing import List
from llama_index.core.llms import ChatResponse

from src.settings import sql_database, SQLTableSchema, SQL_QUERY_EXECUTOR

# ============================ Get SQL Table Info Functions ============================
def get_sqltable_info(table_schema_objs: List[SQLTableSchema]) -> str:
    """
    Generate a context string for each table based on its schema and additional context.

    Args:
        table_schema_objs (List[SQLTableSchema]): List of table schema objects.

    Returns:
        str: Combined context string for all tables.
    """
    context_strs = []

    for table_schema_obj in table_schema_objs:
        # Get the schema and basic information of the table
        table_info = sql_database.get_single_table_info(table_schema_obj.table_name)

        # Append additional context or description of the table, if available
        if table_schema_obj.context_str:
            table_info += f"\nThe table description is: {table_schema_obj.context_str}"

        context_strs.append(table_info)

    # Return a combined context string for all tables
    return "\n\n".join(context_strs)


# ============================ Extract SQL Query Functions ============================

def extract_sql_query_from_response(response: ChatResponse) -> str:
    """
    Extract the SQL query from the LLM's response.

    Args:
        response (ChatResponse): The response object from the LLM.

    Returns:
        str: Extracted SQL query.
    """
    response_content = response.message.content
    print(response_content)

    # Locate the starting position of the SQL query in the response
    sql_query_start = response_content.find("SQLQuery:")
    if sql_query_start != -1:
        # Extract the portion of the response starting from "SQLQuery:"
        response_content = response_content[sql_query_start:]

        # Remove the "SQLQuery:" prefix
        if response_content.startswith("SQLQuery:"):
            response_content = response_content[len("SQLQuery:"):]

    # Locate the starting position of the explanation in the response
    sql_result_end = response_content.find("Explanation:")
    if sql_result_end != -1:
        # Exclude everything after "Explanation:"
        response_content = response_content[:sql_result_end]

    # Clean up the response by stripping unnecessary characters and markdown code blocks
    sql_query = response_content.strip().strip("```").strip()
    return sql_query


# ============================ Execute SQL Query Functions ============================
def execute_sql_query(sql_query: str):
    """
    Execute the given SQL query after validating it for safety.

    Args:
        sql_query (str): The SQL query to execute.

    Returns:
        Any: Query result if successful, or None if an error occurs.
    """
    try:
        # Convert the SQL query to lowercase for case-insensitive checks
        sql_lower = sql_query.lower()
        print(sql_query)

        # List of forbidden destructive and modification SQL keywords
        forbidden_keywords = ["delete", "drop", "truncate", "alter", "update", "insert"]

        # Check if the SQL query contains any forbidden keywords
        if any(keyword in sql_lower for keyword in forbidden_keywords):
            raise ValueError("Destructive or modifying SQL operation detected. Operation not allowed.")

        # Execute the query if it passes validation
        data = SQL_QUERY_EXECUTOR.retrieve(sql_query)
        return data

    except Exception as e:
        print(f"Error occurred while executing the SQL query: {str(e)}")
        return None